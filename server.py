import asyncio
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from routers import router

from fastapi.staticfiles import StaticFiles

from hypercorn.config import Config
from hypercorn.asyncio import serve


app = FastAPI(title='SignSense', docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.add_middleware(HTTPSRedirectMiddleware)

ROOT = os.path.dirname(__file__)


async def main(app, config):
    await serve(app, config)

if __name__ == "__main__":

    origins = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    config = Config()
    config.bind = ['0.0.0.0:8050']

    config.worker_class = 'asyncio'
    config.workers = 9
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(app, config))


