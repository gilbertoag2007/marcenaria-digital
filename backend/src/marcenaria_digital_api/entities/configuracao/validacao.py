import math
from decimal import Decimal, InvalidOperation

from marcenaria_digital_api.entities.configuracao import Configuracao
from marcenaria_digital_api.entities.enums import EstiloMovel, TipoConfiguracao, TipoMovel
from marcenaria_digital_api.entities.exceptions import (
    ConfiguracaoInvalidaError,
    ErroValidacao,
)


def validar_configuracao(configuracao: Configuracao) -> None:
    """Valida regras intrínsecas e relações espaciais de uma configuração."""
    erros: list[ErroValidacao] = []

    if type(configuracao.id) is not int or configuracao.id <= 0:
        erros.append(ErroValidacao("id", "deve ser um inteiro positivo"))
    if not isinstance(configuracao.tipo, TipoMovel):
        erros.append(ErroValidacao("tipo", "tipo de móvel não permitido"))
    if not isinstance(configuracao.estilo, EstiloMovel):
        erros.append(ErroValidacao("estilo", "estilo de móvel não permitido"))
    _validar_limites_dimensionais(configuracao, erros)
    if type(configuracao.ativo) is not bool:
        erros.append(ErroValidacao("ativo", "deve ser verdadeiro ou falso"))
    if not configuracao.detalhes:
        erros.append(ErroValidacao("detalhes", "deve possuir ao menos um item"))

    ids: set[int] = set()
    duplicados: set[int] = set()
    for indice, detalhe in enumerate(configuracao.detalhes):
        prefixo = f"detalhes.{indice}"
        if type(detalhe.id) is not int or detalhe.id <= 0:
            erros.append(ErroValidacao(f"{prefixo}.id", "deve ser um inteiro positivo"))
        if not isinstance(detalhe.tipo, TipoConfiguracao):
            erros.append(ErroValidacao(f"{prefixo}.tipo", "tipo de configuração não permitido"))
        if detalhe.id in ids:
            duplicados.add(detalhe.id)
        ids.add(detalhe.id)
        for campo, valor in (
            ("percentual_ocupacao_vertical", detalhe.percentual_ocupacao_vertical),
            ("percentual_ocupacao_horizontal", detalhe.percentual_ocupacao_horizontal),
        ):
            if (
                isinstance(valor, bool)
                or not isinstance(valor, (int, float))
                or not math.isfinite(valor)
                or not 0 < valor <= 100
            ):
                erros.append(
                    ErroValidacao(
                        f"{prefixo}.{campo}", "deve ser maior que 0 e menor ou igual a 100"
                    )
                )

    for detalhe_id in sorted(duplicados):
        erros.append(
            ErroValidacao("detalhes.id", f"o id {detalhe_id} está duplicado na configuração")
        )

    por_id = {detalhe.id: detalhe for detalhe in configuracao.detalhes}
    referencias = (
        "em_cima_de_id",
        "embaixo_de_id",
        "a_direita_de_id",
        "a_esquerda_de_id",
    )
    for indice, detalhe in enumerate(configuracao.detalhes):
        prefixo = f"detalhes.{indice}"
        for campo in referencias:
            referencia = getattr(detalhe, campo)
            if referencia is None:
                continue
            if type(referencia) is not int or referencia <= 0:
                erros.append(ErroValidacao(f"{prefixo}.{campo}", "deve ser um inteiro positivo"))
            elif referencia == detalhe.id:
                erros.append(ErroValidacao(f"{prefixo}.{campo}", "não pode referenciar o próprio detalhe"))
            elif referencia not in por_id:
                erros.append(
                    ErroValidacao(
                        f"{prefixo}.{campo}",
                        f"referencia o detalhe inexistente de id {referencia}",
                    )
                )

        if (
            detalhe.em_cima_de_id is not None
            and detalhe.em_cima_de_id == detalhe.embaixo_de_id
        ):
            erros.append(
                ErroValidacao(prefixo, "não pode estar acima e abaixo do mesmo detalhe")
            )
        if (
            detalhe.a_direita_de_id is not None
            and detalhe.a_direita_de_id == detalhe.a_esquerda_de_id
        ):
            erros.append(
                ErroValidacao(prefixo, "não pode estar à direita e à esquerda do mesmo detalhe")
            )

    if not duplicados:
        erros.extend(_validar_relacoes_inversas(configuracao, por_id))
        erros.extend(_validar_ciclos(configuracao, ids))

    if erros:
        raise ConfiguracaoInvalidaError(erros)


