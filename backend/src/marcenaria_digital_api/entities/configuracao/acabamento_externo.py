from dataclasses import dataclass, field

from marcenaria_digital_api.entities.enums import (
    Corte,
    Espessura,
    EstiloAcabamento,
    Posicao,
)

@dataclass(frozen=True, slots=True)
class AcabamentoExterno:
    """Representa um acabamento externo do móvel."""

    id: int = field(
        metadata={"description": "Identificador único do acabamento externo."}
    )
    posicao: Posicao = field(
        metadata={"description": "Posição do acabamento externo no móvel."}
    )
    estilo_acabamento: EstiloAcabamento = field(
        metadata={"description": "Estilo visual do acabamento externo. Interno, Externo, etc."}
    )
    extensao_cm: float = field(
        metadata={
            "description": (
                "Extensão do acabamento em centímetros. Interpretada como largura "
                "ou altura conforme sua posição."
            )
        }
    )
    espessura: Espessura = field(
        metadata={"description": "Espessura do material usado no acabamento externo."}
    )
    corte_extremidade_1: Corte = field(
        metadata={
            "description": "Tipo de corte na primeira extremidade do acabamento externo.Começa de cima para baixo e da esquerda para direita, dependendo da posição do acabamento."
        }
    )
    corte_extremidade_2: Corte = field(
        metadata={
            "description": "Tipo de corte na segunda extremidade do acabamento externo."
        }
    )
