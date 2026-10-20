from .enum_descritivo import EnumDescritivo


class Posicao(EnumDescritivo):
    """Define a posição da peça em relação ao móvel."""

    SUPERIOR = (
        "SUPERIOR",
        "Indica que a peça ou compartimento será posicionado na parte superior do móvel.",
    )
    INFERIOR = (
        "INFERIOR",
        "Indica que a peça ou compartimento será posicionado na parte inferior do móvel.",
    )
    DIREITA = (
        "DIREITA",
        "Indica que a peça ou compartimento será posicionado na parte direita do móvel.",
    )
    ESQUERDA = (
        "ESQUERDA",
        "Indica que a peça ou compartimento será posicionado na parte esquerda do móvel.",
    )


