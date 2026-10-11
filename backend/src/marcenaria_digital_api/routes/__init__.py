from fastapi import APIRouter

from .configuracao import estilos_router, router as configuracao_router

router = APIRouter()
router.include_router(configuracao_router)
router.include_router(estilos_router)

__all__ = ["router"]
