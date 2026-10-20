from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from marcenaria_digital_api.entities.configuracao.limites import Limites
from marcenaria_digital_api.entities.enums import (
    DirecaoHorizontal,
    DirecaoVertical,
    TipoMovel,
)


@dataclass(frozen=True, slots=True)
class Configuracao(ABC):
    """Define os dados comuns a qualquer configuração de móvel."""

    id: int = field(
        metadata={"description": "Identificador único da configuração."}
    )
    limites: Limites = field(
        metadata={"description": "Limites mínimos e máximos de altura, largura, profundidade permitidos pela configuração."}
    )
    ativo: bool = field(
        metadata={"description": "Indica se a configuração está disponível para uso."}
    )
    direcao_vertical: DirecaoVertical = field(
        metadata={"description": "Direção vertical dos compartimentos."}
    )
    direcao_horizontal: DirecaoHorizontal = field(
        metadata={"description": "Direção horizontal dos compartimentos."}
    )

    @property
    @abstractmethod
    def tipo(self) -> TipoMovel:
        """Informa o tipo de móvel representado pela configuração concreta."""
        raise NotImplementedError
