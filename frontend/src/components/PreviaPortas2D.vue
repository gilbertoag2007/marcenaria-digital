<script setup lang="ts">
import { computed } from "vue";

import type { PortaConfiguracao } from "../types/configuracao";
import { calcularLayoutPortasPrevia } from "../utils/layoutPrevia";

const props = defineProps<{
  portas: PortaConfiguracao[];
  descricao: string;
}>();

const retangulos = computed(() => calcularLayoutPortasPrevia(props.portas));
</script>

<template>
  <svg
    class="previa previa--externa"
    viewBox="0 0 100 100"
    role="img"
    :aria-label="descricao"
    preserveAspectRatio="xMidYMid meet"
  >
    <title>{{ descricao }}</title>
    <rect class="estrutura" x="1" y="1" width="98" height="98" rx="2" />
    <rect
      v-for="porta in retangulos"
      :key="porta.id"
      class="porta-externa"
      :x="2 + porta.x * 0.96"
      :y="2 + porta.y * 0.96"
      :width="porta.largura * 0.96"
      :height="porta.altura * 0.96"
      rx="0.5"
    />
  </svg>
</template>
