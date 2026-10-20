import pytest
from pydantic import ValidationError

from marcenaria_digital_api.entities.exceptions import ConfiguracaoInvalidaError
from marcenaria_digital_api.routes.schemas import ConfiguracaoInput
from marcenaria_digital_api.services import validar_configuracao


def test_aceita_relacoes_inversas_coerentes(payload_valido: dict) -> None:
    validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())


def test_rejeita_ids_de_acabamento_duplicados(payload_valido: dict) -> None:
    """Garante a identidade única dos acabamentos dentro da configuração."""
    payload_valido["acabamentos"][1]["id"] = 1
    configuracao = ConfiguracaoInput.model_validate(payload_valido).para_entidade()

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(configuracao)

    assert any(
        item.campo == "acabamentos.id" for item in capturada.value.detalhes
    )


@pytest.mark.parametrize(
    ("campo_minimo", "campo_maximo"),
    [
        ("altura_minima_cm", "altura_maxima_cm"),
        ("largura_minima_cm", "largura_maxima_cm"),
        ("profundidade_minima_cm", "profundidade_maxima_cm"),
        ("espessura_minima_cm", "espessura_maxima_cm"),
    ],
)
def test_rejeita_limite_minimo_maior_que_maximo(
    payload_valido: dict, campo_minimo: str, campo_maximo: str
) -> None:
    payload_valido["limites"][campo_minimo] = 100.5
    payload_valido["limites"][campo_maximo] = 99.5

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert any(
        item.campo == f"limites.{campo_minimo}" and campo_maximo in item.mensagem
        for item in capturada.value.detalhes
    )


@pytest.mark.parametrize(
    ("alteracao", "mensagem"),
    [
        ({"em_cima_de_id": 999}, "inexistente"),
        ({"em_cima_de_id": 10}, "próprio"),
        ({"em_cima_de_id": 20, "embaixo_de_id": 20}, "acima e abaixo"),
    ],
)
def test_rejeita_referencia_espacial_invalida(
    payload_valido: dict, alteracao: dict, mensagem: str
) -> None:
    payload_valido["compartimentos"][0].update(alteracao)

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert mensagem in " ".join(item.mensagem for item in capturada.value.detalhes)


def test_rejeita_ciclo_vertical(payload_valido: dict) -> None:
    payload_valido["compartimentos"][0]["em_cima_de_id"] = 20
    payload_valido["compartimentos"][1]["em_cima_de_id"] = 10
    payload_valido["compartimentos"][1]["embaixo_de_id"] = None

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert any("ciclo" in item.mensagem for item in capturada.value.detalhes)


def test_rejeita_posicao_de_acabamento_invalida(payload_valido: dict) -> None:
    """Garante que o acabamento só aceita posições do domínio."""
    payload_valido["acabamentos"][0]["tipo_acabamento"] = "ACABAMENTO SUPERIOR"

    with pytest.raises(ValidationError):
        ConfiguracaoInput.model_validate(payload_valido)


def test_rejeita_relacao_inversa_incoerente(payload_valido: dict) -> None:
    payload_valido["compartimentos"].append(
        {
            "id": 30,
            "percentual_ocupacao_vertical": 10.0,
            "percentual_ocupacao_horizontal": 10.0,
        }
    )
    payload_valido["compartimentos"][1]["embaixo_de_id"] = 30

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert any("inversa" in item.mensagem for item in capturada.value.detalhes)
