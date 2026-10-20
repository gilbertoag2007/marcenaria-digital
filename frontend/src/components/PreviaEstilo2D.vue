<script setup lang="ts">
import { computed } from "vue";

import type {
  AcabamentoExterno,
  CompartimentoConfiguracao,
  Posicao,
} from "../types/configuracao";
import { calcularLayoutPrevia } from "../utils/layoutPrevia";

const INICIO_ESTRUTURA = 2;
const EXTENSAO_ESTRUTURA = 96;
const ESPESSURA_VISUAL_ACABAMENTO = 12;

interface RetanguloAcabamento {
  id: number;
  posicao: Posicao;
  x: number;
  y: number;
  largura: number;
  altura: number;
}

const AREAS_ACABAMENTO: Record<
  Posicao,
  Omit<RetanguloAcabamento, "id" | "posicao">
> = {
  SUPERIOR: {
    x: INICIO_ESTRUTURA,
    y: INICIO_ESTRUTURA,
    largura: EXTENSAO_ESTRUTURA,
    altura: ESPESSURA_VISUAL_ACABAMENTO,
  },
  INFERIOR: {
    x: INICIO_ESTRUTURA,
    y: 98 - ESPESSURA_VISUAL_ACABAMENTO,
    largura: EXTENSAO_ESTRUTURA,
    altura: ESPESSURA_VISUAL_ACABAMENTO,
  },
  ESQUERDA: {
    x: INICIO_ESTRUTURA,
    y: INICIO_ESTRUTURA,
    largura: ESPESSURA_VISUAL_ACABAMENTO,
    altura: EXTENSAO_ESTRUTURA,
  },
  DIREITA: {
    x: 98 - ESPESSURA_VISUAL_ACABAMENTO,
    y: INICIO_ESTRUTURA,
    largura: ESPESSURA_VISUAL_ACABAMENTO,
    altura: EXTENSAO_ESTRUTURA,
  },
};

const props = defineProps<{
  acabamentos: AcabamentoExterno[];
  compartimentos: CompartimentoConfiguracao[];
  descricao: string;
}>();

const retangulos = computed(() => {
  const posicoes = new Set(props.acabamentos.map(({ posicao }) => posicao));
  const esquerda = posicoes.has("ESQUERDA") ? ESPESSURA_VISUAL_ACABAMENTO : 0;
  const direita = posicoes.has("DIREITA") ? ESPESSURA_VISUAL_ACABAMENTO : 0;
  const superior = posicoes.has("SUPERIOR") ? ESPESSURA_VISUAL_ACABAMENTO : 0;
  const inferior = posicoes.has("INFERIOR") ? ESPESSURA_VISUAL_ACABAMENTO : 0;
  const largura = EXTENSAO_ESTRUTURA - esquerda - direita;
  const altura = EXTENSAO_ESTRUTURA - superior - inferior;

  return calcularLayoutPrevia(props.compartimentos).map((retangulo) => ({
    ...retangulo,
    x: INICIO_ESTRUTURA + esquerda + (retangulo.x / 100) * largura,
    y: INICIO_ESTRUTURA + superior + (retangulo.y / 100) * altura,
    largura: (retangulo.largura / 100) * largura,
    altura: (retangulo.altura / 100) * altura,
  }));
});

const retangulosAcabamentos = computed((): RetanguloAcabamento[] =>
  props.acabamentos.map(({ id, posicao }) => ({
    id,
    posicao,
    ...AREAS_ACABAMENTO[posicao],
  })),
);
</script>

<template>
  <svg
    class="previa previa--interna"
    viewBox="0 0 100 100"
    role="img"
    :aria-label="descricao"
    preserveAspectRatio="xMidYMid meet"
  >
    <title>{{ descricao }}</title>
    <rect class="estrutura" x="1" y="1" width="98" height="98" rx="2" />
    <g v-for="retangulo in retangulos" :key="retangulo.id">
      <rect
        class="compartimento"
        :x="retangulo.x"
        :y="retangulo.y"
        :width="retangulo.largura"
        :height="retangulo.altura"
        rx="0.5"
      />
    </g>
    <rect
      v-for="acabamento in retangulosAcabamentos"
      :key="acabamento.id"
      class="acabamento-externo"
      :data-posicao="acabamento.posicao"
      :x="acabamento.x"
      :y="acabamento.y"
      :width="acabamento.largura"
      :height="acabamento.altura"
      rx="0.5"
    />
  </svg>
</template>
