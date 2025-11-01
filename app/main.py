from fastapi import FastAPI, HTTPException
from httpx import AsyncClient
from typing import List, Dict, Any

app = FastAPI(title="JSONPlaceholder API Client")

BASE_URL = "https://jsonplaceholder.typicode.com"

@app.get("/")
async def root():
    return {
        "message": "FastAPI + JSONPlaceholder",
        "endpoints": {
            "posts": "/posts",
            "users": "/users",
            "comments": "/comments/{post_id}"
        }
    }

@app.get("/posts", response_model=List[Dict[str, Any]])
async def get_posts():
    """Busca todos os posts do JSONPlaceholder"""
    async with AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/posts")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar posts: {str(e)}")

@app.get("/posts/{post_id}", response_model=Dict[str, Any])
async def get_post(post_id: int):
    """Busca um post específico por ID"""
    async with AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/posts/{post_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar post: {str(e)}")

@app.get("/users", response_model=List[Dict[str, Any]])
async def get_users():
    """Busca todos os usuários do JSONPlaceholder"""
    async with AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/users")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar usuários: {str(e)}")

@app.get("/comments/{post_id}", response_model=List[Dict[str, Any]])
async def get_comments(post_id: int):
    """Busca comentários de um post específico"""
    async with AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/posts/{post_id}/comments")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar comentários: {str(e)}")

@app.post("/posts", response_model=Dict[str, Any])
async def create_post(title: str, body: str, userId: int = 1):
    """Cria um novo post (simulado)"""
    async with AsyncClient() as client:
        try:
            payload = {"title": title, "body": body, "userId": userId}
            response = await client.post(f"{BASE_URL}/posts", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao criar post: {str(e)}")