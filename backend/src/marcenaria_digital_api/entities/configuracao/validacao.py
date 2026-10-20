import math
from decimal import Decimal, InvalidOperation

from marcenaria_digital_api.entities.configuracao import (
    AcabamentoExterno,
    CompartimentoConfiguracao,
    Configuracao,
    ConfiguracaoArmario,
    Limites,
    PortaConfiguracao,
)
from marcenaria_digital_api.entities.enums import (
    AberturaPorta,
    Corte,
    DirecaoHorizontal,
    DirecaoVertical,
    Espessura,
    EstiloAcabamento,
    EstiloMovel,
    Posicao,
    TipoMovel,
)
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
    _validar_limites_dimensionais(configuracao, erros)
    if type(configuracao.ativo) is not bool:
        erros.append(ErroValidacao("ativo", "deve ser verdadeiro ou falso"))
    if not isinstance(configuracao.direcao_vertical, DirecaoVertical):
        erros.append(
            ErroValidacao("direcao_vertical", "direção vertical não permitida")
        )
    if not isinstance(configuracao.direcao_horizontal, DirecaoHorizontal):
        erros.append(
            ErroValidacao("direcao_horizontal", "direção horizontal não permitida")
        )
    if isinstance(configuracao, ConfiguracaoArmario):
        _validar_configuracao_armario(configuracao, erros)
    else:
        erros.append(ErroValidacao("tipo", "configuração concreta não suportada"))

    if erros:
        raise ConfiguracaoInvalidaError(erros)


def _validar_configuracao_armario(
    configuracao: ConfiguracaoArmario, erros: list[ErroValidacao]
) -> None:
    """Valida os atributos específicos de uma configuração de armário."""
    if not isinstance(configuracao.estilo_armario, EstiloMovel):
        erros.append(
            ErroValidacao("estilo_armario", "estilo de armário não permitido")
        )
    _validar_acabamentos(configuracao.acabamentos, erros)
    if not configuracao.compartimentos:
        erros.append(ErroValidacao("compartimentos", "deve possuir ao menos um item"))
    _validar_elementos_espaciais(
        configuracao.compartimentos,
        "compartimentos",
        CompartimentoConfiguracao,
        erros,
    )
    _validar_elementos_espaciais(
        configuracao.portas, "portas", PortaConfiguracao, erros
    )

