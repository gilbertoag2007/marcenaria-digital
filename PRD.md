# PRD — Marcenaria Digital

## 1. Visão do Produto
Este sistema foi idealizado a partir de uma necessidade prática relacionada à marcenaria como hobby. Nas horas vagas, sempre que possível, construo móveis sob medida para uso particular. Uma das primeiras tarefas desse processo é elaborar o plano de corte das peças que serão utilizadas no móvel.
Sem o sistema, esse processo é realizado manualmente, com papel e caneta e com isso sujeitos a erros de calculo.

O **Marcenaria Digital** é um sistema para auxiliar na elaboração do plano de corte, na configuração de um layout de acordo com o tipo e o estilo do móvel selecionado, na visualização do móvel em 2D e 3D e na impressão do plano de corte e do manual de montagem.

O usuário informa as dimensões e características do móvel desejado e o sistema calcula automaticamente as peças necessárias para sua construção, gerando: **plano de corte**, **lista de materiais**, **visualização do móvel em 2D e 3D** e **manual de montagem**.

---

## 2. Problema

A construção de móveis sob medida exige diversos cálculos manuais relacionados a:

* dimensões externas do móvel;
* espessura das chapas;
* laterais, base e topo;
* compartimentos internos;
* prateleiras;
* gavetas;
* fundos;
* portas;
* acabamentos;
* ferragens e demais materiais.

Erros nesses cálculos podem resultar em desperdício de MDF, peças com dimensões incorretas e dificuldade durante a montagem.

O sistema busca automatizar essas etapas e transformar as especificações do móvel em informações utilizáveis para corte e montagem.

---

## 3. Objetivo

Permitir que o usuário projete um móvel sob medida informando suas dimensões e características estruturais.

A partir dessas informações, o sistema deverá:

1. validar se o móvel pode ser construído conforme as regras cadastradas;
2. calcular automaticamente as peças necessárias considerando quantidade de compartimentos;
3. calcular os materiais de acabamento e montagem necessários;
4. permitir a visualização do projeto em 2D e 3D;
5. gerar o plano de corte em chapa de MDF padrão (275 cm × 185 cm);
6. armazenar todas as informações do móvel para consultas futuras;
7. permitir a impressão e a exportação do plano de corte;
8. gerar o manual de montagem e permitir sua impressão e exportação.

---

## 4. Escopo Inicial

A primeira versão será focada em **armários de MDF**.

Cada armário será definido principalmente pelas seguintes informações:

* nome do móvel;
* altura do móvel;
* largura do móvel;
* profundidade do móvel;
* tipo de móvel (armário);
* estilo do móvel (armário multiuso, guarda-roupa ou armário aéreo).

Por se tratar de um armário, as seguintes informações também deverão ser fornecidas:

* possui acabamento frontal superior? (Sim ou Não);
* possui acabamento frontal inferior? (Sim ou Não);
* quantidade de compartimentos internos;
* conteúdo de cada compartimento e suas respectivas quantidades (gavetas, cabideiros e áreas livres);
* configuração das gavetas;
* configuração dos cabideiros;
* configuração das áreas livres;
* quantidade e disposição das portas.

Os cálculos utilizarão centímetros (cm) como unidade principal para as dimensões do móvel e das peças. Apenas as espessuras do fundo do armário e fundo de gavetas serão expressas em milímetros (mm).

## 4.1 Estratégia de entrega incremental

O produto será construído em 11 fases cumulativas. Cada fase somente deverá
introduzir a infraestrutura e as funcionalidades necessárias para o seu próprio
objetivo e deverá preservar os contratos entregues pelas fases anteriores.

Nas Fases 1 a 7, as configurações serão persistidas em um arquivo JSON
versionado dentro do projeto. Os dados informados para um móvel e os resultados
dos cálculos permanecerão apenas em memória durante a requisição ou na sessão do
frontend; portanto, ainda não será possível salvar nem recuperar um móvel.

Na Fase 8, as configurações passarão a possuir CRUD completo com banco de dados.
Na Fase 9, o mesmo ocorrerá com os móveis e seus resultados. As Fases 10 e 11
adicionarão a geração dos documentos PDF.

---

## 5. Fluxo Principal

O fluxo esperado para a visão completa do produto é apresentado a seguir. Suas etapas serão disponibilizadas de forma incremental, conforme as fases definidas no roadmap:

→ **Definição do nome, do tipo e das dimensões externas do móvel**

→ **Configuração do estilo e acabamentos frontais**

→ **Configuração dos compartimentos, conteúdos e portas**

→ **Validação das especificações**

→ **Cálculo das peças estruturais (altura, largura, profundidade, posição X, posição Y e posição Z)**

→ **Cálculo do fundo do armário (altura, largura, profundidade, posição X, posição Y e posição Z)**

→ **Cálculo das peças dos compartimentos (altura, largura, profundidade, quantidade de divisões verticais, quantidade de divisões horizontais, posição X, posição Y e posição Z)**

→ **Cálculo das peças do conteúdo de cada compartimento (altura, largura, profundidade, posição X, posição Y e posição Z)**

→ **Cálculo das peças das portas (altura, largura, profundidade, posição X, posição Y e posição Z)**

→ **Cálculo dos materiais de acabamento**

→ **Cálculo dos materiais de montagem**

→ **Visualização da lista de peças e materiais**

→ **Visualização do móvel em 2D**

→ **Visualização do móvel em 3D**

→ **Visualização do plano de corte em chapa de MDF padrão (275 cm × 185 cm)**

→ **Persistência das configurações em banco de dados**

→ **Persistência das informações do móvel em banco de dados**

→ **Geração e impressão do manual de montagem em PDF**

