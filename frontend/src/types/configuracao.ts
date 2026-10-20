export type TipoMovel = "ARMARIO";
export type EstiloMovel = "MULTIUSO" | "GUARDA_ROUPA" | "ARMARIO_AEREO";
export type Posicao = "SUPERIOR" | "INFERIOR" | "DIREITA" | "ESQUERDA";
export type EstiloAcabamento = "INTERNO" | "EXTERNO";
export type Corte = "reto" | "meia esquadria";
export type Espessura = "6 mm" | "15 mm" | "18 mm";
export type DirecaoVertical = "cima_baixo" | "baixo_cima";
export type DirecaoHorizontal = "direita_esquerda" | "esquerda_direita";
export type AberturaPorta =
  | "ABERTURA VERTICAL PARA DIREITA"
  | "ABERTURA VERTICAL PARA ESQUERDA"
  | "ABERTURA HORIZONTAL PARA CIMA"
  | "ABERTURA HORIZONTAL PARA BAIXO"
  | "PORTA CORRER";

export interface AcabamentoExterno {
  id: number;
  posicao: Posicao;
  estilo_acabamento: EstiloAcabamento;
  extensao_cm: number;
  espessura: Espessura;
  corte_extremidade_1: Corte;
  corte_extremidade_2: Corte;
}

export interface Limites {
  altura_minima_cm: number;
  altura_maxima_cm: number;
  largura_minima_cm: number;
  largura_maxima_cm: number;
  profundidade_minima_cm: number;
  profundidade_maxima_cm: number;
  espessura_minima_cm: number;
  espessura_maxima_cm: number;
}

export interface CompartimentoConfiguracao {
  id: number;
  percentual_ocupacao_vertical: number;
  percentual_ocupacao_horizontal: number;
  em_cima_de_id: number | null;
  embaixo_de_id: number | null;
  a_direita_de_id: number | null;
  a_esquerda_de_id: number | null;
}

export interface PortaConfiguracao extends CompartimentoConfiguracao {
  abertura: AberturaPorta;
}

export interface Configuracao {
  id: number;
  tipo: TipoMovel;
  estilo_armario: EstiloMovel;
  limites: Limites;
  ativo: boolean;
  direcao_vertical: DirecaoVertical;
  direcao_horizontal: DirecaoHorizontal;
  acabamentos: AcabamentoExterno[];
  compartimentos: CompartimentoConfiguracao[];
  portas: PortaConfiguracao[];
}

export type AcabamentoExternoRespostaApi = Omit<
  AcabamentoExterno,
  "posicao"
> & {
  tipo_acabamento: Posicao;
};

export type ConfiguracaoRespostaApi = Omit<
  Configuracao,
  "estilo_armario" | "acabamentos"
> & {
  estilo: EstiloMovel;
  acabamentos: AcabamentoExternoRespostaApi[];
};
