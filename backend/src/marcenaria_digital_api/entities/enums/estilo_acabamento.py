from .enum_descritivo import EnumDescritivo


class EstiloAcabamento(EnumDescritivo):
    """Define o estilo visual do acabamento externo."""

    INTERNO = (
        "INTERNO",
        "Indica que o acabamento será posicionado internamente em relação às laterais do móvel.",
    )
    EXTERNO = (
        "EXTERNO",
        "Indica que o acabamento será posicionado externamente em relação às laterais do móvel.",
    )
