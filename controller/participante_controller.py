from typing import List, Optional
from fastapi import APIRouter, status, Path, Query
from model.participante import ParticipanteCreate, ParticipanteUpdate, ParticipanteResponse
from service.participante_service import ParticipanteService

router = APIRouter(prefix="/participantes", tags=["Participantes"])


@router.post(
    "",
    response_model=ParticipanteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar um novo participante",
    description="Recebe os dados do participante (nome, email, curso), valida unicidade de e-mail e salva o cadastro.",
)
def cadastrar_participante(participante: ParticipanteCreate):
    return ParticipanteService.criar_participante(participante)


@router.get(
    "",
    response_model=List[ParticipanteResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos os participantes",
    description="Retorna a lista de todos os participantes cadastrados, com possibilidade de filtro por curso.",
)
def listar_participantes(
    curso: Optional[str] = Query(None, description="Filtrar participantes por curso (ex: Ciência da Computação)")
):
    return ParticipanteService.listar_participantes(curso=curso)


@router.get(
    "/{id}",
    response_model=ParticipanteResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar participante por ID",
    description="Retorna os dados cadastrais de um participante a partir do seu identificador único.",
)
def consultar_participante(
    id: int = Path(..., description="ID único do participante", gt=0)
):
    return ParticipanteService.buscar_por_id(id)


@router.put(
    "/{id}",
    response_model=ParticipanteResponse,
    status_code=status.HTTP_200_OK,
    summary="Atualizar dados do participante",
    description="Permite atualizar os dados do participante com validação de formato e unicidade de e-mail.",
)
def atualizar_participante(
    id: int = Path(..., description="ID único do participante a ser atualizado", gt=0),
    dados: ParticipanteUpdate = ...,
):
    return ParticipanteService.atualizar_participante(id, dados)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir participante",
    description="Remove o participante do sistema e cancela suas inscrições em eventos.",
)
def excluir_participante(
    id: int = Path(..., description="ID único do participante", gt=0)
):
    ParticipanteService.excluir_participante(id)
    return None
