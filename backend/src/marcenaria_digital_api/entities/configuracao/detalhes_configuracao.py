from dataclasses import dataclass

from marcenaria_digital_api.entities.enums import TipoConfiguracao


@dataclass(frozen=True, slots=True)
class DetalheConfiguracao:
    """Representa um item e suas relações dentro de uma configuração."""

    id: int
    tipo: TipoConfiguracao
    percentual_ocupacao_vertical: float
    percentual_ocupacao_horizontal: float
    em_cima_de_id: int | None = None
    embaixo_de_id: int | None = None
    a_direita_de_id: int | None = None
    a_esquerda_de_id: int | None = None
