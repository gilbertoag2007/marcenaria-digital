<script setup lang="ts">
import { computed } from "vue";

import type { DetalheConfiguracao } from "../types/configuracao";
import { calcularLayoutPrevia } from "../utils/layoutPrevia";

const props = defineProps<{
  detalhes: DetalheConfiguracao[];
  descricao: string;
}>();

const retangulos = computed(() => calcularLayoutPrevia(props.detalhes));
</script>

<template>
  <svg
    class="previa"
    viewBox="0 0 100 100"
    role="img"
    :aria-label="descricao"
    preserveAspectRatio="xMidYMid meet"
  >
    <title>{{ descricao }}</title>
    <rect class="estrutura" x="1" y="1" width="98" height="98" rx="2" />
    <g v-for="retangulo in retangulos" :key="retangulo.id">
      <rect
        :class="['detalhe', `detalhe--${retangulo.tipo.toLowerCase()}`]"
        :x="2 + retangulo.x * 0.96"
        :y="2 + retangulo.y * 0.96"
        :width="retangulo.largura * 0.96"
        :height="retangulo.altura * 0.96"
        rx="0.5"
      />
    </g>
  </svg>
</template>
