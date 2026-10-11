export type TipoMovel = "ARMARIO";
export type EstiloMovel = "MULTIUSO" | "GUARDA_ROUPA" | "ARMARIO_AEREO";
export type TipoConfiguracao = "COMPARTIMENTO" | "PORTA";

export interface DetalheConfiguracao {
  id: number;
  tipo: TipoConfiguracao;
  percentual_ocupacao_vertical: number;
  percentual_ocupacao_horizontal: number;
  em_cima_de_id: number | null;
  embaixo_de_id: number | null;
  a_direita_de_id: number | null;
  a_esquerda_de_id: number | null;
}

export interface Configuracao {
  id: number;
  tipo: TipoMovel;
  estilo: EstiloMovel;
  altura_minima_cm: number;
  altura_maxima_cm: number;
  largura_minima_cm: number;
  largura_maxima_cm: number;
  profundidade_minima_cm: number;
  profundidade_maxima_cm: number;
  ativo: boolean;
  detalhes: DetalheConfiguracao[];
}
