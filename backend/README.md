# Backend — Fases 1 e 2

## Preparação

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[test]"
```

## Execução

```powershell
.\.venv\Scripts\python.exe -m uvicorn marcenaria_digital_api.main:app --reload
```

A documentação OpenAPI ficará disponível em `http://127.0.0.1:8000/docs`.

Endpoints disponíveis:

- `POST /api/v1/configuracoes`: cria uma configuração;
- `GET /api/v1/configuracoes`: lista configurações ativas;
- `GET /api/v1/configuracoes/{id}`: consulta uma configuração ativa;
- `GET /api/v1/estilos-armario`: lista estilos com configurações ativas.

Cada configuração agrupa suas faixas dimensionais no objeto `limites`, que
contém os valores mínimos e máximos de altura, largura, profundidade e espessura
em centímetros. Esse mesmo formato aninhado é usado pela API e pelo arquivo JSON.

Portas enviadas e retornadas na coleção `portas` incluem:

```json
{
  "abertura": "ABERTURA VERTICAL PARA DIREITA"
}
```

Cada item representa uma única porta. O campo `abertura` aceita
`ABERTURA VERTICAL PARA DIREITA`, `ABERTURA VERTICAL PARA ESQUERDA`,
`ABERTURA HORIZONTAL PARA CIMA`, `ABERTURA HORIZONTAL PARA BAIXO` ou
`PORTA CORRER`.
A coleção `compartimentos` contém exclusivamente compartimentos. A quantidade de
portas é derivada do tamanho da coleção `portas`.

Cada configuração também informa `acabamentos`, uma lista opcional que pode ser
omitida ou enviada vazia quando não houver acabamentos.
Cada item possui `id`, `tipo_acabamento` (`SUPERIOR`, `INFERIOR`, `DIREITA` ou
`ESQUERDA`), `estilo_acabamento` (`INTERNO` ou `EXTERNO`), `extensao_cm`,
`espessura` (`6 mm`, `15 mm` ou `18 mm`) e os cortes das duas extremidades
(`reto` ou `meia esquadria`). Os IDs dos acabamentos devem ser positivos e
únicos na coleção `acabamentos`.

No domínio Python, o estilo fica em `ConfiguracaoArmario.estilo_armario` e a
posição do acabamento em `AcabamentoExterno.posicao`. Os contratos HTTP e o JSON
versionado mantêm, respectivamente, os nomes `estilo` e
`acabamentos[].tipo_acabamento`; o schema e o repositório fazem essa conversão
explicitamente. `tipo` é validado como `ARMARIO` na entrada e obtido da
propriedade derivada `Configuracao.tipo` nas entidades. `Configuracao` é
abstrata; `ConfiguracaoArmario` é a implementação concreta e contém as
coleções `acabamentos`, `compartimentos` e `portas`. `Limites` agrupa oito
valores `Decimal` positivos em centímetros: mínimo e máximo de altura, largura,
profundidade e espessura.

Enums disponíveis no backend:

- `TipoMovel`: `ARMARIO`;
- `EstiloMovel`: `MULTIUSO`, `GUARDA_ROUPA`, `ARMARIO_AEREO`;
- `DirecaoVertical`: `cima_baixo`, `baixo_cima`;
- `DirecaoHorizontal`: `direita_esquerda`, `esquerda_direita`;
- `Posicao`: `SUPERIOR`, `INFERIOR`, `DIREITA`, `ESQUERDA`;
- `EstiloAcabamento`: `INTERNO`, `EXTERNO`;
- `Espessura`: `6 mm`, `15 mm`, `18 mm`;
- `Corte`: `reto`, `meia esquadria`;
- `AberturaPorta`: `ABERTURA VERTICAL PARA DIREITA`,
  `ABERTURA VERTICAL PARA ESQUERDA`, `ABERTURA HORIZONTAL PARA CIMA`,
  `ABERTURA HORIZONTAL PARA BAIXO`, `PORTA CORRER`.

`CompartimentoConfiguracao` representa um compartimento; cada
`PortaConfiguracao` representa uma porta e exige `abertura`. Ambas as coleções
usam percentuais de ocupação entre 0 (exclusivo) e 100 (inclusivo), IDs
positivos únicos dentro da própria coleção e relações espaciais opcionais
apontadas para itens da mesma coleção. Uma configuração exige ao menos um
compartimento; `acabamentos` e `portas` podem estar vazias ou ser omitidas no
request.

No catálogo da Fase 2, o frontend consulta `GET /api/v1/configuracoes` e exibe
as prévias SVG **Layout Interno** (compartimentos e acabamentos em suas posições
de borda) e **Layout Externo** (portas). A tabela possui as colunas Layout
Interno, Layout Externo, Tipo de móvel, Estilo, Limites, Acabamentos, Portas,
Compartimentos, Status e Ações. Limites apresenta os intervalos de altura,
largura, profundidade e espessura. As colunas Acabamentos, Portas e
Compartimentos mostram as respectivas quantidades; Acabamentos não discrimina
posição ou estilo. A interface também permite buscar e ordenar configurações,
selecionar uma por seu ID e apresenta estados de carregamento, vazio e erro.
Essas projeções são somente de leitura e não alteram os dados persistidos.

O caminho do arquivo de configurações pode ser sobrescrito pela variável de
ambiente `MARCENARIA_CONFIGURACOES_JSON_PATH`.

## Arquitetura

O backend utiliza Arquitetura em Camadas com o padrão
Route-Service-Repository:

```text
routes --> services --> repositories
              |              |
              +--> entities <-+
```

- `routes`: define os endpoints e schemas HTTP, chama os serviços e converte
  resultados e erros em respostas da API.
- `services`: coordena os fluxos da aplicação, as validações e as regras de
  negócio.
- `repositories`: define os contratos e implementa a persistência e recuperação
  dos dados. Na Fase 1, utiliza o arquivo JSON versionado.
- `entities`: contém entidades, enums, objetos de valor e exceções do negócio,
  sem depender das demais camadas.

As rotas não devem conter regras de negócio nem acessar repositórios diretamente.
Os repositórios são criados e injetados nos serviços pelo ponto de entrada
`marcenaria_digital_api.main`.

Estrutura principal:

```text
src/marcenaria_digital_api/
├── entities/
├── repositories/
├── routes/
├── services/
├── config.py
└── main.py
```

## Testes

```powershell
.\.venv\Scripts\python.exe -m pytest
```
