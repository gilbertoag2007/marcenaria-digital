import json
from pathlib import Path

from fastapi.testclient import TestClient

from marcenaria_digital_api.main import create_app


def test_cria_configuracao_e_documenta_contrato(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 201
    assert resposta.json() == payload_valido
    openapi = cliente.get("/openapi.json").json()
    operacao = openapi["paths"]["/api/v1/configuracoes"]["post"]
    assert set(operacao["responses"]) >= {"201", "409", "422", "500"}
    propriedades = openapi["components"]["schemas"]["ConfiguracaoInput"]["properties"]
    assert {
        "altura_minima_cm",
        "altura_maxima_cm",
        "largura_minima_cm",
        "largura_maxima_cm",
        "profundidade_minima_cm",
        "profundidade_maxima_cm",
    } <= propriedades.keys()


def test_retorna_422_e_nao_grava_payload_incompleto(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))
    del payload_valido["detalhes"][0]["percentual_ocupacao_vertical"]
    original = arquivo_configuracoes.read_text(encoding="utf-8")

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "configuracao_invalida"
    assert any(
        item["campo"] == "detalhes.0.percentual_ocupacao_vertical"
        for item in resposta.json()["detalhes"]
    )
    assert arquivo_configuracoes.read_text(encoding="utf-8") == original


def test_retorna_422_e_nao_grava_sem_limite_dimensional(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))
    del payload_valido["altura_minima_cm"]
    original = arquivo_configuracoes.read_text(encoding="utf-8")

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert {
        "campo": "altura_minima_cm",
        "mensagem": "campo obrigatório",
    } in resposta.json()["detalhes"]
    assert arquivo_configuracoes.read_text(encoding="utf-8") == original


def test_retorna_422_para_intervalo_dimensional_invertido(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["largura_minima_cm"] = 200.5
    payload_valido["largura_maxima_cm"] = 100.5

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert {
        "campo": "largura_minima_cm",
        "mensagem": "deve ser menor ou igual a largura_maxima_cm",
    } in resposta.json()["detalhes"]
    assert json.loads(arquivo_configuracoes.read_text())["configuracoes"] == []


def test_retorna_422_para_relacao_ciclica_sem_gravar(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["detalhes"][1]["em_cima_de_id"] = 10
    payload_valido["detalhes"][1]["embaixo_de_id"] = None

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert any("ciclo" in item["mensagem"] for item in resposta.json()["detalhes"])
    assert json.loads(arquivo_configuracoes.read_text())["configuracoes"] == []


def test_retorna_409_para_id_duplicado(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))
    assert cliente.post("/api/v1/configuracoes", json=payload_valido).status_code == 201

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 409
    assert resposta.json()["erro"] == "configuracao_duplicada"
    assert len(json.loads(arquivo_configuracoes.read_text())["configuracoes"]) == 1


def test_retorna_500_sem_expor_detalhe_interno(tmp_path: Path, payload_valido: dict) -> None:
    caminho_inexistente = tmp_path / "nao-existe.json"
    cliente = TestClient(create_app(caminho_inexistente))

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 500
    assert resposta.json() == {
        "erro": "falha_persistencia",
        "mensagem": "Não foi possível persistir a configuração.",
    }
