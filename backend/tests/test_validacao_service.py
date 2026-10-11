from dataclasses import replace

import pytest

from marcenaria_digital_api.entities.exceptions import ConfiguracaoInvalidaError
from marcenaria_digital_api.routes.schemas import ConfiguracaoInput
from marcenaria_digital_api.services import validar_configuracao


def test_aceita_relacoes_inversas_coerentes(payload_valido: dict) -> None:
    validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())


@pytest.mark.parametrize("quantidade", [-1, 11, True])
def test_rejeita_quantidade_de_portas_invalida_no_dominio(
    payload_valido: dict, quantidade: int | bool
) -> None:
    """Valida a faixa e o tipo da quantidade também na camada de domínio."""
    configuracao = ConfiguracaoInput.model_validate(payload_valido).para_entidade()
    detalhe_invalido = replace(
        configuracao.detalhes[0], quantidade_portas=quantidade
    )
    configuracao_invalida = replace(
        configuracao,
        detalhes=[detalhe_invalido, *configuracao.detalhes[1:]],
    )

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(configuracao_invalida)

    assert any(
        item.campo == "detalhes.0.quantidade_portas"
        for item in capturada.value.detalhes
    )


@pytest.mark.parametrize(
    ("quantidade", "abertura", "campo"),
    [
        (0, "ABERTURA VERTICAL", "abertura_porta"),
        (1, None, "abertura_porta"),
        (None, None, "quantidade_portas"),
    ],
)
def test_rejeita_combinacao_invalida_de_portas_no_compartimento(
    payload_valido: dict,
    quantidade: int | None,
    abertura: str | None,
    campo: str,
) -> None:
    """Valida a dependência entre quantidade e abertura no compartimento."""
    payload_valido["detalhes"][0]["quantidade_portas"] = quantidade
    payload_valido["detalhes"][0]["abertura_porta"] = abertura
    configuracao = ConfiguracaoInput.model_validate(payload_valido).para_entidade()

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(configuracao)

    assert any(
        item.campo == f"detalhes.0.{campo}" for item in capturada.value.detalhes
    )


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
            "quantidade_portas": 1,
            "abertura_porta": "ABERTURA VERTICAL",
        }
    )
    payload_valido["detalhes"][1]["embaixo_de_id"] = 30

    with pytest.raises(ConfiguracaoInvalidaError) as capturada:
        validar_configuracao(ConfiguracaoInput.model_validate(payload_valido).para_entidade())

    assert any("inversa" in item.mensagem for item in capturada.value.detalhes)