→ **Geração e impressão da lista de peças, da lista de materiais e do plano de corte**

---

# 6. Requisitos Funcionais

Os requisitos abaixo estão organizados pela primeira fase em que deverão estar
disponíveis. As fases posteriores deverão manter as funcionalidades já entregues.

### Fase 1 — Configurações (backend)

#### RF01 — Criar configurações de armário

O backend deverá permitir definir configurações reutilizáveis para os estilos de
armário, incluindo compartimentos, portas, ocupações e relações espaciais.

#### RF02 — Validar configurações

O backend deverá rejeitar configurações incompletas, inconsistentes ou com
relações espaciais inválidas, informando os erros encontrados.

#### RF03 — Persistir configurações em JSON

O backend deverá gravar e recuperar as configurações em um arquivo JSON mantido
dentro do projeto. Esse será o único mecanismo de persistência até a Fase 7.

### Fase 2 — Catálogo visual de estilos (backend e frontend)

#### RF04 — Recuperar estilos de armário

O backend deverá listar todos os estilos ativos a partir das configurações
gravadas no JSON e disponibilizar os respectivos detalhes ao frontend.

#### RF05 — Apresentar estilos em 2D

O frontend deverá apresentar em 2D todos os estilos recuperados, permitindo que
o usuário visualize suas divisões e selecione um deles. Essa representação é uma
prévia do estilo, e não a representação dimensional de um móvel calculado.

### Fase 3 — Configuração e cálculo do móvel (backend e frontend)

#### RF06 — Informar os dados do armário

O frontend deverá permitir informar nome, dimensões, estilo, acabamentos.

#### RF07 — Validar as especificações do móvel

O sistema deverá validar os dados informados e apresentar mensagens que
identifiquem as inconsistências e os campos que precisam ser corrigidos.

#### RF08 — Calcular peças e materiais

O backend deverá calcular as peças estruturais e dos componentes, incluindo
laterais, base, topo, fundo, compartimentos, gavetas e portas, além dos
materiais de acabamento, montagem e ferragens.

#### RF09 — Calcular dimensões e posições

O backend deverá determinar as dimensões, a espessura e as coordenadas X, Y e Z
de cada peça necessária às representações do móvel. As dimensões devem se baser nas configurações no tipo de móvel e estilo selecionado.

#### RF10 — Manter o cálculo sem persistência

Até a conclusão da Fase 8, os dados informados para o móvel e os resultados
calculados não deverão ser gravados em banco de dados. Eles poderão permanecer
somente na requisição em processamento ou no estado temporário do frontend.

### Fase 4 — Resultados do cálculo (backend e frontend)

#### RF11 — Apresentar a lista de peças

O sistema deverá apresentar uma lista consolidada contendo nome, finalidade,
quantidade, altura, largura, profundidade, espessura e posicionamento X, Y e Z.

#### RF12 — Apresentar as demais informações geradas

O sistema deverá apresentar a lista estimada de materiais, as ferragens e a área
total de MDF calculada para o móvel.

### Fase 5 — Representação 2D do móvel (backend e frontend)

#### RF13 — Gerar e apresentar o móvel em 2D

O backend deverá fornecer a geometria calculada e o frontend deverá representar
em 2D o móvel, suas peças e divisões internas conforme as dimensões informadas.

### Fase 6 — Representação 3D do móvel (backend e frontend)

#### RF14 — Gerar e apresentar o móvel em 3D

O backend deverá fornecer a geometria calculada e o frontend deverá permitir
visualizar, rotacionar, aproximar e inspecionar interna e externamente o móvel.

### Fase 7 — Plano de corte (backend e frontend)

#### RF15 — Gerar o plano de corte

O sistema deverá distribuir as peças em uma ou mais chapas padrão de MDF de
275 cm × 185 cm, respeitando as restrições de corte definidas. Deve haver um espaçamento de 5 milimentros entre cada peça por conta de perda que ocorre nos cortes.

#### RF16 — Apresentar o plano de corte e seus indicadores

O frontend deverá apresentar a posição das peças, a quantidade de chapas e os
percentuais de aproveitamento e desperdício.

### Fase 8 — CRUD de configurações (backend e frontend)

#### RF17 — Gerenciar configurações em banco de dados

O sistema deverá permitir criar, listar, consultar, alterar, ativar, inativar e
excluir configurações utilizando banco de dados.

#### RF18 — Migrar as configurações iniciais

O sistema deverá disponibilizar uma forma controlada e idempotente de importar
para o banco as configurações existentes no arquivo JSON.

### Fase 9 — CRUD de móveis (backend e frontend)

#### RF19 — Salvar móvel

O sistema deverá armazenar as especificações do móvel, a versão da configuração
utilizada e os resultados gerados pelo cálculo.

#### RF20 — Consultar móveis

O sistema deverá permitir listar e recuperar móveis anteriormente armazenados.

#### RF21 — Editar e recalcular móvel

O sistema deverá permitir alterar um móvel salvo e recalcular suas peças,
materiais, representações e plano de corte.

#### RF22 — Excluir móvel

O sistema deverá permitir excluir um móvel armazenado, observando as regras de
integridade e o comportamento de exclusão definido pela aplicação.

### Fase 10 — PDF do plano de corte e das listas (backend e frontend)

#### RF23 — Gerar PDF para fabricação

O sistema deverá gerar um PDF contendo o plano de corte, a lista de peças e a
lista de materiais, correspondente à versão atual do móvel.

#### RF24 — Disponibilizar o PDF para impressão

O frontend deverá permitir visualizar, baixar e imprimir o PDF de fabricação.

### Fase 11 — PDF do manual de montagem (backend e frontend)

#### RF25 — Gerar manual de montagem