def _validar_limites_dimensionais(
    configuracao: Configuracao, erros: list[ErroValidacao]
) -> None:
    """Valida valores e intervalos dimensionais permitidos pela configuração."""
    dimensoes = (
        ("altura", configuracao.altura_minima_cm, configuracao.altura_maxima_cm),
        ("largura", configuracao.largura_minima_cm, configuracao.largura_maxima_cm),
        (
            "profundidade",
            configuracao.profundidade_minima_cm,
            configuracao.profundidade_maxima_cm,
        ),
    )
    for dimensao, minimo, maximo in dimensoes:
        valores_validos = True
        for limite, valor in (("minima", minimo), ("maxima", maximo)):
            campo = f"{dimensao}_{limite}_cm"
            try:
                valido = (
                    isinstance(valor, Decimal)
                    and valor.is_finite()
                    and valor > Decimal("0")
                )
            except InvalidOperation:
                valido = False
            if not valido:
                valores_validos = False
                erros.append(
                    ErroValidacao(campo, "deve ser um número decimal positivo")
                )
        if valores_validos and minimo > maximo:
            erros.append(
                ErroValidacao(
                    f"{dimensao}_minima_cm",
                    f"deve ser menor ou igual a {dimensao}_maxima_cm",
                )
            )


def _validar_relacoes_inversas(
    configuracao: Configuracao, por_id: dict[int, object]
) -> list[ErroValidacao]:
    erros: list[ErroValidacao] = []
    pares = (
        ("em_cima_de_id", "embaixo_de_id"),
        ("embaixo_de_id", "em_cima_de_id"),
        ("a_direita_de_id", "a_esquerda_de_id"),
        ("a_esquerda_de_id", "a_direita_de_id"),
    )
    for indice, detalhe in enumerate(configuracao.detalhes):
        for campo, campo_inverso in pares:
            referencia = getattr(detalhe, campo)
            referenciado = por_id.get(referencia)
            if referenciado is None:
                continue
            inversa = getattr(referenciado, campo_inverso)
            if inversa is not None and inversa != detalhe.id:
                erros.append(
                    ErroValidacao(
                        f"detalhes.{indice}.{campo}",
                        f"a relação inversa {campo_inverso} do detalhe {referencia} é incoerente",
                    )
                )
    return erros


def _validar_ciclos(configuracao: Configuracao, ids: set[int]) -> list[ErroValidacao]:
    vertical = {detalhe_id: set() for detalhe_id in ids}
    horizontal = {detalhe_id: set() for detalhe_id in ids}
    for detalhe in configuracao.detalhes:
        if detalhe.em_cima_de_id in ids:
            vertical[detalhe.id].add(detalhe.em_cima_de_id)
        if detalhe.embaixo_de_id in ids:
            vertical[detalhe.embaixo_de_id].add(detalhe.id)
        if detalhe.a_direita_de_id in ids:
            horizontal[detalhe.a_direita_de_id].add(detalhe.id)
        if detalhe.a_esquerda_de_id in ids:
            horizontal[detalhe.id].add(detalhe.a_esquerda_de_id)

    erros: list[ErroValidacao] = []
    if _possui_ciclo(vertical):
        erros.append(ErroValidacao("detalhes", "as relações do eixo vertical formam um ciclo"))
    if _possui_ciclo(horizontal):
        erros.append(ErroValidacao("detalhes", "as relações do eixo horizontal formam um ciclo"))
    return erros


def _possui_ciclo(grafo: dict[int, set[int]]) -> bool:
    visitados: set[int] = set()
    em_visita: set[int] = set()

    def visitar(no: int) -> bool:
        if no in em_visita:
            return True
        if no in visitados:
            return False
        em_visita.add(no)
        if any(visitar(vizinho) for vizinho in grafo[no]):
            return True
        em_visita.remove(no)
        visitados.add(no)
        return False

    return any(visitar(no) for no in grafo)
