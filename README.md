# Metal Bands API

API REST desenvolvida com **FastAPI**, **SQLAlchemy** e **SQLite** para gerenciamento (CRUD) de um catálogo de bandas de Heavy Metal e subgêneros, gerenciada com **uv** e documentada com **Scalar**.

---

## Tecnologias

- **Python 3.11+**
- **FastAPI** — Framework web e validação de dados com Pydantic
- **SQLAlchemy** — ORM e gerenciamento de sessões com banco de dados
- **SQLite** — Banco de dados relacional local (`metal_bands.db`)
- **Scalar (`scalar-fastapi`)** — Documentação interativa da API em `/docs`
- **uv** — Gerenciador de pacotes e ambiente virtual

---

## Estrutura do Projeto

```text
fastapi-crud/
├── .gitignore
├── pyproject.toml
├── uv.lock
├── metal_bands.db          # Criado automaticamente na primeira execução
└── src/
    └── fastapi_crud/
        ├── __init__.py
        ├── database.py     # Conexão, sessão e dependência get_db
        ├── models.py       # Modelo da tabela bands (SQLAlchemy)
        ├── schemas.py      # Schemas de entrada e saída (Pydantic)
        └── main.py         # Aplicação FastAPI, rotas CRUD e docs
```

---

## Como Executar

### 1. Clonar o repositório e instalar dependências

```bash
git clone <url-do-seu-repositorio>
cd fastapi-crud
uv sync
```

*(Caso esteja iniciando do zero: `uv init fastapi-crud && cd fastapi-crud && uv add "fastapi[standard]" sqlalchemy scalar-fastapi`)*

### 2. Iniciar o servidor de desenvolvimento

```bash
uv run fastapi dev src/fastapi_crud/main.py
```

### 3. Acessar a documentação

Abra **`http://127.0.0.1:8000`** no navegador — a rota raiz redireciona automaticamente para **`/docs`** com a interface interativa do Scalar.

---

## Endpoints Disponíveis

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` ou `/docs` | Redireciona para a documentação interativa Scalar |
| `POST` | `/bands` | Cadastra uma nova banda (`201 Created` / `409 Conflict`) |
| `GET` | `/bands` | Lista bandas com filtros opcionais (`subgenre`, `country`, `active`) |
| `GET` | `/bands/{band_id}` | Busca uma banda específica pelo ID (`404 Not Found` se não existir) |
| `PATCH` | `/bands/{band_id}` | Atualiza parcialmente os dados de uma banda |
| `DELETE` | `/bands/{band_id}` | Remove uma banda do banco de dados (`204 No Content`) |

---

## Exemplo de Payload (`POST /bands`)

```json
{
  "name": "Sepultura",
  "subgenre": "Thrash / Groove Metal",
  "country": "Brasil",
  "formed_year": 1984,
  "active": true
}
```