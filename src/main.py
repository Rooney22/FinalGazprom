import uvicorn
from src.core.settings import settings


if __name__ == '__main__':
    uvicorn.run('app:app',
                host=settings.host,
                port=settings.port,
                reload=True,
                )
