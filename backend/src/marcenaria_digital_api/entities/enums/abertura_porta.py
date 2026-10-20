from .enum_descritivo import EnumDescritivo


class AberturaPorta(EnumDescritivo):
    """Identifica a direção de abertura de uma porta."""

    ABERTURA_VERTICAL_PARA_DIREITA = (
        "ABERTURA VERTICAL PARA DIREITA",
        "Indica que a porta possui eixo vertical e abre para a direita.",
    )
    ABERTURA_VERTICAL_PARA_ESQUERDA = (
        "ABERTURA VERTICAL PARA ESQUERDA",
        "Indica que a porta possui eixo vertical e abre para a esquerda.",
    )
    ABERTURA_HORIZONTAL_PARA_CIMA = (
        "ABERTURA HORIZONTAL PARA CIMA",
        "Indica que a porta possui eixo horizontal e abre para cima.",
    )
    ABERTURA_HORIZONTAL_PARA_BAIXO = (
        "ABERTURA HORIZONTAL PARA BAIXO",
        "Indica que a porta possui eixo horizontal e abre para baixo.",
    )
    PORTA_CORRER = (
        "PORTA CORRER",
        "Indica que a porta é do tipo correr, deslizando horizontalmente.",
    )