O sistema deverá gerar um manual com a sequência e as informações necessárias
para a montagem do móvel.

#### RF26 — Disponibilizar o manual em PDF

O frontend deverá permitir visualizar, baixar e imprimir o PDF do manual de
montagem.

---

# 7. Regras de Negócio

### Regras transversais

### RN01 — Identificação das entidades persistidas

Toda configuração deverá possuir uma identificação única. A partir da Fase 9,
todo móvel persistido também deverá possuir uma identificação única e um nome.

### RN02 — Tipo de móvel do escopo inicial

No escopo inicial, somente móveis do tipo **armário** poderão ser configurados.

### RN03 — Estilos de armário permitidos

Todo armário deverá ser classificado em um dos seguintes estilos: **armário multiuso**, **guarda-roupa** ou **armário aéreo**.

### RN04 — Dimensões externas obrigatórias

Todo armário deverá possuir altura, largura e profundidade informadas e válidas antes do cálculo das peças.

### RN05 — Unidade das dimensões

As dimensões do móvel e das peças deverão ser calculadas e armazenadas em centímetros (cm).

### RN06 — Unidade das espessuras especiais

As espessuras do fundo do armário e fundo das gavetas deverão ser informadas em milímetros (mm).

### RN07 — Acabamentos frontais

A existência de acabamento frontal superior e de acabamento frontal inferior deverá ser definida individualmente pelas opções **Sim** ou **Não**.

### RN08 — Estrutura interna do armário

Os compartimentos internos deverão estar associados ao armário, e o conteúdo de cada compartimento deverá permanecer associado ao compartimento em que foi configurado.

### RN09 — Conteúdos permitidos nos compartimentos

Os compartimentos poderão conter prateleiras, divisões verticais, gavetas, cabideiros e áreas livres, conforme a configuração do projeto. Cada compartimento pode ter apenas um tipo de conteúdo.

### RN10 — Configuração dos componentes internos

Gavetas, cabideiros, divisões verticais e áreas livres deverão respeitar os espaços disponíveis de acordo com o respectivo compartimento.

### RN11 — Configuração das portas

As portas deverão ser calculadas de acordo com a quantidade, as dimensões e a disposição definidas no projeto.

### RN12 — Validação anterior ao cálculo

O cálculo das peças somente poderá ser executado após a validação das dimensões e das configurações do armário.

### RN13 — Tratamento de configurações inválidas

Quando uma configuração for inválida deverá ser apresentada uma mensagem explicando a inconsistência e o cálculo das peças não deve ser iniciado.

### RN14 — Composição das peças estruturais

O cálculo estrutural deverá considerar, conforme a configuração do armário, laterais, base, topo, fundo e compartimentos.

### RN15 — Informações obrigatórias das peças

Cada peça calculada deverá possuir nome, finalidade, altura, largura, profundidade, espessura e posicionamento nos eixos X, Y e Z.

### RN16 — Origem da lista de peças

A lista consolidada de peças deverá ser gerada exclusivamente a partir da configuração validadas de acordo com o estilo de armário  e tipo de móvel selecionado.

### RN17 — Materiais considerados

A lista estimada de materiais deverá considerar os materiais de acabamento, os materiais de montagem e as ferragens necessárias ao projeto.

### RN18 — Cálculo da área de MDF

A área total de MDF utilizada deverá ser calculada a partir das dimensões(largura e altura) e quantidades das peças geradas para o armário. Deverá ser incluído 5mm entre cada peça por conta dos cortes realizados na chapa.

### RN19 — Chapa padrão do plano de corte

O plano de corte deverá considerar como padrão a chapa de MDF com dimensões de **275 cm × 185 cm**.

### RN20 — Distribuição inicial do plano de corte

Na Fase 7, todas as peças deverão ser posicionadas dentro dos limites das chapas.
A distribuição das peças deverá buscar a redução do desperdício e da quantidade de chapas utilizadas.

### RN21 — Indicadores do plano otimizado

O plano de corte otimizado deverá informar a quantidade de chapas utilizadas, a posição das peças e os percentuais de aproveitamento e desperdício.
### RN22 — Consistência após alterações

Sempre que uma configuração do projeto for alterada, as peças, os materiais, a área utilizada e o plano de corte deverão ser recalculados antes de serem considerados atuais.

### RN23 — Persistência do projeto

Até a conclusão da Fase 8, os dados e resultados do móvel serão transitórios. A
partir da Fase 9, o móvel salvo deverá manter associadas suas especificações, a
versão da configuração utilizada, suas peças, materiais e plano de corte.

### RN24 — Fonte das representações visuais

As visualizações em 2D e 3D deverão utilizar as dimensões e as posições das peças resultantes do mesmo cálculo validado do projeto.

### Regras das entregas evolutivas

### RN25 — Persistência inicial das configurações

Até a conclusão da Fase 7, o arquivo JSON dentro do projeto será a fonte de
verdade das configurações. A gravação deverá ser atômica e preservar um JSON
válido mesmo em caso de falha durante a atualização.

### RN26 — Migração das configurações

Na Fase 8, a importação do JSON não poderá duplicar configurações já existentes
no banco. Depois da migração, o banco de dados será a fonte de verdade e o JSON
permanecerá apenas como carga inicial ou recurso de desenvolvimento.

### RN27 — Geração do manual de montagem

O manual de montagem deverá ser gerado a partir das peças, dimensões, posições, materiais e configurações do projeto validado.

### RN28 — Documentos para exportação e impressão

Somente moveis persistidos em banco de dados poderão ser exportados em PDF ou impressos.

---

# 8. Modelo Conceitual

O agregado principal do domínio será o **Móvel**.

