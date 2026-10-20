from dataclasses import dataclass, field

from marcenaria_digital_api.entities.configuracao.acabamento_externo import (
    AcabamentoExterno,
)
from marcenaria_digital_api.entities.configuracao.compartimento_configuracao import (
    CompartimentoConfiguracao,
)
from marcenaria_digital_api.entities.configuracao.configuracao import Configuracao
from marcenaria_digital_api.entities.configuracao.porta_configuracao import (
    PortaConfiguracao,
)
from marcenaria_digital_api.entities.enums import EstiloMovel, TipoMovel


@dataclass(frozen=True, slots=True)
class ConfiguracaoArmario(Configuracao):
    """Representa uma configuração concreta de armário."""

    estilo_armario: EstiloMovel = field(
        metadata={"description": "Estilo do armário configurado."}
    )
    compartimentos: list[CompartimentoConfiguracao] = field(
        metadata={"description": "Lista de compartimentos que compõem o armário."}
    )
    acabamentos: list[AcabamentoExterno] = field(
        default_factory=list,
        metadata={"description": "Lista de acabamentos externos associados ao armário."},
    )
    portas: list[PortaConfiguracao] = field(
        default_factory=list,
        metadata={"description": "Lista de portas associadas ao armário."},
    )

    @property
    def tipo(self) -> TipoMovel:
        """Identifica a configuração concreta como configuração de armário."""
        return TipoMovel.ARMARIO
