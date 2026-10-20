from dataclasses import fields

import pytest

from marcenaria_digital_api.entities.configuracao import (
    AcabamentoExterno,
    CompartimentoConfiguracao,
    Configuracao,
    ConfiguracaoArmario,
    Limites,
    PortaConfiguracao,
)
from marcenaria_digital_api.entities.enums import (
    AberturaPorta,
    Corte,
    DirecaoHorizontal,
    DirecaoVertical,
    Espessura,
    EstiloAcabamento,
    EstiloMovel,
    Posicao,
    TipoMovel,
)
from marcenaria_digital_api.entities.exceptions import ErroValidacao


@pytest.mark.parametrize(
    "entidade",
    [
        Configuracao,
        ConfiguracaoArmario,
        CompartimentoConfiguracao,
        PortaConfiguracao,
        Limites,
        AcabamentoExterno,
        ErroValidacao,
    ],
)
def test_todos_os_atributos_das_entidades_possuem_descricao(
    entidade: type,
) -> None:
    """Garante que todo campo das entidades documenta sua responsabilidade."""
    for atributo in fields(entidade):
        assert atributo.metadata.get("description")


@pytest.mark.parametrize(
    "enum",
    [
        AberturaPorta,
        Corte,
        DirecaoHorizontal,
        DirecaoVertical,
        Espessura,
        EstiloAcabamento,
        EstiloMovel,
        Posicao,
        TipoMovel,
    ],
)
def test_todos_os_membros_dos_enums_possuem_descricao(enum: type) -> None:
    """Garante que todo membro dos enums possui uma descrição de domínio."""
    for membro in enum:
        assert membro.descricao