As configurações serão modelos fixos, reutilizáveis e independentes dos móveis.
Elas definirão a organização de compartimentos e portas aplicável a cada combinação de tipo e estilo de móvel.

Como as representações abaixo serão utilizadas como referência para o código
Python, serão adotadas as seguintes convenções: classes e enums em `PascalCase`,
atributos em `snake_case`, membros de enums em `UPPER_SNAKE_CASE`, coleções com
`list[Tipo]` e atributos opcionais com `Tipo | None`.

## 8.1 Configuração

### Configuracao

Representa um modelo reutilizável de organização de um móvel.

```text
id: int
tipo: TipoMovel
estilo: EstiloMovel
ativo: bool
detalhes: list[DetalheConfiguracao]
```

### DetalheConfiguracao

Representa o posicionamento espacial e organização dos compartimentos e portas dentro do móvel.

```text
id: int
configuracao: Configuracao
tipo: TipoConfiguracao
percentual_ocupacao_vertical: float
percentual_ocupacao_horizontal: float
em_cima_de: DetalheConfiguracao | None
embaixo_de: DetalheConfiguracao | None
a_direita_de: DetalheConfiguracao | None
a_esquerda_de: DetalheConfiguracao | None
```

Uma `Configuracao` possui um ou mais detalhes, e cada
`DetalheConfiguracao` pertence a exatamente uma configuração. As quatro
referências espaciais são autorrelacionamentos opcionais.

## 8.2 Objetos de valor

### Dimensao

```text
altura_cm: float
largura_cm: float
profundidade_cm: float
espessura_mm: float
```

`Dimensao` será utilizada para agrupar as medidas de móveis, compartimentos e
peças. Quando uma medida não se aplicar ao objeto, sua obrigatoriedade deverá
ser definida pelas regras da respectiva classe.

### Posicao3D

```text
x: float
y: float
z: float
```

## 8.3 Móvel e especializações

### Movel

```text
id: int
dimensao total: Dimensao
tipo: TipoMovel
```

### Armario

`Armario` herda de `Movel` e acrescenta:

```text
estilo: EstiloMovel
pecas_estruturantes: list[Peca]
pecas_de_acabamento: list[Peca]
compartimentos: list[Compartimento]
gavetas: list[Gaveta]
portas: list[Porta]
```

## 8.4 Peças e componentes

### Peca

Representa uma peça de madeira MDF que será produzida e posicionada no móvel.

```text
id: int
dimensao: Dimensao
posicao: Posicao3D
finalidade: Finalidade
agrupador: Componente | None
```

### Componente

Representa um agrupador de peças. É a classe-base de compartimentos, gavetas, estruturas, portas. Ela serve para abstrair as referências ao objeto pai na entidade Peca.  

```text
id: int
nome: str
armario: Armario
pecas: list[Peca]
materiais: list[Material]
```

### Compartimento

`Compartimento` herda de `Componente` e acrescenta:

```text
dimensao: Dimensao
ordenacao_horizontal: OrdenacaoHorizontal
ordenacao_vertical: OrdenacaoVertical
conteudo: TipoConteudo
```

Para o compartimento, as dimensões relevantes são altura e largura.

### Gaveta

`Gaveta` herda de `Componente` e acrescenta:

```text
compartimento: Compartimento
```

### Estrutura

`Estrutura` herda de `Componente` e acrescenta:

```text
```

### Porta

`Porta` herda de `Componente` e acrescenta:
```text
```

## 8.5 Materiais

### Material

```text
tipo: TipoMaterial
quantidade: int
```

## 8.6 Enumerações

### TipoConfiguracao

```text
COMPARTIMENTO
PORTA
```

### TipoMovel

```text
ARMARIO
```

### EstiloMovel

```text
MULTIUSO
GUARDA_ROUPA
ARMARIO_AEREO
```

### Finalidade

```text
LATERAL_DIREITA
LATERAL_ESQUERDA
TOPO
BASE
ACABAMENTO_FRONTAL_SUPERIOR
ACABAMENTO_FRONTAL_INFERIOR
PRATELEIRA
DIVISAO_VERTICAL
DIVISAO_HORIZONTAL
FRENTE_DE_GAVETA
LATERAL_ESQUERDA_DA_GAVETA
LATERAL_DIREITA_DA_GAVETA
TRASEIRA_DA_GAVETA
FUNDO
```

### OrdenacaoHorizontal

```text
DIREITA_PARA_ESQUERDA
ESQUERDA_PARA_DIREITA
```

### OrdenacaoVertical

```text
BAIXO_PARA_CIMA
CIMA_PARA_BAIXO
```

### TipoConteudo

```text
GAVETA
CABIDEIRO
AREA_LIVRE
```

### TipoMaterial

```text
MACANETA
PUXADOR
DOBRADICA
PREGO
PARAFUSO
```

## 8.7 Relações conceituais principais

```text
Configuracao       1 ─── 1..* DetalheConfiguracao
DetalheConfiguracao 1 ─── 1    Configuracao (associação obrigatória)

Movel              <|── Armario
Componente         <|── Compartimento
Componente         <|── Gaveta
Componente         <|── Porta
Componente         <|── Estrutura
{especialização completa e disjunta: todo Componente possui exatamente um desses tipos}

Armario            1 ─── 1..* Compartimento (associação obrigatória)
Armario            1 ─── 0..* Gaveta
Armario            1 ─── 0..* Porta
Armario            1 ─── 1..* Peca
Armario            1 ─── 1..* Material

Compartimento      1 ─── 0..* Gaveta
Componente         1 ─── 1..* Peca
Componente         1 ─── 1.* Material
Porta              1 ─── 1    Peca
Porta              1 ─── 0..* Material
```

