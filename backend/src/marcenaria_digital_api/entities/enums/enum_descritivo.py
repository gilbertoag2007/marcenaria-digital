from enum import StrEnum


class EnumDescritivo(StrEnum):
    """Fornece uma descrição de domínio para cada membro textual do enum."""

    descricao: str

    def __new__(cls, valor: str, descricao: str) -> "EnumDescritivo":
        """Cria um membro preservando seu valor textual e sua descrição."""
        membro = str.__new__(cls, valor)
        membro._value_ = valor
        membro.descricao = descricao
        return membro
