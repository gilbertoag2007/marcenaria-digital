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

Detalhes do tipo `COMPARTIMENTO` enviados e retornados nesses contratos incluem:

```json
{
  "quantidade_portas": 2,
  "abertura_porta": "ABERTURA VERTICAL"
}
```

`quantidade_portas` deve ser um inteiro entre 0 e 10, inclusive. Para uma
quantidade positiva, `abertura_porta` é obrigatória e aceita `ABERTURA VERTICAL`
ou `ABERTURA HORIZONTAL`. Para quantidade zero, a abertura deve ser nula.
Detalhes do tipo `PORTA` devem manter os dois atributos nulos.

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
