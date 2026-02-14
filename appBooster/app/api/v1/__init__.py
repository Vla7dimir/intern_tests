"""API v1 routers."""

from fastapi import APIRouter

from app.api.v1 import experiments, statistics

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(experiments.router)
api_router.include_router(statistics.router)
