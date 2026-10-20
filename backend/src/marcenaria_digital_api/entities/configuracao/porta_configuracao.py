from dataclasses import dataclass, field

from marcenaria_digital_api.entities.enums import AberturaPorta


@dataclass(frozen=True, slots=True)
class PortaConfiguracao:
    """Representa uma porta e suas relações dentro da configuração."""

    id: int = field(
        metadata={"description": "Identificador único da porta na configuração."}
    )
    percentual_ocupacao_vertical: float = field(
        metadata={"description": "Percentual vertical ocupado pela porta."}
    )
    percentual_ocupacao_horizontal: float = field(
        metadata={"description": "Percentual horizontal ocupado pela porta."}
    )
    abertura: AberturaPorta = field(
        metadata={"description": "Direção de abertura da porta."}
    )
    em_cima_de_id: int | None = field(
        default=None,
        metadata={"description": "Identificador do elemento abaixo desta porta."},
    )
    embaixo_de_id: int | None = field(
        default=None,
        metadata={"description": "Identificador do elemento acima desta porta."},
    )
    a_direita_de_id: int | None = field(
        default=None,
        metadata={"description": "Identificador do elemento à esquerda desta porta."},
    )
    a_esquerda_de_id: int | None = field(
        default=None,
        metadata={"description": "Identificador do elemento à direita desta porta."},
    )
