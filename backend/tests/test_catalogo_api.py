import copy
import json
from pathlib import Path

from fastapi.testclient import TestClient

from marcenaria_digital_api.main import create_app


def _gravar_catalogo(
    arquivo_configuracoes: Path, payload_valido: dict
) -> list[dict]:
    """Grava configurações ativas e inativas para os testes do catálogo."""
    configuracoes: list[dict] = []
    for configuracao_id, estilo, ativo in (
        (3, "GUARDA_ROUPA", True),
        (1, "MULTIUSO", False),
        (2, "GUARDA_ROUPA", True),
        (4, "ARMARIO_AEREO", True),
    ):
        configuracao = copy.deepcopy(payload_valido)
        configuracao.update(
            {"id": configuracao_id, "estilo": estilo, "ativo": ativo}
        )
        configuracoes.append(configuracao)
    arquivo_configuracoes.write_text(
        json.dumps(
            {"versao": 1, "configuracoes": configuracoes},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return configuracoes


def test_lista_somente_configuracoes_ativas_na_ordem_do_json(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    configuracoes = _gravar_catalogo(arquivo_configuracoes, payload_valido)
    cliente = TestClient(create_app(arquivo_configuracoes))

    resposta = cliente.get("/api/v1/configuracoes")

    assert resposta.status_code == 200
    assert resposta.json() == [
        configuracoes[0],
        configuracoes[2],
        configuracoes[3],
    ]


def test_lista_vazia_quando_nao_ha_configuracoes_ativas(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    payload_valido["ativo"] = False
    arquivo_configuracoes.write_text(
        json.dumps({"versao": 1, "configuracoes": [payload_valido]}),
        encoding="utf-8",
    )
    cliente = TestClient(create_app(arquivo_configuracoes))

    resposta = cliente.get("/api/v1/configuracoes")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_recupera_configuracao_ativa_por_id(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    configuracoes = _gravar_catalogo(arquivo_configuracoes, payload_valido)
    cliente = TestClient(create_app(arquivo_configuracoes))

    resposta = cliente.get("/api/v1/configuracoes/3")

    assert resposta.status_code == 200
    assert resposta.json() == configuracoes[0]


def test_retorna_404_para_configuracao_inexistente_ou_inativa(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    _gravar_catalogo(arquivo_configuracoes, payload_valido)
    cliente = TestClient(create_app(arquivo_configuracoes))

    for configuracao_id in (1, 999):
        resposta = cliente.get(f"/api/v1/configuracoes/{configuracao_id}")
        assert resposta.status_code == 404
        assert resposta.json()["erro"] == "configuracao_nao_encontrada"


def test_retorna_422_padronizado_para_id_invalido(
    arquivo_configuracoes: Path,
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))

    resposta = cliente.get("/api/v1/configuracoes/0")

    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "requisicao_invalida"
    assert resposta.json()["detalhes"][0]["campo"] == "path.id"


def test_lista_estilos_ativos_sem_duplicidade(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    _gravar_catalogo(arquivo_configuracoes, payload_valido)
    cliente = TestClient(create_app(arquivo_configuracoes))

    resposta = cliente.get("/api/v1/estilos-armario")

    assert resposta.status_code == 200
    assert resposta.json() == ["GUARDA_ROUPA", "ARMARIO_AEREO"]


def test_consulta_retorna_500_sem_expor_falha_interna(tmp_path: Path) -> None:
    arquivo_invalido = tmp_path / "configuracoes.json"
    arquivo_invalido.write_text("não é JSON", encoding="utf-8")
    cliente = TestClient(create_app(arquivo_invalido))

    resposta = cliente.get("/api/v1/configuracoes")

    assert resposta.status_code == 500
    assert resposta.json() == {
        "erro": "falha_persistencia",
        "mensagem": "Não foi possível persistir a configuração.",
    }
    assert str(arquivo_invalido) not in resposta.text


def test_documenta_endpoints_da_fase_2(
    arquivo_configuracoes: Path,
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))

    caminhos = cliente.get("/openapi.json").json()["paths"]

    assert "get" in caminhos["/api/v1/configuracoes"]
    assert "get" in caminhos["/api/v1/configuracoes/{id}"]
    assert "get" in caminhos["/api/v1/estilos-armario"]
    resposta_422 = caminhos["/api/v1/configuracoes/{id}"]["get"][
        "responses"
    ]["422"]
    assert resposta_422["content"]["application/json"]["schema"]["$ref"].endswith(
        "/RequisicaoInvalidaResponse"
    )


def test_permite_consulta_do_frontend_vite(
    arquivo_configuracoes: Path,
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))

    resposta = cliente.options(
        "/api/v1/configuracoes",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert resposta.status_code == 200
    assert resposta.headers["access-control-allow-origin"] == "http://localhost:5173"
