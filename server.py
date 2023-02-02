import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import router

from fastapi.staticfiles import StaticFiles

app = FastAPI(title='SignSense', docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

ROOT = os.path.dirname(__file__)


def start_server(host="0.0.0.0", port=8000, loop="asyncio", reload=False):
    import hypercorn

    hypercorn.run("server:app", host=host, port=port,
                loop=loop, reload=reload, forwarded_allow_ips=['*'])


if __name__ == "__main__":

    origins = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    start_server(reload=False)
