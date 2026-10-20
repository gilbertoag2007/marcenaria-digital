
from .enum_descritivo import EnumDescritivo


class Espessura(EnumDescritivo):
    """Identifica a espessura de um material."""

    mm_6 = ("6 mm", "Indica que o material possui espessura de 6 milímetros.")
    mm_15 = ("15 mm", "Indica que o material possui espessura de 15 milímetros.")
    mm_18 = ("18 mm", "Indica que o material possui espessura de 18 milímetros.")
    
