from fastapi import APIRouter, Request, status

from marcenaria_digital_api.routes.exception_handlers import (
    ConfiguracaoDuplicadaResponse,
    ConfiguracaoInvalidaResponse,
    FalhaPersistenciaResponse,
)
from marcenaria_digital_api.routes.schemas import ConfiguracaoInput, ConfiguracaoOutput
from marcenaria_digital_api.services import ConfiguracaoService

router = APIRouter(prefix="/configuracoes", tags=["Configurações"])


@router.post(
    "",
    response_model=ConfiguracaoOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Criar configuração de armário",
    description=(
        "Valida os limites dimensionais, os detalhes e persiste uma nova "
        "configuração no catálogo JSON."
    ),
    responses={
        409: {
            "model": ConfiguracaoDuplicadaResponse,
            "description": "Já existe uma configuração com o id informado.",
        },
        422: {
            "model": ConfiguracaoInvalidaResponse,
            "description": "A configuração informada é inválida.",
        },
        500: {
            "model": FalhaPersistenciaResponse,
            "description": "Falha inesperada de persistência.",
        },
    },
)
def criar_configuracao(
    entrada: ConfiguracaoInput, request: Request
) -> ConfiguracaoOutput:
    """Recebe, valida e encaminha a criação de uma configuração ao serviço."""
    servico: ConfiguracaoService = request.app.state.configuracao_service
    configuracao = servico.criar(entrada.para_entidade())
    return ConfiguracaoOutput.da_entidade(configuracao)
