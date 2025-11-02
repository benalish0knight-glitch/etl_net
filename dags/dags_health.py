from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests

# --- Variáveis de Conexão Temporárias ---
# ATENÇÃO: Se o Airflow estiver em Docker e o FastAPI estiver no seu OS, use host.docker.internal.
# Se AMBOS estiverem no seu OS sem Docker, use '127.0.0.1'.
# Se AMBOS estiverem em Docker, use o nome do serviço do FastAPI (ex: 'fastapi-app').
FASTAPI_HOST = 'http://host.docker.internal' 
FASTAPI_PORT = 8000
FASTAPI_ENDPOINT = '/' # O endpoint raiz
FASTAPI_BASE_URL = f"{FASTAPI_HOST}:{FASTAPI_PORT}"
# ----------------------------------------

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'jsonplaceholder_etl_local_check',
    default_args=default_args,
    description='ETL com verificação de saúde local (temporária)',
    schedule_interval=timedelta(hours=1),
    catchup=False,
    tags=['dev', 'local', 'fastapi']
)

def check_fastapi_health(**context):
    """
    Verifica se a API FastAPI está funcionando e retorna status 200.
    A URL de teste é construída diretamente no código.
    """
    health_url = f"{FASTAPI_BASE_URL}{FASTAPI_ENDPOINT}"
    
    try:
        print(f"Tentando acessar o health check em: {health_url}")
        response = requests.get(health_url, timeout=10)
        
        # O Airflow falhará a tarefa se esta linha levantar uma exceção
        # Aqui, estamos verificando explicitamente se o status é 200
        if response.status_code == 200:
            print(f"✅ FastAPI está saudável. Status: 200 OK.")
            return True
        else:
            print(f"❌ Erro de saúde: Status inesperado {response.status_code}. Conteúdo: {response.text[:100]}...")
            # Força a falha da tarefa
            raise Exception(f"Health check falhou com status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Captura erros de conexão (DNS, timeout, etc.)
        print(f"❌ Erro de conexão ao FastAPI: {str(e)}")
        # Força a falha da tarefa
        raise Exception(f"Falha na conexão HTTP: {e}")

# Task 1: Verificar saúde da API
health_check = PythonOperator(
    task_id='check_api_health_direct',
    python_callable=check_fastapi_health,
    dag=dag,
)