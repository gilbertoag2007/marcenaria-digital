from typing import Annotated

from fastapi import APIRouter, Path, Request, status

from marcenaria_digital_api.entities.enums import EstiloMovel
from marcenaria_digital_api.routes.exception_handlers import (
    ConfiguracaoDuplicadaResponse,
    ConfiguracaoInvalidaResponse,
    ConfiguracaoNaoEncontradaResponse,
    FalhaPersistenciaResponse,
    RequisicaoInvalidaResponse,
)
from marcenaria_digital_api.routes.schemas import ConfiguracaoInput, ConfiguracaoOutput
from marcenaria_digital_api.services import ConfiguracaoService

router = APIRouter(prefix="/configuracoes", tags=["Configurações"])
estilos_router = APIRouter(prefix="/estilos-armario", tags=["Estilos de armário"])


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


@router.get(
    "",
    response_model=list[ConfiguracaoOutput],
    summary="Listar configurações ativas",
    description="Lista as configurações ativas disponíveis no catálogo JSON.",
    responses={
        500: {
            "model": FalhaPersistenciaResponse,
            "description": "Falha inesperada de leitura.",
        }
    },
)
def listar_configuracoes(request: Request) -> list[ConfiguracaoOutput]:
    """Lista as configurações ativas para o catálogo público."""
    servico: ConfiguracaoService = request.app.state.configuracao_service
    return [
        ConfiguracaoOutput.da_entidade(configuracao)
        for configuracao in servico.listar_ativas()
    ]


@router.get(
    "/{id}",
    response_model=ConfiguracaoOutput,
    summary="Consultar configuração ativa",
    description="Recupera uma configuração ativa pelo identificador.",
    responses={
        404: {
            "model": ConfiguracaoNaoEncontradaResponse,
            "description": "Configuração inexistente ou inativa.",
        },
        422: {
            "model": RequisicaoInvalidaResponse,
            "description": "Identificador inválido.",
        },
        500: {
            "model": FalhaPersistenciaResponse,
            "description": "Falha inesperada de leitura.",
        },
    },
)
def obter_configuracao(
    id: Annotated[int, Path(gt=0)], request: Request
) -> ConfiguracaoOutput:
    """Recupera uma configuração ativa do catálogo público."""
    servico: ConfiguracaoService = request.app.state.configuracao_service
    configuracao = servico.obter_ativa_por_id(id)
    return ConfiguracaoOutput.da_entidade(configuracao)


@estilos_router.get(
    "",
    response_model=list[EstiloMovel],
    summary="Listar estilos de armário ativos",
    description="Lista, sem duplicidade, estilos com configurações ativas.",
    responses={
        500: {
            "model": FalhaPersistenciaResponse,
            "description": "Falha inesperada de leitura.",
        }
    },
)
def listar_estilos_armario(request: Request) -> list[EstiloMovel]:
    """Lista os estilos que possuem configurações ativas."""
    servico: ConfiguracaoService = request.app.state.configuracao_service
    return servico.listar_estilos_ativos()
