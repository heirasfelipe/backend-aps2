from typing import List, Optional
from fastapi import APIRouter, status, Path, Query
from model.evento import EventoCreate, EventoUpdate, EventoResponse
from model.inscricao import InscricaoResponse, DetalhesInscricaoResponse
from service.evento_service import EventoService
from service.inscricao_service import InscricaoService

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.post(
    "",
    response_model=EventoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo evento acadêmico",
    description="Recebe os dados de um novo evento em formato JSON, valida os campos e retorna o evento criado.",
)
def cadastrar_evento(evento: EventoCreate):
    return EventoService.criar_evento(evento)


@router.get(
    "",
    response_model=List[EventoResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos os eventos",
    description="Retorna a lista completa de eventos acadêmicos cadastrados, com opção de filtro por categoria.",
)
def listar_eventos(
    categoria: Optional[str] = Query(None, description="Filtrar eventos por categoria (ex: Palestra, Workshop)")
):
    return EventoService.listar_eventos(categoria=categoria)


@router.get(
    "/{id}",
    response_model=EventoResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar evento por ID",
    description="Retorna os dados detalhados de um evento específico. Se não existir, retorna 404.",
)
def consultar_evento(
    id: int = Path(..., description="ID único do evento a ser consultado", gt=0)
):
    return EventoService.buscar_por_id(id)


@router.put(
    "/{id}",
    response_model=EventoResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar dados de um evento",
    description="Atualiza um ou mais campos de um evento existente com validação de regras de negócio.",
)
def atualizar_evento(
    id: int = Path(..., description="ID único do evento a ser atualizado", gt=0),
    dados: EventoUpdate = ...,
):
    return EventoService.atualizar_evento(id, dados)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir um evento",
    description="Remove o evento do sistema e remove em cascata todas as inscrições vinculadas a ele.",
)
def excluir_evento(
    id: int = Path(..., description="ID único do evento a ser removido", gt=0)
):
    EventoService.excluir_evento(id)
    return None


# ==========================================
# ROTAS DE INSCRIÇÕES VINCULADAS AO EVENTO
# ==========================================

@router.post(
    "/{evento_id}/inscricoes/{participante_id}",
    response_model=InscricaoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Inscrições"],
    summary="Inscrever participante em um evento",
    description=(
        "Realiza a inscrição do participante no evento especificado após validar: "
        "1) existência do evento; "
        "2) existência do participante; "
        "3) se já está inscrito; "
        "4) se há vagas disponíveis."
    ),
)
def inscrever_participante(
    evento_id: int = Path(..., description="ID do evento acadêmico", gt=0),
    participante_id: int = Path(..., description="ID do participante que deseja se inscrever", gt=0),
):
    return InscricaoService.inscrever_participante(evento_id, participante_id)


@router.get(
    "/{evento_id}/inscricoes",
    response_model=List[DetalhesInscricaoResponse],
    status_code=status.HTTP_200_OK,
    tags=["Inscrições"],
    summary="Consultar participantes inscritos no evento",
    description="Retorna a lista de todos os participantes que estão inscritos no evento informado.",
)
def listar_inscritos(
    evento_id: int = Path(..., description="ID do evento acadêmico", gt=0)
):
    return InscricaoService.listar_inscritos_por_evento(evento_id)


@router.delete(
    "/{evento_id}/inscricoes/{participante_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Inscrições"],
    summary="Cancelar inscrição de um participante",
    description="Cancela a inscrição de um participante no evento liberando a vaga.",
)
def cancelar_inscricao(
    evento_id: int = Path(..., description="ID do evento acadêmico", gt=0),
    participante_id: int = Path(..., description="ID do participante", gt=0),
):
    InscricaoService.cancelar_inscricao(evento_id, participante_id)
    return None