`Componente` representa uma classe-base abstrata. Sua especialização é total,
pois todo componente deve ser um `Compartimento`, `Porta`, `Estrutura`  ou uma `Gaveta`,
e disjunta, pois um mesmo componente não pode pertencer simultaneamente a mais
de um desses tipos. Cada `Compartimento`, `Porta`, `Estrutura`  ou  `Gaveta` corresponde
obrigatoriamente a um único `Componente`.

Todo `Armario` deve possuir pelo menos um `Compartimento`, podendo possuir
vários, e cada compartimento deve pertencer a exatamente um armário. O vínculo
entre um componente e suas peças será representado pela coleção
`Componente.pecas`. Cada peça de componente deverá pertencer a um único
componente. Uma peça de gaveta, por exemplo, será associada à `Gaveta`; seu
compartimento e seu armário poderão ser obtidos por meio da cadeia
`Peca → Gaveta → Compartimento → Armario`, sem duplicação de referências na
peça.

---

# 9. Arquitetura

O projeto deverá adotar **Clean Architecture**, com o domínio e os casos de uso
independentes de frameworks web, banco de dados, renderização 3D e mecanismos de
exportação. A organização abaixo considera um repositório único para o backend,
o frontend e os recursos de execução local.

Para o backend Python será utilizado o padrão **src layout**. O pacote importável
será chamado `marcenaria_digital_api`, enquanto o diretório raiz do repositório
poderá manter o nome `marcenaria_digital`.

## 9.1 Estrutura de diretórios

```text
marcenaria-digital/                                     [Fase 1]
├── backend/                                            [Fase 1]
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── src/                                            [Fase 1]
│   │   └── marcenaria_digital_api/                     [Fase 1]
│   │       ├── __init__.py
│   │       ├── domain/                                 [Fase 1]
│   │       │   ├── entities/                           [Fase 1]
│   │       │   │   ├── configuracao/                   [Fase 1]
│   │       │   │   │   ├── configuracao.py
│   │       │   │   │   ├── detalhes_configuracao.py
│   │       │   │   ├── movel/                         [Fase 3]
│   │       │   │   │   ├── movel.py
│   │       │   │   │   ├── componente.py
│   │       │   │   │   ├── material.py
│   │       │   │   │   ├── peca.py
│   │       │   │   │   ├── compartimento.py
│   │       │   │   │   ├── gaveta.py
│   │       │   │   │   ├── estrutura.py
│   │       │   │   │   ├── porta.py
│   │       │   │   │   └── armario.py
│   │       │   ├── value_objects/                      [Fase 3]
│   │       │   │   ├── dimensao.py
│   │       │   │   └── posicao_3d.py
│   │       │   ├── enums/                              [Fase 1]
│   │       │   │   ├── tipo_movel.py
│   │       │   │   ├── finalidade.py
│   │       │   │   ├── ordenacao_horizontal.py
│   │       │   │   ├── conteudo.py
│   │       │   │   ├── tipo_material.py
│   │       │   │   ├── estilo_movel.py
│   │       │   │   └── ordenacao_vertical.py
│   │       │   ├── services/                           [Fase 1]
│   │       │   │   ├── configuracao_movel.py
│   │       │   │   ├── validacao.py
│   │       │   │   ├── calculo_pecas.py
│   │       │   └── exceptions/                         [Fase 1]
│   │       │       └── configuracao_exception.py
│   │       │       └── movel_exception.py
│   │       ├── application/                            [Fase 1]
│   │       │   ├── dto/                                [Fase 1]
│   │       │   │   ├── armario_input.py
│   │       │   │   ├── armario_output.py
│   │       │   │   ├── configuracao_input.py
│   │       │   │   ├── configuracao_output.py
│   │       ├── infrastructure/                         [Fase 1]
│   │       │   ├── persistence/                        [Fase 1]
│   │       │   │   ├── json/                           [Fase 1]
│   │       │   │   │   ├── configuracoes.json
│   │       │   │   │   └── configuracao_repository.py
│   │       │   │   └── database/                       [Fase 8]
│   │       │   │       ├── database.py
│   │       │   │       ├── models.py
│   │       │   │       └── repositories.py
│   │       │   └── documents/                          [Fase 10]
│   │       │       ├── gerador_documento_fabricacao.py
│   │       │       └── gerador_manual_montagem.py
│   │       ├── presentation/                           [Fase 1]
│   │       │   └── api/                                [Fase 1]
│   │       │       ├── main.py
│   │       │       ├── routes/                         [Fase 1]
│   │       │       │   ├── armario.py
│   │       │       │   └── configuracao.py
│   │       │       └── exception_handlers.py
│   │       └── config.py
│   └── Dockerfile
├── specs/                                              [Fase 1]
│   └── fase-1/                                         [Fase 1]
│       ├── requisitos.json
│       ├── dominio.json
│       ├── api.json
│       ├── persistencia.json
│       └── aceite.json
├── frontend/                                           [Fase 2]
│   ├── src/                                            [Fase 2]
│   └── Dockerfile
├── .env.example
├── compose.yaml
├── PRD.md
└── README.md
```

Os arquivos `__init__.py` dos subpacotes foram omitidos da árvore para facilitar
a leitura, mas deverão existir nos diretórios Python importáveis.

Os marcadores são aplicados exclusivamente aos diretórios e identificam a
primeira fase em que cada um deverá ser criado. Arquivos e classes não recebem
marcadores, ainda que sejam necessários apenas em fases posteriores.
As especificações SDD serão mantidas em `specs/`, separadas por fase. Cada
diretório de fase deverá conter somente as especificações do respectivo escopo,
em arquivos JSON objetivos e versionados.
Na Fase 1 será criado apenas o adaptador JSON de configurações. O Alembic e a
persistência em banco serão adicionados na Fase 8 para as configurações e
ampliados na Fase 9 para os móveis. Os adaptadores de documentos serão criados
nas Fases 10 e 11. O cálculo do plano de corte permanecerá independente de sua
posterior geração como documento.

