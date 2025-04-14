import logging
import os
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from app.api.routes import router

load_dotenv()

app = FastAPI()


@app.middleware('http')
async def add_request_uuid(request: Request, call_next):
    request_id = str(uuid4())
    response = await call_next(request)
    response.headers['X-Request-ID'] = request_id
    return response


@app.middleware('http')
async def log_requests(request: Request, call_next):
    body = await request.body()
    logger.info(
        f'Incoming request: {request.method} {request.url} Body: {body.decode("utf-8")}'
    )
    response = await call_next(request)
    return response


app.include_router(router)


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app, host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 8000))
    )
