from .enum_descritivo import EnumDescritivo


class Corte(EnumDescritivo):
    """
    Define o tipo de corte nas extremidades de cada peça.
    O tipo de corte define a forma como as peças de madeira são cortadas para a montagem do móvel.
    """

    reto = (
        "reto",
        "Indica que a extremidade da peça receberá um corte reto.",
    )
    meia_esquadria = (
        "meia esquadria",
        "Indica que a extremidade da peça receberá um corte em meia-esquadria.",
    )
