import pytest

from marcenaria_digital_api.entities.exceptions import ConfiguracaoInvalidaError
from marcenaria_digital_api.routes.schemas import ConfiguracaoInput
from marcenaria_digital_api.services import validar_configuracao


def test_aceita_relacoes_inversas_coerentes(payload_valido: dict) -> None:
    validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())


@pytest.mark.parametrize(
    ("campo_minimo", "campo_maximo"),
    [
        ("altura_minima_cm", "altura_maxima_cm"),
        ("largura_minima_cm", "largura_maxima_cm"),
        ("profundidade_minima_cm", "profundidade_maxima_cm"),
    ],
)
def test_rejeita_limite_minimo_maior_que_maximo(
    payload_valido: dict, campo_minimo: str, campo_maximo: str
) -> None:
    payload_valido[campo_minimo] = 100.5
    payload_valido[campo_maximo] = 99.5

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert any(
        item.campo == campo_minimo and campo_maximo in item.mensagem
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
    payload_valido["detalhes"][0].update(alteracao)

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert mensagem in " ".join(item.mensagem for item in capturada.value.detalhes)


def test_rejeita_ciclo_vertical(payload_valido: dict) -> None:
    payload_valido["detalhes"][0]["em_cima_de_id"] = 20
    payload_valido["detalhes"][1]["em_cima_de_id"] = 10
    payload_valido["detalhes"][1]["embaixo_de_id"] = None

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert any("ciclo" in item.mensagem for item in capturada.value.detalhes)


def test_rejeita_relacao_inversa_incoerente(payload_valido: dict) -> None:
    payload_valido["detalhes"].append(
        {
            "id": 30,
            "tipo": "COMPARTIMENTO",
            "percentual_ocupacao_vertical": 10.0,
            "percentual_ocupacao_horizontal": 10.0,
        }
    )
    payload_valido["detalhes"][1]["embaixo_de_id"] = 30

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert any("inversa" in item.mensagem for item in capturada.value.detalhes)
