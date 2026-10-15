import type { DetalheConfiguracao } from "../types/configuracao";

export interface RetanguloPrevia {
  id: number;
  tipo: DetalheConfiguracao["tipo"];
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

/** Calcula retângulos normalizados para representar os detalhes no SVG. */
export function calcularLayoutPrevia(
  detalhes: DetalheConfiguracao[],
): RetanguloPrevia[] {
  if (detalhes.length === 0) return [];

  const porId = new Map(detalhes.map((detalhe) => [detalhe.id, detalhe]));
  const posicoes = new Map<number, Posicao>(
    detalhes.map((detalhe) => [detalhe.id, { x: 0, y: 0 }]),
  );

  for (let rodada = 0; rodada < detalhes.length; rodada += 1) {
    for (const detalhe of detalhes) {
      posicionarPelasRelacoes(detalhe, porId, posicoes);
    }
  }

  const limites = detalhes.reduce(
    (atual, detalhe) => {
      const posicao = posicoes.get(detalhe.id)!;
      return {
        esquerda: Math.min(atual.esquerda, posicao.x),
        topo: Math.min(atual.topo, posicao.y),
        direita: Math.max(
          atual.direita,
          posicao.x + detalhe.percentual_ocupacao_horizontal,
        ),
        base: Math.max(
          atual.base,
          posicao.y + detalhe.percentual_ocupacao_vertical,
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
  const limitesPorFaixa = calcularLimitesHorizontaisPorFaixa(detalhes, posicoes);

  return detalhes.map((detalhe) => {
    const posicao = posicoes.get(detalhe.id)!;
    const limitesHorizontais = limitesPorFaixa.get(chaveDaFaixa(posicao.y))!;
    const larguraDaFaixa = Math.max(
      limitesHorizontais.direita - limitesHorizontais.esquerda,
      1,
    );
    return {
      id: detalhe.id,
      tipo: detalhe.tipo,
      x: ((posicao.x - limitesHorizontais.esquerda) / larguraDaFaixa) * 100,
      y: ((posicao.y - limites.topo) / alturaTotal) * 100,
      largura:
        (detalhe.percentual_ocupacao_horizontal / larguraDaFaixa) * 100,
      altura: (detalhe.percentual_ocupacao_vertical / alturaTotal) * 100,
    };
  });
}

/** Calcula os retângulos das portas para representar a fachada da configuração. */
export function calcularLayoutPortasPrevia(
  detalhes: DetalheConfiguracao[],
): RetanguloPortaPrevia[] {
  const retangulosPorId = new Map(
    calcularLayoutPrevia(detalhes).map((retangulo) => [retangulo.id, retangulo]),
  );

  return detalhes.flatMap((detalhe) => {
    const retangulo = retangulosPorId.get(detalhe.id);
    if (!retangulo) return [];

    if (detalhe.tipo === "PORTA") {
      return [{ ...retangulo, id: `${detalhe.id}-1` }];
    }

    if (detalhe.quantidade_portas === 0) return [];

    const aberturaHorizontal = detalhe.abertura_porta.startsWith(
      "ABERTURA HORIZONTAL",
    );
    return Array.from({ length: detalhe.quantidade_portas }, (_, indice) => ({
      id: `${detalhe.id}-${indice + 1}`,
      x: aberturaHorizontal
        ? retangulo.x
        : retangulo.x + (retangulo.largura / detalhe.quantidade_portas) * indice,
      y: aberturaHorizontal
        ? retangulo.y + (retangulo.altura / detalhe.quantidade_portas) * indice
        : retangulo.y,
      largura: aberturaHorizontal
        ? retangulo.largura
        : retangulo.largura / detalhe.quantidade_portas,
      altura: aberturaHorizontal
        ? retangulo.altura / detalhe.quantidade_portas
        : retangulo.altura,
    }));
  });
}

/** Obtém os limites de cada faixa horizontal para eliminar deslocamentos entre linhas. */
function calcularLimitesHorizontaisPorFaixa(
  detalhes: DetalheConfiguracao[],
  posicoes: Map<number, Posicao>,
): Map<string, LimitesHorizontais> {
  const limitesPorFaixa = new Map<string, LimitesHorizontais>();

  for (const detalhe of detalhes) {
    const posicao = posicoes.get(detalhe.id)!;
    const chave = chaveDaFaixa(posicao.y);
    const limitesAtuais = limitesPorFaixa.get(chave);
    const direita = posicao.x + detalhe.percentual_ocupacao_horizontal;

    limitesPorFaixa.set(chave, {
      esquerda: Math.min(limitesAtuais?.esquerda ?? posicao.x, posicao.x),
      direita: Math.max(limitesAtuais?.direita ?? direita, direita),
    });
  }

  return limitesPorFaixa;
}

/** Gera uma chave estável para detalhes posicionados na mesma faixa vertical. */
function chaveDaFaixa(y: number): string {
  return y.toFixed(6);
}

/** Atualiza a posição de um detalhe a partir das relações declaradas. */
function posicionarPelasRelacoes(
  detalhe: DetalheConfiguracao,
  porId: Map<number, DetalheConfiguracao>,
  posicoes: Map<number, Posicao>,
): void {
  const posicao = posicoes.get(detalhe.id)!;
  const direitaDe = obterReferencia(detalhe.a_direita_de_id, porId, posicoes);
  const esquerdaDe = obterReferencia(detalhe.a_esquerda_de_id, porId, posicoes);
  const embaixoDe = obterReferencia(detalhe.embaixo_de_id, porId, posicoes);
  const emCimaDe = obterReferencia(detalhe.em_cima_de_id, porId, posicoes);

  if (direitaDe) {
    posicao.x =
      direitaDe.posicao.x + direitaDe.detalhe.percentual_ocupacao_horizontal;
  } else if (esquerdaDe) {
    posicao.x =
      esquerdaDe.posicao.x - detalhe.percentual_ocupacao_horizontal;
  }
  if (embaixoDe) {
    posicao.y =
      embaixoDe.posicao.y + embaixoDe.detalhe.percentual_ocupacao_vertical;
  } else if (emCimaDe) {
    posicao.y = emCimaDe.posicao.y - detalhe.percentual_ocupacao_vertical;
  }
}

/** Recupera um detalhe de referência e sua posição calculada. */
function obterReferencia(
  id: number | null,
  porId: Map<number, DetalheConfiguracao>,
  posicoes: Map<number, Posicao>,
): { detalhe: DetalheConfiguracao; posicao: Posicao } | null {
  if (id === null) return null;
  const detalhe = porId.get(id);
  const posicao = posicoes.get(id);
  return detalhe && posicao ? { detalhe, posicao } : null;
}
