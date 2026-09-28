from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from database import db
from model.participante import ParticipanteCreate, ParticipanteUpdate


class ParticipanteService:
    """Camada de serviço responsável pelas regras de negócio relacionadas a Participantes."""

    @classmethod
    def criar_participante(cls, dados: ParticipanteCreate) -> Dict[str, Any]:
        """Cadastra um novo participante garantindo unicidade de e-mail."""
        email_normalizado = str(dados.email).lower().strip()
        for p in db.participantes:
            if p["email"].lower() == email_normalizado:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Já existe um participante cadastrado com este e-mail."
                )

        novo_participante = {
            "id": db.gerar_id_participante(),
            "nome": dados.nome,
            "email": email_normalizado,
            "curso": dados.curso,
        }
        db.participantes.append(novo_participante)
        return novo_participante

    @classmethod
    def listar_participantes(cls, curso: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retorna todos os participantes cadastrados, com filtro opcional por curso."""
        participantes = db.participantes
        if curso:
            participantes = [p for p in participantes if p["curso"].lower() == curso.lower()]
        return participantes

    @classmethod
    def buscar_por_id(cls, participante_id: int) -> Dict[str, Any]:
        """Busca um participante pelo ID."""
        for p in db.participantes:
            if p["id"] == participante_id:
                return p

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante não encontrado."
        )

    @classmethod
    def atualizar_participante(cls, participante_id: int, dados: ParticipanteUpdate) -> Dict[str, Any]:
        """Atualiza os dados de um participante."""
        participante = None
        for p in db.participantes:
            if p["id"] == participante_id:
                participante = p
                break

        if not participante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante não encontrado."
            )

        dados_dict = dados.model_dump(exclude_unset=True)

        # Se for atualizar e-mail, verificar duplicidade em outro participante
        if "email" in dados_dict:
            novo_email = str(dados_dict["email"]).lower().strip()
            for p in db.participantes:
                if p["id"] != participante_id and p["email"].lower() == novo_email:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Este e-mail já está sendo utilizado por outro participante."
                    )
            dados_dict["email"] = novo_email

        participante.update(dados_dict)
        return participante

    @classmethod
    def excluir_participante(cls, participante_id: int) -> None:
        """Exclui um participante e suas inscrições associadas."""
        participante_encontrado = None
        for p in db.participantes:
            if p["id"] == participante_id:
                participante_encontrado = p
                break

        if not participante_encontrado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante não encontrado."
            )

        db.participantes.remove(participante_encontrado)

        # Remove inscrições deste participante (integridade referencial)
        db.inscricoes[:] = [i for i in db.inscricoes if i["participante_id"] != participante_id]
