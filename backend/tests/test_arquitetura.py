from pathlib import Path

import pytest


RAIZ_PACOTE = (
    Path(__file__).parents[1] / "src" / "marcenaria_digital_api"
)


def _codigo_python(camada: str) -> str:
    """Reúne o código Python de uma camada para verificar dependências."""
    return "\n".join(
        arquivo.read_text(encoding="utf-8")
        for arquivo in (RAIZ_PACOTE / camada).rglob("*.py")
    )


@pytest.mark.parametrize(
    "diretorio_antigo",
    ["application", "domain", "infrastructure", "presentation"],
)
def test_nao_mantem_diretorios_da_arquitetura_anterior(
    diretorio_antigo: str,
) -> None:
    """Garante que a estrutura antiga não permaneça no pacote."""
    assert not (RAIZ_PACOTE / diretorio_antigo).exists()


def test_respeita_dependencias_entre_camadas() -> None:
    """Garante que as camadas não importem dependências proibidas."""
    codigo_entidades = _codigo_python("entities")
    codigo_repositorios = _codigo_python("repositories")
    codigo_servicos = _codigo_python("services")
    codigo_rotas = _codigo_python("routes")

    assert "marcenaria_digital_api.services" not in codigo_entidades
    assert "marcenaria_digital_api.repositories" not in codigo_entidades
    assert "marcenaria_digital_api.routes" not in codigo_entidades
    assert "marcenaria_digital_api.services" not in codigo_repositorios
    assert "marcenaria_digital_api.routes" not in codigo_repositorios
    assert "marcenaria_digital_api.routes" not in codigo_servicos
    assert "marcenaria_digital_api.repositories" not in codigo_rotas

