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
    schema_422 = operacao["responses"]["422"]["content"]["application/json"]["schema"]
    assert schema_422["$ref"].endswith("/ConfiguracaoInvalidaResponse")
    propriedades = openapi["components"]["schemas"]["ConfiguracaoInput"]["properties"]
    assert {
        "acabamentos",
        "limites",
        "compartimentos",
        "portas",
        "direcao_vertical",
        "direcao_horizontal",
    } <= propriedades.keys()
    assert "detalhes" not in propriedades
    propriedades_limites = openapi["components"]["schemas"]["LimitesInput"][
        "properties"
    ]
    assert {
        "altura_minima_cm",
        "altura_maxima_cm",
        "largura_minima_cm",
        "largura_maxima_cm",
        "profundidade_minima_cm",
        "profundidade_maxima_cm",
        "espessura_minima_cm",
        "espessura_maxima_cm",
    } <= propriedades_limites.keys()
    propriedades_acabamento = openapi["components"]["schemas"][
        "AcabamentoExternoInput"
    ]["properties"]
    assert {
        "id",
        "tipo_acabamento",
        "estilo_acabamento",
        "extensao_cm",
        "espessura",
        "corte_extremidade_1",
        "corte_extremidade_2",
    } <= propriedades_acabamento.keys()
    propriedades_compartimento = openapi["components"]["schemas"][
        "CompartimentoConfiguracaoInput"
    ]["properties"]
    assert "abertura_porta" not in propriedades_compartimento
    assert "quantidade_portas" not in propriedades_compartimento
    assert "tipo" not in propriedades_compartimento
    propriedades_porta = openapi["components"]["schemas"][
        "PortaConfiguracaoInput"
    ]["properties"]
    assert "abertura" in propriedades_porta
    valores_abertura = openapi["components"]["schemas"]["AberturaPorta"]["enum"]
    assert valores_abertura == [
        "ABERTURA VERTICAL PARA DIREITA",
        "ABERTURA VERTICAL PARA ESQUERDA",
        "ABERTURA HORIZONTAL PARA CIMA",
        "ABERTURA HORIZONTAL PARA BAIXO",
        "PORTA CORRER",
    ]


def test_aceita_configuracao_legada_sem_campo_acabamentos(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    """Preserva a compatibilidade com configurações anteriores ao novo campo."""
    cliente = TestClient(create_app(arquivo_configuracoes))
    del payload_valido["acabamentos"]

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 201
    assert resposta.json()["acabamentos"] == []


def test_rejeita_campo_quantidade_portas_removido(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    """Rejeita o antigo campo redundante no contrato estrito da API."""
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["compartimentos"][0]["quantidade_portas"] = 1

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert resposta.json()["detalhes"][0]["campo"] == (
        "compartimentos.0.quantidade_portas"
    )


def test_rejeita_colecao_detalhes_removida(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    """Rejeita a coleção antiga após a renomeação para compartimentos."""
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["detalhes"] = payload_valido.pop("compartimentos")

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    campos = {item["campo"] for item in resposta.json()["detalhes"]}
    assert {"compartimentos", "detalhes"} <= campos


def test_rejeita_campo_tipo_removido(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    """Rejeita o antigo discriminador no contrato estrito da API."""
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["compartimentos"][0]["tipo"] = "COMPARTIMENTO"

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert resposta.json()["detalhes"][0]["campo"] == "compartimentos.0.tipo"


def test_rejeita_campo_abertura_porta_removido(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    """Rejeita o antigo campo de porta dentro de um compartimento."""
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["compartimentos"][0]["abertura_porta"] = None

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert resposta.json()["detalhes"][0]["campo"] == (
        "compartimentos.0.abertura_porta"
    )


def test_rejeita_estilo_de_acabamento_desconhecido(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    """Rejeita valores que não pertencem ao enum de estilo de acabamento."""
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["acabamentos"][0]["estilo_acabamento"] = "EMBUTIDO"

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert resposta.json()["detalhes"][0]["campo"] == (
        "acabamentos.0.estilo_acabamento"
    )


def test_rejeita_abertura_de_porta_desconhecida(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    """Rejeita valores que não pertencem ao enum de abertura."""
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["portas"][0]["abertura"] = "ABERTURA DIAGONAL"

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert resposta.json()["detalhes"][0]["campo"] == "portas.0.abertura"
    assert json.loads(arquivo_configuracoes.read_text())["configuracoes"] == []


def test_retorna_422_e_nao_grava_payload_incompleto(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))
    del payload_valido["compartimentos"][0]["percentual_ocupacao_vertical"]
    original = arquivo_configuracoes.read_text(encoding="utf-8")

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert resposta.json()["erro"] == "configuracao_invalida"
    assert any(
        item["campo"] == "compartimentos.0.percentual_ocupacao_vertical"
        for item in resposta.json()["detalhes"]
    )
    assert arquivo_configuracoes.read_text(encoding="utf-8") == original


def test_retorna_422_e_nao_grava_sem_limite_dimensional(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))
    del payload_valido["limites"]["altura_minima_cm"]
    original = arquivo_configuracoes.read_text(encoding="utf-8")

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert {
        "campo": "limites.altura_minima_cm",
        "mensagem": "campo obrigatório",
    } in resposta.json()["detalhes"]
    assert arquivo_configuracoes.read_text(encoding="utf-8") == original


def test_retorna_422_para_intervalo_dimensional_invertido(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["limites"]["largura_minima_cm"] = 200.5
    payload_valido["limites"]["largura_maxima_cm"] = 100.5

    resposta = cliente.post("/api/v1/configuracoes", json=payload_valido)

    assert resposta.status_code == 422
    assert {
        "campo": "limites.largura_minima_cm",
        "mensagem": "deve ser menor ou igual a largura_maxima_cm",
    } in resposta.json()["detalhes"]
    assert json.loads(arquivo_configuracoes.read_text())["configuracoes"] == []


def test_retorna_422_para_relacao_ciclica_sem_gravar(
    arquivo_configuracoes: Path, payload_valido: dict
) -> None:
    cliente = TestClient(create_app(arquivo_configuracoes))
    payload_valido["compartimentos"][1]["em_cima_de_id"] = 10
    payload_valido["compartimentos"][1]["embaixo_de_id"] = None

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
