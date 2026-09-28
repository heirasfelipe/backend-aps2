"""
Aplicação Principal - Sistema de Gerenciamento de Eventos Acadêmicos
Avaliação Parcial 02 — Desenvolvimento de uma API RESTful
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller import evento_router, participante_router

tags_metadata = [
    {
        "name": "Eventos",
        "description": "Operações para gerenciamento de eventos acadêmicos (palestras, workshops, minicursos, etc.).",
    },
    {
        "name": "Participantes",
        "description": "Operações para cadastro e gerenciamento de participantes e estudantes.",
    },
    {
        "name": "Inscrições",
        "description": "Controle de inscrições de participantes em eventos com regras de vagas e duplicidade.",
    },
]

app = FastAPI(
    title="API de Gerenciamento de Eventos Acadêmicos",
    description=(
        "API RESTful desenvolvida com FastAPI e Python para gerenciamento de eventos acadêmicos, "
        "participantes e controle de inscrições seguindo a arquitetura MVC.\n\n"
        "### Recursos principais:\n"
        "- **Eventos**: CRUD completo, controle de capacidade e vagas restantes.\n"
        "- **Participantes**: CRUD completo, validação de e-mail e unicidade.\n"
        "- **Inscrições**: Validação de vagas, verificação de duplicidade e cancelamento.\n"
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração de CORS para permitir consumo por clientes Front-End
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro dos controladores (Arquitetura MVC)
app.include_router(evento_router)
app.include_router(participante_router)


@app.get("/", tags=["Início"], summary="Página inicial da API")
def raiz():
    """Endpoint raiz com mensagem de boas-vindas e links para documentação."""
    return {
        "mensagem": "Bem-vindo à API de Gerenciamento de Eventos Acadêmicos!",
        "documentacao_swagger": "/docs",
        "documentacao_redoc": "/redoc",
        "status": "online",
        "versao": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
