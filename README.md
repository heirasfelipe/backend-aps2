# 🎓 API RESTful de Gerenciamento de Eventos Acadêmicos
> **Avaliação Parcial 02 — Desenvolvimento de uma API RESTful**  
> Disciplina: Engenharia de Software / Desenvolvimento Back-End

Uma API RESTful robusta, desenvolvida com **Python**, **FastAPI** e **Pydantic**, projetada para gerenciar eventos acadêmicos (como palestras, workshops, minicursos, seminários e competições), participantes (alunos, professores, comunidade) e o fluxo completo de inscrições com controle rigoroso de vagas e regras de negócio.

---

## 📋 Sumário
1. [Objetivo e Funcionalidades](#-objetivo-e-funcionalidades)
2. [Tecnologias Utilizadas](#-tecnologias-utilizadas)
3. [Arquitetura do Projeto (MVC)](#-arquitetura-do-projeto-mvc)
4. [Instalação e Configuração](#-instalação-e-configuração)
5. [Como Executar a Aplicação](#-como-executar-a-aplicação)
6. [Documentação Interativa (Swagger & ReDoc)](#-documentação-interativa-swagger--redoc)
7. [Endpoints da API](#-endpoints-da-api)
8. [Regras de Negócio e Validações](#-regras-de-negócio-e-validações)
9. [Exemplos de Requisições e Respostas](#-exemplos-de-requisições-e-respostas)
10. [Testes Automatizados](#-testes-automatizados)
11. [Publicação no GitHub](#-publicação-no-github)

---

## 🚀 Objetivo e Funcionalidades

O projeto atende a todos os requisitos da **Avaliação Parcial 02**, contemplando:
- **Operações CRUD completas** para Eventos e Participantes via métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`).
- **Controle de Inscrições**: Inscrição de participantes em eventos com regras de vagas e duplicidade.
- **Validação estrita de dados** através do Pydantic (e-mails válidos, datas no calendário, horários, capacidade positiva, strings não vazias).
- **Tratamento semântico de erros** com os códigos de status HTTP corretos (`200`, `201`, `204`, `400`, `404`, `422`).
- **Padrão Arquitetural MVC**: separação clara de responsabilidades entre Controladores, Modelos e Serviços.
- **Armazenamento em memória**: gerenciamento dinâmico sem dependência de banco externo para fácil execução e avaliação.

---

## 🛠 Tecnologias Utilizadas

- **[Python 3.10+](https://www.python.org/)** - Linguagem de programação moderna e tipada.
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno de alta performance para criação de APIs RESTful.
- **[Pydantic v2](https://docs.pydantic.dev/)** - Modelagem de dados, parsing e validação rigorosa com tipagem estática.
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI ultrarrápido para execução da aplicação.
- **[Pytest](https://docs.pytest.org/)** & **[HTTPX](https://www.python-httpx.org/)** - Suíte de testes automatizados de integração e cobertura de regras de negócio.

---

## 🏛 Arquitetura do Projeto (MVC)

A aplicação foi estruturada respeitando a separação de responsabilidades recomendada:

```
backend aps2/
│
├── controller/                   # Controladores (Camada de Apresentação / Rotas HTTP)
│   ├── __init__.py
│   ├── evento_controller.py      # Endpoints de eventos e inscrições vinculadas
│   └── participante_controller.py# Endpoints de participantes
│
├── model/                        # Modelos (Camada de Dados e Validação Pydantic)
│   ├── __init__.py
│   ├── evento.py                 # Schemas: EventoCreate, EventoUpdate, EventoResponse
│   ├── participante.py           # Schemas: ParticipanteCreate, ParticipanteUpdate, etc.
│   └── inscricao.py              # Schemas de confirmação e detalhes de inscrições
│
├── service/                      # Serviços (Camada de Regras de Negócio)
│   ├── __init__.py
│   ├── evento_service.py         # Lógica e métricas de eventos (vagas, remoção em cascata)
│   ├── participante_service.py   # Lógica e unicidade de e-mail de participantes
│   └── inscricao_service.py      # Validação de regras de negócio de inscrições
│
├── database.py                   # Armazenamento em memória (Simulador de Banco)
├── main.py                       # Inicialização do FastAPI, CORS e inclusão de rotas
├── requirements.txt              # Dependências do projeto
├── .gitignore                    # Arquivos ignorados pelo Git
└── tests/                        # Testes Automatizados
    ├── __init__.py
    └── test_api.py               # 11 testes cobrindo CRUDs e todas as regras de negócio
```

- **Controller**: Trata as requisições HTTP, parâmetros de rota/query e delega o processamento ao Service.
- **Service**: Concentra a lógica de negócio (por exemplo: verificar se o evento tem vagas livres antes da inscrição, se o participante já está inscrito ou se a nova capacidade é válida).
- **Model**: Define os contratos de entrada e saída via Pydantic, garantindo tipos e validações sintáticas.
- **Database**: Gerencia o estado persistido em memória com identificadores autoincrementais.

---

## 💻 Instalação e Configuração

### 1. Clonar ou Acessar a Pasta do Projeto
Abra o terminal na pasta do projeto:
```bash
cd "c:\Users\felip\OneDrive\Área de Trabalho\Engenharia de Software\backend aps2"
```

### 2. Criar e Ativar o Ambiente Virtual (Recomendado)
- **No Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **No Windows (CMD):**
  ```cmd
  python -m venv .venv
  .\.venv\Scripts\activate.bat
  ```
- **No Linux/macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar as Dependências
Com o ambiente ativado, execute:
```bash
pip install -r requirements.txt
```

---

## ▶️ Como Executar a Aplicação

Você pode executar o servidor de duas maneiras:

### Opção 1: Diretamente com Python
```bash
python main.py
```

### Opção 2: Através do Uvicorn (com Live Reloading)
```bash
python -m uvicorn main:app --reload --port 8000
```

O servidor iniciará em `http://127.0.0.1:8000`.

---

## 📖 Documentação Interativa (Swagger & ReDoc)

O FastAPI gera automaticamente interfaces de documentação interativa para teste imediato de todas as rotas no navegador:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
  *Permite testar todas as rotas diretamente pelo navegador clicando em "Try it out".*
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  
  *Visualização limpa e estruturada dos modelos e especificações OpenAPI.*

---

## 📡 Endpoints da API

### 1. Eventos (`/eventos`)
| Método | Rota | Código Sucesso | Descrição |
|---|---|:---:|---|
| `POST` | `/eventos` | `201 Created` | Cadastra um novo evento acadêmico. |
| `GET` | `/eventos` | `200 OK` | Lista todos os eventos (filtro opcional `?categoria=`). |
| `GET` | `/eventos/{id}` | `200 OK` | Consulta os dados de um evento específico. |
| `PUT` | `/eventos/{id}` | `200 OK` | Atualiza os dados de um evento existente. |
| `DELETE`| `/eventos/{id}` | `204 No Content` | Remove um evento e suas inscrições associadas. |

### 2. Participantes (`/participantes`)
| Método | Rota | Código Sucesso | Descrição |
|---|---|:---:|---|
| `POST` | `/participantes` | `201 Created` | Cadastra um novo participante. |
| `GET` | `/participantes` | `200 OK` | Lista todos os participantes (filtro opcional `?curso=`). |
| `GET` | `/participantes/{id}` | `200 OK` | Consulta os dados de um participante específico. |
| `PUT` | `/participantes/{id}` | `200 OK` | Atualiza dados cadastrais de um participante. |
| `DELETE`| `/participantes/{id}` | `204 No Content` | Remove um participante e cancela suas inscrições. |

### 3. Inscrições em Eventos
| Método | Rota | Código Sucesso | Descrição |
|---|---|:---:|---|
| `POST` | `/eventos/{evento_id}/inscricoes/{participante_id}` | `201 Created` | Inscreve o participante no evento com validação de vagas. |
| `GET` | `/eventos/{evento_id}/inscricoes` | `200 OK` | Consulta todos os participantes inscritos no evento. |
| `DELETE`| `/eventos/{evento_id}/inscricoes/{participante_id}` | `204 No Content` | Cancela a inscrição de um participante no evento. |

---

## 🛡 Regras de Negócio e Validações

### Validações de Entrada (Pydantic / 422 Unprocessable Entity):
- **Título do evento**: Obrigatório, não pode ser vazio ou conter apenas espaços em branco.
- **Nome do participante**: Obrigatório, não pode ser vazio ou conter apenas espaços em branco.
- **Curso**: Obrigatório e não vazio.
- **E-mail**: Formato de e-mail estritamente validado (`user@domain.com`).
- **Capacidade do evento**: Deve ser um número inteiro estritamente maior que zero (`gt=0`).
- **Data do evento**: Formato `AAAA-MM-DD`, validando se é uma data real do calendário (impede datas impossíveis como 30 de fevereiro).
- **Horário do evento**: Formato `HH:MM`, validando horas (00-23) e minutos (00-59).

### Regras de Negócio (Service / 400 Bad Request & 404 Not Found):
1. **Inscrição em evento**:
   - Se o evento não existir: `404 Not Found` → `{"detail": "Evento não encontrado."}`
   - Se o participante não existir: `404 Not Found` → `{"detail": "Participante não encontrado."}`
   - Se o participante já estiver inscrito: `400 Bad Request` → `{"detail": "Participante já está inscrito neste evento."}`
   - Se não houver vagas livres: `400 Bad Request` → `{"detail": "Não existem vagas disponíveis para este evento."}`
2. **Atualização de capacidade**:
   - Impede diminuir a capacidade de um evento para um valor menor do que o número de participantes já inscritos.
3. **Unicidade de e-mail**:
   - Impede o cadastro de dois participantes com o mesmo endereço de e-mail.
4. **Exclusão em cascata**:
   - Ao excluir um evento ou participante, suas respectivas inscrições são automaticamente limpas.

---

## 💡 Exemplos de Requisições e Respostas

### 1. Cadastrar Evento
- **Requisição:** `POST /eventos`
```json
{
  "titulo": "Workshop de FastAPI e Microsserviços",
  "descricao": "Construindo APIs RESTful assíncronas com Python.",
  "data": "2026-10-25",
  "horario": "14:00",
  "local": "Laboratório de Informática 02",
  "capacidade": 30,
  "categoria": "Workshop"
}
```
- **Resposta (`201 Created`):**
```json
{
  "titulo": "Workshop de FastAPI e Microsserviços",
  "descricao": "Construindo APIs RESTful assíncronas com Python.",
  "data": "2026-10-25",
  "horario": "14:00",
  "local": "Laboratório de Informática 02",
  "capacidade": 30,
  "categoria": "Workshop",
  "id": 1,
  "vagas_disponiveis": 30,
  "total_inscritos": 0
}
```

---

### 2. Cadastrar Participante
- **Requisição:** `POST /participantes`
```json
{
  "nome": "Felipe Mendes",
  "email": "felipe.mendes@universidade.edu.br",
  "curso": "Engenharia de Software"
}
```
- **Resposta (`201 Created`):**
```json
{
  "nome": "Felipe Mendes",
  "email": "felipe.mendes@universidade.edu.br",
  "curso": "Engenharia de Software",
  "id": 1
}
```

---

### 3. Inscrever Participante no Evento
- **Requisição:** `POST /eventos/1/inscricoes/1`
- **Resposta (`201 Created`):**
```json
{
  "id": 1,
  "evento_id": 1,
  "participante_id": 1,
  "data_inscricao": "2026-09-28 12:30:00",
  "mensagem": "Inscrição realizada com sucesso!"
}
```

---

### 4. Consultar Inscritos no Evento
- **Requisição:** `GET /eventos/1/inscricoes`
- **Resposta (`200 OK`):**
```json
[
  {
    "id": 1,
    "evento_id": 1,
    "data_inscricao": "2026-09-28 12:30:00",
    "participante": {
      "nome": "Felipe Mendes",
      "email": "felipe.mendes@universidade.edu.br",
      "curso": "Engenharia de Software",
      "id": 1
    }
  }
]
```

---

### 5. Exemplos de Tratamento de Erros

#### Evento Inexistente (`404 Not Found`):
```json
{
  "detail": "Evento não encontrado."
}
```

#### Participante Já Inscrito (`400 Bad Request`):
```json
{
  "detail": "Participante já está inscrito neste evento."
}
```

#### Evento Sem Vagas Disponíveis (`400 Bad Request`):
```json
{
  "detail": "Não existem vagas disponíveis para este evento."
}
```

#### Falha de Validação de Dados (`422 Unprocessable Entity`):
Quando campos obrigatórios estão ausentes, formato de e-mail é inválido ou capacidade <= 0:
```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "capacidade"],
      "msg": "Input should be greater than 0",
      "input": 0
    }
  ]
}
```

---

## 🧪 Testes Automatizados

O projeto inclui uma suíte completa de testes com o **Pytest**, verificando 100% dos requisitos funcionais, integridade de dados e regras de negócio.

Para rodar os testes:
```bash
python -m pytest tests/ -v
```

Resultado esperado:
```text
tests/test_api.py::test_cadastrar_evento_sucesso PASSED                  [  9%]
tests/test_api.py::test_cadastrar_evento_dados_invalidos PASSED          [ 18%]
tests/test_api.py::test_listar_eventos PASSED                            [ 27%]
tests/test_api.py::test_consultar_evento_por_id PASSED                   [ 36%]
tests/test_api.py::test_atualizar_evento PASSED                          [ 45%]
tests/test_api.py::test_excluir_evento PASSED                            [ 54%]
tests/test_api.py::test_cadastrar_participante_sucesso PASSED            [ 63%]
tests/test_api.py::test_cadastrar_participante_erros PASSED              [ 72%]
tests/test_api.py::test_listar_e_consultar_participante PASSED           [ 81%]
tests/test_api.py::test_atualizar_e_excluir_participante PASSED          [ 90%]
tests/test_api.py::test_fluxo_inscricao_e_regras_de_negocio PASSED       [100%]

======================== 11 passed in 0.83s ========================
```

---

## 📦 Publicação no GitHub

Para subir este projeto para o seu repositório pessoal no GitHub, execute os seguintes comandos no terminal:

```bash
# 1. Inicializar o repositório git local (se ainda não tiver sido inicializado)
git init

# 2. Adicionar todos os arquivos
git add .

# 3. Fazer o commit inicial
git commit -m "feat: implementacao completa da API RESTful de Eventos Academicos (APS 02)"

# 4. Configurar branch principal
git branch -M main

# 5. Adicionar a URL do seu repositório remoto no GitHub
# Substitua o link abaixo pelo link do seu repositório criado no GitHub:
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git

# 6. Enviar os arquivos para o GitHub
git push -u origin main
```

---

## 👨‍💻 Autores e Contribuição

Desenvolvido para a **Avaliação Parcial 02 — Desenvolvimento de uma API RESTful**.
- Framework: FastAPI + Pydantic
- Linguagem: Python
- Arquitetura: MVC (Model-View-Controller)
