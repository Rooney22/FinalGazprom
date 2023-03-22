from fastapi import FastAPI

from src.api.base_router import router


app = FastAPI(
    title="Знаев Алексей. FinalGazprom",
    description="Финальный проект",
    version="0.0.1",
)

app.include_router(router)
