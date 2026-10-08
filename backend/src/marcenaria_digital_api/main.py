from pathlib import Path

from fastapi import FastAPI

from marcenaria_digital_api.config import Settings
from marcenaria_digital_api.repositories.json import ConfiguracaoJsonRepository
from marcenaria_digital_api.routes import router
from marcenaria_digital_api.routes.exception_handlers import (
    registrar_exception_handlers,
)
from marcenaria_digital_api.services import ConfiguracaoService


def create_app(caminho_configuracoes: str | Path | None = None) -> FastAPI:
    """Cria a aplicação e compõe suas dependências concretas."""
    settings = Settings()
    repositorio = ConfiguracaoJsonRepository(
        caminho_configuracoes or settings.configuracoes_json_path
    )

    aplicacao = FastAPI(
        title="Marcenaria Digital API",
        version="1.0.0",
        description="API para configurações reutilizáveis de armários.",
    )
    aplicacao.state.configuracao_service = ConfiguracaoService(repositorio)
    registrar_exception_handlers(aplicacao)
    aplicacao.include_router(router, prefix="/api/v1")
    return aplicacao


app = create_app()
