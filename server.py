import os
from multiprocessing import freeze_support, cpu_count

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import router

from fastapi.staticfiles import StaticFiles

import uvicorn

app = FastAPI(title='SignSense', docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")

ROOT = os.path.dirname(__file__)


def start_server(host="0.0.0.0", port=8050, workers_number=4,
                 loop="asyncio", reload=False):

    uvicorn.run("server:app", host=host, port=port,
                workers=workers_number, loop=loop, reload=reload, forwarded_allow_ips=['*'], ws_ping_interval=None)


if __name__ == "__main__":
    freeze_support()
    number_of_workers = int(cpu_count() * 0.75)

    origins = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    start_server(workers_number=number_of_workers, reload=False)

