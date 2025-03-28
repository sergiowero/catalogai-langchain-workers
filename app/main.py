import logging
import os

from api.routes import router
from dotenv import load_dotenv
from fastapi import FastAPI

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
