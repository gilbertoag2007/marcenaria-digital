from .enum_descritivo import EnumDescritivo


class DirecaoHorizontal(EnumDescritivo):
    """
    Define a direção que os compartimentos serão organizados horizontalmente dentro do móvel.
    """
    direita_esquerda = (
        "direita_esquerda",
        "Indica que os compartimentos serão organizados da direita para a esquerda.",
    )
    
    esquerda_direita = (
        "esquerda_direita",
        "Indica que os compartimentos serão organizados da esquerda para a direita.",
    )

 