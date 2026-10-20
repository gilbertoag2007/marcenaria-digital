from .enum_descritivo import EnumDescritivo


class DirecaoVertical(EnumDescritivo):
    """
    Define a direção que os compartimentos serão organizados dentro do móvel.
    """

    cima_baixo = (
        "cima_baixo",
        "Indica que os compartimentos serão organizados de cima para baixo.",
    )

    baixo_cima = (
        "baixo_cima",
        "Indica que os compartimentos serão organizados de baixo para cima.",
    )

 