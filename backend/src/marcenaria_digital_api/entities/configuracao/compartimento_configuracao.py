from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CompartimentoConfiguracao:
    """Representa um compartimento e suas relações dentro de uma configuração."""

    id: int = field(
        metadata={"description": "Identificador único do compartimento na configuração."}
    )
    percentual_ocupacao_vertical: float = field(
        metadata={"description": "Percentual vertical ocupado pelo compartimento."}
    )
    percentual_ocupacao_horizontal: float = field(
        metadata={"description": "Percentual horizontal ocupado pelo compartimento."}
    )
    em_cima_de_id: int | None = field(
        default=None,
        metadata={
            "description": "Identificador do compartimento localizado abaixo deste compartimento."
        },
    )
    embaixo_de_id: int | None = field(
        default=None,
        metadata={
            "description": "Identificador do compartimento localizado acima deste compartimento."
        },
    )
    a_direita_de_id: int | None = field(
        default=None,
        metadata={
            "description": "Identificador do compartimento localizado à esquerda deste compartimento."
        },
    )
    a_esquerda_de_id: int | None = field(
        default=None,
        metadata={
            "description": "Identificador do compartimento localizado à direita deste compartimento."
        },
    )
