from typing import Literal

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from marcenaria_digital_api.entities.exceptions import (
    ConfiguracaoDuplicadaError,
    ConfiguracaoInvalidaError,
    FalhaPersistenciaError,
)


class DetalheErroResponse(BaseModel):
    """Representa um erro de validação de campo."""

    campo: str
    mensagem: str


class ConfiguracaoInvalidaResponse(BaseModel):
    """Representa a resposta para uma configuração inválida."""

    erro: Literal["configuracao_invalida"] = "configuracao_invalida"
    detalhes: list[DetalheErroResponse]


class ConfiguracaoDuplicadaResponse(BaseModel):
    """Representa a resposta para um identificador duplicado."""

    erro: Literal["configuracao_duplicada"] = "configuracao_duplicada"
    mensagem: str


class FalhaPersistenciaResponse(BaseModel):
    """Representa uma falha interna de persistência."""

    erro: Literal["falha_persistencia"] = "falha_persistencia"
    mensagem: str


def registrar_exception_handlers(app: FastAPI) -> None:
    """Registra os tratadores de exceções da API."""

    @app.exception_handler(RequestValidationError)
    async def tratar_erro_estrutural(
        _request: Request, erro: RequestValidationError
    ) -> JSONResponse:
        """Converte erros estruturais da requisição em resposta padronizada."""
        detalhes = []
        for item in erro.errors():
            caminho = [str(parte) for parte in item["loc"] if parte != "body"]
            detalhes.append(
                {
                    "campo": ".".join(caminho) or "corpo",
                    "mensagem": _mensagem_validacao(item["type"]),
                }
            )
        return JSONResponse(
            status_code=422,
            content={"erro": "configuracao_invalida", "detalhes": detalhes},
        )

    @app.exception_handler(ConfiguracaoInvalidaError)
    async def tratar_configuracao_invalida(
        _request: Request, erro: ConfiguracaoInvalidaError
    ) -> JSONResponse:
        """Converte inconsistências de negócio em resposta HTTP 422."""
        return JSONResponse(
            status_code=422,
            content={
                "erro": "configuracao_invalida",
                "detalhes": [
                    {"campo": item.campo, "mensagem": item.mensagem}
                    for item in erro.detalhes
                ],
            },
        )

    @app.exception_handler(ConfiguracaoDuplicadaError)
    async def tratar_configuracao_duplicada(
        _request: Request, erro: ConfiguracaoDuplicadaError
    ) -> JSONResponse:
        """Converte identificadores duplicados em resposta HTTP 409."""
        return JSONResponse(
            status_code=409,
            content={"erro": "configuracao_duplicada", "mensagem": str(erro)},
        )

    @app.exception_handler(FalhaPersistenciaError)
    async def tratar_falha_persistencia(
        _request: Request, _erro: FalhaPersistenciaError
    ) -> JSONResponse:
        """Converte falhas internas de persistência em resposta segura."""
        return JSONResponse(
            status_code=500,
            content={
                "erro": "falha_persistencia",
                "mensagem": "Não foi possível persistir a configuração.",
            },
        )


def _mensagem_validacao(tipo: str) -> str:
    """Traduz um tipo de erro estrutural para uma mensagem pública."""
    mensagens = {
        "missing": "campo obrigatório",
        "greater_than": "deve ser maior que 0",
        "less_than_equal": "deve ser menor ou igual a 100",
        "too_short": "deve possuir ao menos um item",
        "enum": "valor não permitido",
        "extra_forbidden": "campo não permitido",
        "int_type": "deve ser um inteiro",
        "float_type": "deve ser um número",
        "bool_type": "deve ser verdadeiro ou falso",
        "json_invalid": "JSON inválido",
        "model_attributes_type": "deve ser um objeto JSON",
    }
    return mensagens.get(tipo, "valor inválido")
