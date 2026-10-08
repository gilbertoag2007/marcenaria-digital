from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


CAMINHO_CONFIGURACOES_PADRAO = (
    Path(__file__).parent / "repositories" / "json" / "configuracoes.json"
)


class Settings(BaseSettings):
    """Centraliza as configurações de ambiente da aplicação."""

    model_config = SettingsConfigDict(env_prefix="MARCENARIA_", extra="ignore")

    configuracoes_json_path: Path = CAMINHO_CONFIGURACOES_PADRAO
