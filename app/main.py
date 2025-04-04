import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import router

load_dotenv()

app = FastAPI()

app.include_router(router)

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app, host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 8000))
    )
