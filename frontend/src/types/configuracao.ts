export type TipoMovel = "ARMARIO";
export type EstiloMovel = "MULTIUSO" | "GUARDA_ROUPA" | "ARMARIO_AEREO";
export type TipoConfiguracao = "COMPARTIMENTO" | "PORTA";
export type AberturaPorta =
  | "ABERTURA VERTICAL PARA DIREITA"
  | "ABERTURA VERTICAL PARA ESQUERDA"
  | "ABERTURA HORIZONTAL PARA CIMA"
  | "ABERTURA HORIZONTAL PARA BAIXO";
export type QuantidadePortas = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10;

interface DetalheConfiguracaoBase {
  id: number;
  percentual_ocupacao_vertical: number;
  percentual_ocupacao_horizontal: number;
  em_cima_de_id: number | null;
  embaixo_de_id: number | null;
  a_direita_de_id: number | null;
  a_esquerda_de_id: number | null;
}

export type DetalheConfiguracao = DetalheConfiguracaoBase &
  (
    | {
        tipo: "COMPARTIMENTO";
        quantidade_portas: 0;
        abertura_porta: null;
      }
    | {
        tipo: "COMPARTIMENTO";
        quantidade_portas: Exclude<QuantidadePortas, 0>;
        abertura_porta: AberturaPorta;
      }
    | {
        tipo: "PORTA";
        quantidade_portas: null;
        abertura_porta: null;
      }
  );

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
