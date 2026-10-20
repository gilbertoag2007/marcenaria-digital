from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Limites:
    """Agrupa os limites dimensionais permitidos para uma configuração."""

    altura_minima_cm: Decimal = field(
        metadata={"description": "Altura mínima permitida, em centímetros."}
    )
    altura_maxima_cm: Decimal = field(
        metadata={"description": "Altura máxima permitida, em centímetros."}
    )
    largura_minima_cm: Decimal = field(
        metadata={"description": "Largura mínima permitida, em centímetros."}
    )
    largura_maxima_cm: Decimal = field(
        metadata={"description": "Largura máxima permitida, em centímetros."}
    )
    profundidade_minima_cm: Decimal = field(
        metadata={"description": "Profundidade mínima permitida, em centímetros."}
    )
    profundidade_maxima_cm: Decimal = field(
        metadata={"description": "Profundidade máxima permitida, em centímetros."}
    )
    espessura_minima_cm: Decimal = field(
        metadata={"description": "Espessura mínima permitida, em centímetros."}
    )
    espessura_maxima_cm: Decimal = field(
        metadata={"description": "Espessura máxima permitida, em centímetros."}
    )
