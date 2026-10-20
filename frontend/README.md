# Frontend — Fase 2

Aplicação Vue 3 com TypeScript e Vite para o catálogo visual de configurações.
O contrato TypeScript separa os compartimentos em `compartimentos` e as portas na
coleção `portas`. Cada porta possui uma `abertura` obrigatória, que pode ser
vertical, horizontal ou `PORTA CORRER`.
O contrato também tipa a posição do acabamento (`SUPERIOR`, `INFERIOR`,
`DIREITA` ou `ESQUERDA`), seu estilo (`INTERNO` ou `EXTERNO`), espessura e
cortes. O modelo usado pela interface segue os nomes do domínio backend:
`ConfiguracaoArmario.estilo_armario` e `AcabamentoExterno.posicao`. O endpoint
`GET /api/v1/configuracoes` mantém os nomes HTTP `estilo` e
`acabamentos[].tipo_acabamento`; `configuracoesApi.ts` converte explicitamente
esses campos para os nomes de domínio antes de entregar as configurações aos
componentes.
O catálogo consome `GET /api/v1/configuracoes`. As faixas mínima e máxima de
altura, largura, profundidade e espessura ficam agrupadas no objeto `limites`
de cada configuração e são apresentadas sob o cabeçalho **Limites**, sem
alteração dos valores.

Os contratos TypeScript refletem os enums atuais do backend: tipo `ARMARIO`;
estilos `MULTIUSO`, `GUARDA_ROUPA` e `ARMARIO_AEREO`; direções
`cima_baixo`/`baixo_cima` e `direita_esquerda`/`esquerda_direita`; posições
`SUPERIOR`, `INFERIOR`, `DIREITA` e `ESQUERDA`; estilos de acabamento `INTERNO`
e `EXTERNO`; espessuras `6 mm`, `15 mm` e `18 mm`; cortes `reto` e
`meia esquadria`; e as quatro aberturas vertical/horizontal mais `PORTA CORRER`.
Na lista de configurações cadastradas, cada item apresenta:

- **Layout Interno**: prévia SVG dos compartimentos e dos acabamentos configurados
  nas bordas, com paleta uniforme e divisões visíveis mesmo quando existe uma
  porta externa sobreposta. Cada acabamento é representado pela posição na
  borda, em escala visual normalizada;
- **Layout Externo**: prévia SVG com um retângulo por item da coleção `portas`;
- **Acabamentos**: quantidade total de acabamentos, sem discriminar posição ou
  estilo;
- **Portas**: quantidade total de portas;
- **Compartimentos**: quantidade total de compartimentos.
- **Tipo de móvel**, **Estilo**, **Status** e **Ações**: identificam a
  configuração disponível e permitem selecionar uma opção.

As portas são desenhadas no Layout Externo e não encobrem os
compartimentos do Layout Interno. A busca considera o identificador, o tipo, o
estilo e os rótulos/estilos dos acabamentos; a ordenação opcional é pelo nome
do estilo. A seleção é transitória e identificada pelo ID da configuração.
O catálogo também informa os estados de carregamento, lista vazia retornada
pela API e erro com opção de nova tentativa.

## Preparação

```powershell
cd frontend
npm install
```

## Execução

Com o backend disponível em `http://127.0.0.1:8000`:

```powershell
npm run dev
```

O catálogo ficará disponível em `http://localhost:5173`.

## Verificação

```powershell
npm run typecheck
npm test
npm run build
```

Defina `VITE_API_BASE_URL` somente quando a API não estiver disponível pelo
proxy local `/api/v1` configurado no Vite.