A estrutura será organizada em subpacotes de acordo com a responsabilidade de
cada elemento. Dentro deles, entidades, casos de uso, rotas e adaptadores serão
separados por contexto funcional, mantendo no mesmo arquivo os elementos que
possuírem alta coesão. Um arquivo deverá ser dividido quando o crescimento gerar
responsabilidades distintas ou dificultar sua manutenção.

Diretórios vazios não deverão ser criados antecipadamente. Os elementos marcados
como fases futuras deverão permanecer apenas como referência neste documento até
que as respectivas funcionalidades sejam implementadas.

## 9.2 Responsabilidades das camadas

### `domain`

Conterá o núcleo das regras de negócio da marcenaria. O subpacote `entities`
agrupará as entidades de configuração e de móvel; `value_objects` conterá
dimensões e posições; `enums` reunirá as classificações do domínio; `services`
implementará a configuração do móvel, suas validações e o cálculo das peças; e
`exceptions` representará os erros próprios dessas operações.

Essa camada será independente de frameworks, mecanismos de persistência e
detalhes da API. Por isso, não poderá importar módulos de `application`,
`infrastructure` ou `presentation`.

### `application`

Conterá os contratos de entrada e saída das operações da aplicação. O subpacote
`dto` reunirá os dados de entrada e saída de armários e configurações. Esses DTOs
também serão utilizados pela API para validação estrutural e serialização,
evitando a criação de schemas equivalentes em `presentation` nesta etapa.

Os DTOs não deverão conter regras de negócio nem elementos específicos de HTTP.
A camada poderá depender de `domain`, mas não de implementações presentes em
`infrastructure` nem de detalhes de `presentation`. Novos módulos de aplicação
serão adicionados somente quando a implementação dos respectivos casos de uso os
exigir.

### `infrastructure`

Conterá os adaptadores técnicos usados para integrar a aplicação a recursos
externos. Na Fase 1, `infrastructure.persistence.json` implementará o repositório
de configurações baseado no arquivo JSON do projeto.

Na Fase 8, `infrastructure.persistence.database` conterá a configuração do
banco, os modelos do ORM e os repositórios de configurações. Na Fase 9, esses
adaptadores serão ampliados para os móveis e resultados calculados. Os modelos
de persistência não deverão substituir as entidades de `domain`; os repositórios
serão responsáveis pela conversão entre essas representações quando necessária.

Nas Fases 10 e 11, `infrastructure.documents` conterá os adaptadores para gerar,
respectivamente, o PDF de fabricação e o manual de montagem. Essa geração
documental não deverá conter nem substituir as regras responsáveis pelo cálculo
das peças e do plano de corte.

### `presentation`

Conterá a API REST. `api.main` será o ponto de entrada e de composição da
aplicação; `api.routes` disponibilizará as operações de armário e configuração;
e `api.exception_handlers` converterá as exceções da aplicação em respostas
HTTP adequadas.

As rotas utilizarão diretamente os DTOs de `application` como contratos de
entrada e saída. Elas deverão se limitar ao protocolo HTTP, à chamada das
operações da aplicação e à construção da resposta, sem implementar regras de
negócio.

### `config`

Centralizará a leitura das configurações de ambiente e de logging utilizadas
pelo backend. Segredos e credenciais não deverão ser versionados; o repositório
deverá manter somente `.env.example` com as variáveis necessárias e valores não
sensíveis.


## 9.3 Regra de dependência

As dependências entre as camadas deverão apontar para o centro da aplicação:

```text
presentation ──→ application ──→ domain
infrastructure ──→ application ──→ domain
```

`domain` não dependerá de nenhuma outra camada. `application` conhecerá apenas
o domínio e seus próprios contratos. A composição das implementações concretas
será realizada no ponto de entrada da API.

---

# 10. API

A API deverá seguir o padrão REST, possuir versionamento explícito e manter
contratos compatíveis ao longo das fases. Em caso de erros de calculo ou erros de execução deverá ser escrito um arquivo de log com as infomrações do erro. 

Os caminhos abaixo são a referência
inicial e poderão ser refinados sem alterar as responsabilidades definidas:

```text
POST   /api/v1/configuracoes                         [Fase 1 — grava no JSON]
GET    /api/v1/configuracoes                         [Fase 2]
GET    /api/v1/configuracoes/{id}                    [Fase 2]
GET    /api/v1/estilos-armario                       [Fase 2]

POST   /api/v1/moveis/calculos                       [Fase 3 — operação sem persistência]
POST   /api/v1/moveis/representacoes-2d              [Fase 5 — operação sem persistência]
POST   /api/v1/moveis/representacoes-3d              [Fase 6 — operação sem persistência]
POST   /api/v1/planos-corte                          [Fase 7 — operação sem persistência]

PUT    /api/v1/configuracoes/{id}                    [Fase 8 — banco de dados]
DELETE /api/v1/configuracoes/{id}                    [Fase 8 — banco de dados]
POST   /api/v1/configuracoes/importacoes/json         [Fase 8]

POST   /api/v1/moveis                                [Fase 9]
GET    /api/v1/moveis                                [Fase 9]
GET    /api/v1/moveis/{id}                           [Fase 9]
PUT    /api/v1/moveis/{id}                           [Fase 9]
DELETE /api/v1/moveis/{id}                           [Fase 9]

GET    /api/v1/moveis/{id}/documentos/fabricacao.pdf [Fase 10]
GET    /api/v1/moveis/{id}/manual-montagem.pdf       [Fase 11]
```

