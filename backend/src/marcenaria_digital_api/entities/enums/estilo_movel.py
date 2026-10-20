from .enum_descritivo import EnumDescritivo


class EstiloMovel(EnumDescritivo):
    """Identifica os estilos de móvel permitidos."""

    MULTIUSO = ("MULTIUSO", "Identifica uma configuração de armário multiuso.")
    GUARDA_ROUPA = (
        "GUARDA_ROUPA",
        "Identifica uma configuração de guarda-roupa.",
    )
    ARMARIO_AEREO = (
        "ARMARIO_AEREO",
        "Identifica uma configuração de armário aéreo.",
    )
