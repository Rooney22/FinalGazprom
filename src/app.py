from fastapi import FastAPI

from src.api.base_router import router


tags_dict = [
    {
        'name': 'authorization',
        'description': 'Авторизация',
    },
    {
        'name': 'methods',
        'description': 'Методы для работы с ML',
    }
]

app = FastAPI(
    title="Знаев Алексей. Backend",
    description="Финальный проект",
    version="0.1.0",
    openapi_tags=tags_dict,
)

app.include_router(router)