As operações das Fases 3, 5, 6 e 7 deverão receber os dados necessários no
corpo da requisição e devolver o resultado sem pressupor que exista um móvel
salvo. A partir da Fase 9, também poderão operar sobre um identificador persistido.

---

# 11. Persistência

### Fases 1 a 7 — Arquivo JSON

As configurações deverão ser armazenadas em um arquivo JSON dentro do projeto.
O arquivo deverá possuir estrutura versionada, codificação UTF-8, identificadores
estáveis e validação antes da leitura ou gravação. Ele será a fonte de verdade
das configurações durante essas fases.

As informações preenchidas para um móvel, as peças calculadas, as listas, as
representações e o plano de corte não deverão ser persistidos nesse período.

### Fase 8 — Banco de dados para configurações

O CRUD de configurações deverá utilizar **PostgreSQL**. Uma rotina idempotente
deverá importar as configurações iniciais do JSON. Após essa transição, o banco
será a fonte de verdade e o JSON poderá continuar no repositório como carga
inicial e referência para ambientes locais.

### Fase 9 em diante — Banco de dados para móveis

O PostgreSQL também deverá armazenar os móveis, suas especificações e os
resultados necessários para recuperação posterior. Dados relacionais poderão ser
armazenados em tabelas convencionais, enquanto estruturas complexas ou snapshots
da configuração utilizada poderão usar JSONB. A estratégia deverá permitir
recuperar um móvel completo e identificar a configuração que originou o cálculo.

---

# 12. Interface Web

A aplicação deverá possuir frontend independente da API.

Tecnologias preferenciais e evolução da persistência:

```text
Angular
   |
   | REST/JSON
   ↓
Fast API
   |
   ↓
Application
   |
   ↓
Domain
   |
   ↓
Infrastructure
   |
   ↓
JSON (Fases 1 a 7)
   |
   └──→ PostgreSQL (Fases 8 a 11)
```

---

# 13. Visualização 3D

Para a representação tridimensional deverá ser considerada uma biblioteca WebGL.

Tecnologia preferencial:

```text
Three.js
```

A API deverá fornecer as dimensões e propriedades geométricas necessárias para que o frontend construa a representação 3D.

A responsabilidade de renderização deverá permanecer no frontend.

---

# 14. Plano de Corte

Deve ser diferenciada a **lista de peças** do **plano de corte**.

A lista de peças informa:

```text
quais peças precisam ser produzidas
```

O plano de corte deverá informar:

```text
como distribuir essas peças nas chapas de MDF
```

Na Fase 7 deverá ser implementado um algoritmo de **2D Cutting Stock / 2D Bin
Packing**. A primeira versão poderá usar uma heurística sem garantia de solução
global ótima, mas deverá posicionar todas as peças em chapas válidas, considerando:

* largura da chapa;
* altura da chapa;
* espessura;
* sentido do veio;
* largura da serra;
* margem da chapa;
* possibilidade de rotação da peça;
* aproveitamento;
* desperdício.

O resultado deverá informar também:

* quantidade de chapas necessárias;
* posição de cada peça;
* percentual de aproveitamento;
* percentual de desperdício.

---

# 15. Requisitos Não Funcionais

### RNF01 — API

A API deverá utilizar Python com FastAPI e expor documentação OpenAPI/Swagger.

### RNF02 — Banco de dados

A persistência inicial das configurações deverá utilizar JSON. A partir da Fase
8, a persistência relacional deverá utilizar PostgreSQL.

### RNF03 — Containerização

Backend e demais componentes deverão permitir execução através de Docker.

### RNF04 — Separação de responsabilidades

Regras de negócio não deverão ser implementadas diretamente nos controllers.

### RNF05 — Versionamento

A API deverá utilizar versionamento explícito.

### RNF08 — Precisão

Cálculos dimensionais deverão evitar arredondamentos que possam produzir medidas inválidas para fabricação.

### RNF08 — Integridade do arquivo JSON

A leitura e a gravação das configurações deverão validar o schema do arquivo e
evitar corrupção ou gravação parcial.

### RNF09 — Compatibilidade evolutiva

A substituição do repositório JSON pelo PostgreSQL não deverá alterar as regras
de domínio nem exigir mudanças incompatíveis nos consumidores da API.

---

# 16. Critérios Gerais de Aceite

Cada fase deverá ser demonstrável isoladamente e integrada às anteriores. Uma
fase será considerada concluída quando:

1. todos os requisitos funcionais atribuídos à fase estiverem implementados;
2. os critérios específicos descritos no roadmap forem atendidos;
3. os contratos da API estiverem documentados no OpenAPI;
4. o fluxo principal da fase puder ser executado sem depender de funcionalidades
   previstas apenas para fases posteriores;
5. não houver regressão nos critérios de aceite das fases já concluídas.

Ao final da Fase 7, haverá um fluxo funcional completo, porém transitório, desde
a seleção do estilo até o plano de corte. Ao final da Fase 9, o produto passará
a salvar e recuperar configurações e móveis. A visão integral deste PRD será
atingida ao final da Fase 11.

---

# 17. Fora do Escopo das 11 Fases

Não fazem parte das 11 fases definidas neste PRD:

* orçamento financeiro completo;
* integração com lojas;
* compra automática de MDF;
* integração com máquinas CNC;
* geração de G-code;
* controle de estoque;
* marketplace;
* realidade aumentada;
* inteligência artificial generativa para criação automática do móvel.

Esses recursos poderão ser avaliados após estabilização do fluxo principal.

---

# 18. Roadmap de Implementação

