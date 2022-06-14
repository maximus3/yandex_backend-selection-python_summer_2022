from fastapi import FastAPI

from app.routers.delete import router as delete_router
from app.routers.imports import router as imports_router
from app.routers.node import router as node_router
from app.routers.nodes import router as nodes_router
from app.routers.sales import router as sales_router


def create_app():
    app = FastAPI()
    app.include_router(imports_router)
    app.include_router(delete_router)
    app.include_router(nodes_router)
    app.include_router(sales_router)
    app.include_router(node_router)

    return app