def _validar_elementos_espaciais(
    elementos: list[object],
    raiz: str,
    classe_esperada: type,
    erros: list[ErroValidacao],
) -> None:
    """Valida identidade, ocupação e relações de elementos espaciais."""
    if not isinstance(elementos, list):
        erros.append(ErroValidacao(raiz, "deve ser uma lista"))
        return

    ids: set[int] = set()
    duplicados: set[int] = set()
    elementos_validos: list[object] = []
    for indice, elemento in enumerate(elementos):
        prefixo = f"{raiz}.{indice}"
        if not isinstance(elemento, classe_esperada):
            erros.append(ErroValidacao(prefixo, "possui tipo inválido"))
            continue
        elementos_validos.append(elemento)
        if type(elemento.id) is not int or elemento.id <= 0:
            erros.append(ErroValidacao(f"{prefixo}.id", "deve ser um inteiro positivo"))
        if isinstance(elemento, PortaConfiguracao) and not isinstance(
            elemento.abertura, AberturaPorta
        ):
            erros.append(
                ErroValidacao(f"{prefixo}.abertura", "deve ser uma abertura válida")
            )
        if elemento.id in ids:
            duplicados.add(elemento.id)
        ids.add(elemento.id)
        for campo, valor in (
            ("percentual_ocupacao_vertical", elemento.percentual_ocupacao_vertical),
            ("percentual_ocupacao_horizontal", elemento.percentual_ocupacao_horizontal),
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

    for elemento_id in sorted(duplicados):
        erros.append(
            ErroValidacao(
                f"{raiz}.id",
                f"o id {elemento_id} está duplicado na configuração",
            )
        )

    por_id = {elemento.id: elemento for elemento in elementos_validos}
    referencias = (
        "em_cima_de_id",
        "embaixo_de_id",
        "a_direita_de_id",
        "a_esquerda_de_id",
    )
    for indice, elemento in enumerate(elementos_validos):
        prefixo = f"{raiz}.{indice}"
        for campo in referencias:
            referencia = getattr(elemento, campo)
            if referencia is None:
                continue
            if type(referencia) is not int or referencia <= 0:
                erros.append(ErroValidacao(f"{prefixo}.{campo}", "deve ser um inteiro positivo"))
            elif referencia == elemento.id:
                erros.append(ErroValidacao(f"{prefixo}.{campo}", "não pode referenciar o próprio elemento"))
            elif referencia not in por_id:
                erros.append(
                    ErroValidacao(
                        f"{prefixo}.{campo}",
                        f"referencia o elemento inexistente de id {referencia}",
                    )
                )

        if (
            elemento.em_cima_de_id is not None
            and elemento.em_cima_de_id == elemento.embaixo_de_id
        ):
            erros.append(
                ErroValidacao(prefixo, "não pode estar acima e abaixo do mesmo elemento")
            )
        if (
            elemento.a_direita_de_id is not None
            and elemento.a_direita_de_id == elemento.a_esquerda_de_id
        ):
            erros.append(
                ErroValidacao(prefixo, "não pode estar à direita e à esquerda do mesmo elemento")
            )

    if not duplicados:
        erros.extend(_validar_relacoes_inversas(elementos_validos, raiz, por_id))
        erros.extend(_validar_ciclos(elementos_validos, raiz, ids))


def _validar_acabamentos(
    acabamentos: list[AcabamentoExterno], erros: list[ErroValidacao]
) -> None:
    """Valida os acabamentos associados à configuração."""
    if not isinstance(acabamentos, list):
        erros.append(ErroValidacao("acabamentos", "deve ser uma lista"))
        return

    ids: set[int] = set()
    duplicados: set[int] = set()
    for indice, acabamento in enumerate(acabamentos):
        prefixo = f"acabamentos.{indice}"
        if not isinstance(acabamento, AcabamentoExterno):
            erros.append(ErroValidacao(prefixo, "deve ser um acabamento externo"))
            continue
        if type(acabamento.id) is not int or acabamento.id <= 0:
            erros.append(ErroValidacao(f"{prefixo}.id", "deve ser um inteiro positivo"))
        if acabamento.id in ids:
            duplicados.add(acabamento.id)
        ids.add(acabamento.id)
        if not isinstance(acabamento.posicao, Posicao):
            erros.append(
                ErroValidacao(
                    f"{prefixo}.posicao", "posição de acabamento não permitida"
                )
            )
        if not isinstance(acabamento.estilo_acabamento, EstiloAcabamento):
            erros.append(
                ErroValidacao(
                    f"{prefixo}.estilo_acabamento", "estilo de acabamento não permitido"
                )
            )
        if (
            isinstance(acabamento.extensao_cm, bool)
            or not isinstance(acabamento.extensao_cm, (int, float))
            or not math.isfinite(acabamento.extensao_cm)
            or acabamento.extensao_cm <= 0
        ):
            erros.append(
                ErroValidacao(
                    f"{prefixo}.extensao_cm", "deve ser um número positivo"
                )
            )
        if not isinstance(acabamento.espessura, Espessura):
            erros.append(
                ErroValidacao(f"{prefixo}.espessura", "espessura não permitida")
            )
        if not isinstance(acabamento.corte_extremidade_1, Corte):
            erros.append(
                ErroValidacao(
                    f"{prefixo}.corte_extremidade_1", "tipo de corte não permitido"
                )
            )
        if not isinstance(acabamento.corte_extremidade_2, Corte):
            erros.append(
                ErroValidacao(
                    f"{prefixo}.corte_extremidade_2", "tipo de corte não permitido"
                )
            )

    for acabamento_id in sorted(duplicados):
        erros.append(
            ErroValidacao(
                "acabamentos.id",
                f"o id {acabamento_id} está duplicado na configuração",
            )
        )


def _validar_limites_dimensionais(
    configuracao: Configuracao, erros: list[ErroValidacao]
) -> None:
    """Valida valores e intervalos dimensionais permitidos pela configuração."""
    if not isinstance(configuracao.limites, Limites):
        erros.append(ErroValidacao("limites", "deve ser um conjunto de limites"))
        return

    limites = configuracao.limites
    dimensoes = (
        ("altura", limites.altura_minima_cm, limites.altura_maxima_cm),
        ("largura", limites.largura_minima_cm, limites.largura_maxima_cm),
        (
            "profundidade",
            limites.profundidade_minima_cm,
            limites.profundidade_maxima_cm,
        ),
        ("espessura", limites.espessura_minima_cm, limites.espessura_maxima_cm),
    )
    for dimensao, minimo, maximo in dimensoes:
        valores_validos = True
        for limite, valor in (("minima", minimo), ("maxima", maximo)):
            campo = f"limites.{dimensao}_{limite}_cm"
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
                    f"limites.{dimensao}_minima_cm",
                    f"deve ser menor ou igual a {dimensao}_maxima_cm",
                )
            )


def _validar_relacoes_inversas(
    elementos: list[object], raiz: str, por_id: dict[int, object]
) -> list[ErroValidacao]:
    """Valida a coerência das relações espaciais inversas."""
    erros: list[ErroValidacao] = []
    pares = (
        ("em_cima_de_id", "embaixo_de_id"),
        ("embaixo_de_id", "em_cima_de_id"),
        ("a_direita_de_id", "a_esquerda_de_id"),
        ("a_esquerda_de_id", "a_direita_de_id"),
    )
    for indice, elemento in enumerate(elementos):
        for campo, campo_inverso in pares:
            referencia = getattr(elemento, campo)
            referenciado = por_id.get(referencia)
            if referenciado is None:
                continue
            inversa = getattr(referenciado, campo_inverso)
            if inversa is not None and inversa != elemento.id:
                erros.append(
                    ErroValidacao(
                        f"{raiz}.{indice}.{campo}",
                        f"a relação inversa {campo_inverso} do elemento {referencia} é incoerente",
                    )
                )
    return erros


def _validar_ciclos(
    elementos: list[object], raiz: str, ids: set[int]
) -> list[ErroValidacao]:
    """Valida a ausência de ciclos nas relações espaciais."""
    vertical = {elemento_id: set() for elemento_id in ids}
    horizontal = {elemento_id: set() for elemento_id in ids}
    for elemento in elementos:
        if elemento.em_cima_de_id in ids:
            vertical[elemento.id].add(elemento.em_cima_de_id)
        if elemento.embaixo_de_id in ids:
            vertical[elemento.embaixo_de_id].add(elemento.id)
        if elemento.a_direita_de_id in ids:
            horizontal[elemento.a_direita_de_id].add(elemento.id)
        if elemento.a_esquerda_de_id in ids:
            horizontal[elemento.id].add(elemento.a_esquerda_de_id)

    erros: list[ErroValidacao] = []
    if _possui_ciclo(vertical):
        erros.append(ErroValidacao(raiz, "as relações do eixo vertical formam um ciclo"))
    if _possui_ciclo(horizontal):
        erros.append(ErroValidacao(raiz, "as relações do eixo horizontal formam um ciclo"))
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
