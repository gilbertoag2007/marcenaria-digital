import type {
  CompartimentoConfiguracao,
  PortaConfiguracao,
} from "../types/configuracao";

export interface RetanguloPrevia {
  id: number;
  x: number;
  y: number;
  largura: number;
  altura: number;
}

export interface RetanguloPortaPrevia {
  id: string;
  x: number;
  y: number;
  largura: number;
  altura: number;
}

interface Posicao {
  x: number;
  y: number;
}

interface LimitesHorizontais {
  esquerda: number;
  direita: number;
}

/** Calcula retângulos normalizados para representar elementos no SVG. */
export function calcularLayoutPrevia(
  elementos: CompartimentoConfiguracao[],
): RetanguloPrevia[] {
  if (elementos.length === 0) return [];

  const porId = new Map(elementos.map((elemento) => [elemento.id, elemento]));
  const posicoes = new Map<number, Posicao>(
    elementos.map((elemento) => [elemento.id, { x: 0, y: 0 }]),
  );

  for (let rodada = 0; rodada < elementos.length; rodada += 1) {
    for (const elemento of elementos) {
      posicionarPelasRelacoes(elemento, porId, posicoes);
    }
  }

  const limites = elementos.reduce(
    (atual, elemento) => {
      const posicao = posicoes.get(elemento.id)!;
      return {
        esquerda: Math.min(atual.esquerda, posicao.x),
        topo: Math.min(atual.topo, posicao.y),
        direita: Math.max(
          atual.direita,
          posicao.x + elemento.percentual_ocupacao_horizontal,
        ),
        base: Math.max(
          atual.base,
          posicao.y + elemento.percentual_ocupacao_vertical,
        ),
      };
    },
    {
      esquerda: Number.POSITIVE_INFINITY,
      topo: Number.POSITIVE_INFINITY,
      direita: Number.NEGATIVE_INFINITY,
      base: Number.NEGATIVE_INFINITY,
    },
  );
  const alturaTotal = Math.max(limites.base - limites.topo, 1);
  const limitesPorFaixa = calcularLimitesHorizontaisPorFaixa(elementos, posicoes);

  return elementos.map((elemento) => {
    const posicao = posicoes.get(elemento.id)!;
    const limitesHorizontais = limitesPorFaixa.get(chaveDaFaixa(posicao.y))!;
    const larguraDaFaixa = Math.max(
      limitesHorizontais.direita - limitesHorizontais.esquerda,
      1,
    );
    return {
      id: elemento.id,
      x: ((posicao.x - limitesHorizontais.esquerda) / larguraDaFaixa) * 100,
      y: ((posicao.y - limites.topo) / alturaTotal) * 100,
      largura:
        (elemento.percentual_ocupacao_horizontal / larguraDaFaixa) * 100,
      altura: (elemento.percentual_ocupacao_vertical / alturaTotal) * 100,
    };
  });
}

/** Calcula os retângulos das portas para representar a fachada da configuração. */
export function calcularLayoutPortasPrevia(
  portas: PortaConfiguracao[],
): RetanguloPortaPrevia[] {
  const retangulosPorId = new Map(
    calcularLayoutPrevia(portas).map((retangulo) => [retangulo.id, retangulo]),
  );

  return portas.flatMap((porta) => {
    const retangulo = retangulosPorId.get(porta.id);
    if (!retangulo) return [];
    return [{ ...retangulo, id: `${porta.id}` }];
  });
}

/** Obtém os limites de cada faixa horizontal para eliminar deslocamentos entre linhas. */
function calcularLimitesHorizontaisPorFaixa(
  elementos: CompartimentoConfiguracao[],
  posicoes: Map<number, Posicao>,
): Map<string, LimitesHorizontais> {
  const limitesPorFaixa = new Map<string, LimitesHorizontais>();

  for (const elemento of elementos) {
    const posicao = posicoes.get(elemento.id)!;
    const chave = chaveDaFaixa(posicao.y);
    const limitesAtuais = limitesPorFaixa.get(chave);
    const direita = posicao.x + elemento.percentual_ocupacao_horizontal;

    limitesPorFaixa.set(chave, {
      esquerda: Math.min(limitesAtuais?.esquerda ?? posicao.x, posicao.x),
      direita: Math.max(limitesAtuais?.direita ?? direita, direita),
    });
  }

  return limitesPorFaixa;
}

/** Gera uma chave estável para elementos posicionados na mesma faixa vertical. */
function chaveDaFaixa(y: number): string {
  return y.toFixed(6);
}

/** Atualiza a posição de um elemento a partir das relações declaradas. */
function posicionarPelasRelacoes(
  elemento: CompartimentoConfiguracao,
  porId: Map<number, CompartimentoConfiguracao>,
  posicoes: Map<number, Posicao>,
): void {
  const posicao = posicoes.get(elemento.id)!;
  const direitaDe = obterReferencia(elemento.a_direita_de_id, porId, posicoes);
  const esquerdaDe = obterReferencia(elemento.a_esquerda_de_id, porId, posicoes);
  const embaixoDe = obterReferencia(elemento.embaixo_de_id, porId, posicoes);
  const emCimaDe = obterReferencia(elemento.em_cima_de_id, porId, posicoes);

  if (direitaDe) {
    posicao.x =
      direitaDe.posicao.x + direitaDe.elemento.percentual_ocupacao_horizontal;
  } else if (esquerdaDe) {
    posicao.x =
      esquerdaDe.posicao.x - elemento.percentual_ocupacao_horizontal;
  }
  if (embaixoDe) {
    posicao.y =
      embaixoDe.posicao.y + embaixoDe.elemento.percentual_ocupacao_vertical;
  } else if (emCimaDe) {
    posicao.y = emCimaDe.posicao.y - elemento.percentual_ocupacao_vertical;
  }
}

/** Recupera um elemento de referência e sua posição calculada. */
function obterReferencia(
  id: number | null,
  porId: Map<number, CompartimentoConfiguracao>,
  posicoes: Map<number, Posicao>,
): { elemento: CompartimentoConfiguracao; posicao: Posicao } | null {
  if (id === null) return null;
  const elemento = porId.get(id);
  const posicao = posicoes.get(id);
  return elemento && posicao ? { elemento, posicao } : null;
}