As fases são sequenciais e cumulativas. Backend e frontend indicam onde deverá
existir implementação nova; não eliminam a necessidade de testes e integração.

### Fase 1 — Criação das configurações (backend)

**Objetivo:** modelar, validar, gravar e recuperar as configurações dos estilos
de armário.

**Persistência:** arquivo JSON dentro do projeto.

**Critérios de aceite:**

* uma configuração válida é serializada e recuperada sem perda de dados;
* uma configuração inválida é rejeitada com mensagem identificável;
* o arquivo permanece válido após inclusão de novas configurações;
* testes do domínio e do repositório JSON são executados sem banco de dados.

### Fase 2 — Catálogo 2D de estilos (backend e frontend)

**Objetivo:** recuperar todas as configurações ativas e apresentar uma prévia 2D
de cada estilo de armário.

**Critérios de aceite:**

* todos os estilos ativos do JSON são retornados pela API;
* o frontend apresenta cada estilo em 2D e permite selecioná-lo;
* estados de carregamento, lista vazia e erro são tratados;


### Fase 3 — Cálculo das peças do móvel (backend e frontend)

**Objetivo:** receber as informações do móvel e o estilo selecionado, validar a
entrada e calcular peças, materiais, dimensões e posições.

**Persistência:** nenhuma informação do móvel será armazenada.

**Critérios de aceite:**

* o frontend permite preencher os dados necessários ao cálculo;
* entradas inválidas não iniciam o cálculo e apresentam mensagens úteis;
* entradas válidas produzem o calculo das dimensões das peças coerentes com o estilo selecionado;
* repetir a mesma entrada produz o mesmo resultado;
* nenhuma tabela ou arquivo de móveis é criado.

### Fase 4 — Lista de peças e demais resultados (backend e frontend)

**Objetivo:** recuperar e apresentar os resultados produzidos na Fase 3.

**Critérios de aceite:**

* a lista consolidada apresenta quantidade, dimensões, espessura, finalidade e posição de cada peça;
* materiais, ferragens e área total de MDF são apresentados;
* o frontend trata listas vazias e erros de cálculo;
* os dados permanecem transitórios.

### Fase 5 — Representação 2D do móvel (backend e frontend)

**Objetivo:** apresentar a representação dimensional 2D do móvel calculado.

**Critérios de aceite:**

* a geometria utiliza o mesmo resultado validado que originou a lista de peças;
* o desenho apresenta estrutura, divisões, componentes e portas nas posições calculadas;
* alterações de dimensões seguidas de novo cálculo atualizam a representação.

### Fase 6 — Representação 3D do móvel (backend e frontend)

**Objetivo:** apresentar a representação tridimensional do móvel calculado.

**Critérios de aceite:**

* a geometria 3D corresponde às dimensões e posições das peças calculadas;
* o usuário pode rotacionar, aplicar zoom e inspecionar o móvel;
* a renderização permanece responsabilidade do frontend, preferencialmente com Three.js.

### Fase 7 — Plano de corte (backend e frontend)

**Objetivo:** calcular e apresentar a distribuição das peças em chapas padrão de MDF.

**Critérios de aceite:**

* todas as peças são posicionadas dentro dos limites de chapas de 275 cm × 185 cm;
* sobreposições e cortes impossíveis são detectados;
* são apresentados quantidade de chapas, aproveitamento e desperdício;
* o plano visual permite identificar cada peça.

### Fase 8 — CRUD de configurações com banco de dados (backend e frontend)

**Objetivo:** substituir o JSON como fonte de verdade por um CRUD de configurações
em PostgreSQL.

**Critérios de aceite:**

* o usuário pode criar, consultar, listar, alterar, ativar, inativar e excluir configurações;
* a importação do JSON é idempotente e preserva identificadores ou sua equivalência;
* as fases anteriores passam a ler configurações pelo repositório de banco;
* regras de integridade impedem configurações inconsistentes.

### Fase 9 — CRUD de móveis com banco de dados (backend e frontend)

**Objetivo:** persistir e gerenciar os móveis e seus resultados.

**Critérios de aceite:**

* o usuário pode criar, consultar, listar, editar e excluir móveis;
* um móvel recuperado mantém a versão da configuração usada no cálculo;
* alterações relevantes invalidam resultados antigos e exigem recálculo;
* peças, materiais, representações e plano de corte podem ser reconstruídos ou recuperados.

### Fase 10 — PDF do plano de corte e das listas (backend e frontend)

**Objetivo:** gerar um documento de fabricação com plano de corte, lista de peças
e lista de materiais.

**Critérios de aceite:**

* o PDF corresponde à versão atual do móvel e identifica o projeto;
* todas as peças e materiais apresentados na interface constam no documento;
* o plano de corte permanece legível e identifica chapas e peças;
* o frontend permite visualizar, baixar e imprimir o arquivo.

### Fase 11 — PDF do manual de montagem (backend e frontend)

**Objetivo:** gerar e disponibilizar o manual de montagem do móvel.

**Critérios de aceite:**

* o manual utiliza as peças, posições, materiais e configuração atuais;
* as etapas de montagem possuem ordem e identificação claras;
* o documento referencia as peças de forma consistente com a lista de fabricação;
* o frontend permite visualizar, baixar e imprimir o arquivo.

---

# 19. Diretriz de Evolução

O projeto deverá manter uma separação clara entre três conceitos:

**Projeto do móvel:** representa aquilo que o usuário deseja construir.

**Engenharia do móvel:** transforma as especificações em peças e materiais necessários.

**Otimização de corte:** determina como as peças serão distribuídas fisicamente nas chapas.

Essa separação permitirá evoluir futuramente o sistema para outros tipos de móveis sem acoplar as regras de negócio ao algoritmo de otimização de chapas.
