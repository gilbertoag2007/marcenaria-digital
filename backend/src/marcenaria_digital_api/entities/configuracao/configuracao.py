from dataclasses import dataclass
from decimal import Decimal

from marcenaria_digital_api.entities.configuracao.detalhes_configuracao import (
    DetalheConfiguracao,
)
from marcenaria_digital_api.entities.enums import EstiloMovel, TipoMovel


@dataclass(frozen=True, slots=True)
class Configuracao:
    """Representa uma configuração reutilizável de móvel."""

    id: int
    tipo: TipoMovel
    estilo: EstiloMovel
    altura_minima_cm: Decimal
    altura_maxima_cm: Decimal
    largura_minima_cm: Decimal
    largura_maxima_cm: Decimal
    profundidade_minima_cm: Decimal
    profundidade_maxima_cm: Decimal
    ativo: bool
    detalhes: list[DetalheConfiguracao]
