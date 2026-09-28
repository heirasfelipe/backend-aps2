from datetime import datetime
from typing import List, Dict, Any
from fastapi import HTTPException, status
from database import db


class InscricaoService:
    """Camada de serviço responsável pelas regras de negócio de Inscrições em Eventos."""

    @classmethod
    def inscrever_participante(cls, evento_id: int, participante_id: int) -> Dict[str, Any]:
        """
        Realiza a inscrição de um participante em um evento.
        
        Verificações obrigatórias:
        1. Se o evento existe (404 Not Found);
        2. Se o participante existe (404 Not Found);
        3. Se o participante já está inscrito no evento (400 Bad Request);
        4. Se o evento ainda possui vagas disponíveis (400 Bad Request).
        """
        # 1. Verifica se o evento existe
        evento = next((e for e in db.eventos if e["id"] == evento_id), None)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento não encontrado."
            )

        # 2. Verifica se o participante existe
        participante = next((p for p in db.participantes if p["id"] == participante_id), None)
        if not participante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante não encontrado."
            )

        # 3. Verifica se o participante já está inscrito no evento
        ja_inscrito = any(
            i["evento_id"] == evento_id and i["participante_id"] == participante_id
            for i in db.inscricoes
        )
        if ja_inscrito:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Participante já está inscrito neste evento."
            )

        # 4. Verifica se o evento ainda possui vagas disponíveis
        total_inscritos = sum(1 for i in db.inscricoes if i["evento_id"] == evento_id)
        if total_inscritos >= evento["capacidade"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não existem vagas disponíveis para este evento."
            )

        # Realiza a inscrição
        nova_inscricao = {
            "id": db.gerar_id_inscricao(),
            "evento_id": evento_id,
            "participante_id": participante_id,
            "data_inscricao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mensagem": "Inscrição realizada com sucesso!"
        }
        db.inscricoes.append(nova_inscricao)

        return nova_inscricao

    @classmethod
    def listar_inscritos_por_evento(cls, evento_id: int) -> List[Dict[str, Any]]:
        """
        Retorna a lista de participantes inscritos em um determinado evento.
        Verifica se o evento existe antes de consultar.
        """
        evento = next((e for e in db.eventos if e["id"] == evento_id), None)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento não encontrado."
            )

        inscricoes_evento = [i for i in db.inscricoes if i["evento_id"] == evento_id]
        resultado = []

        for inscricao in inscricoes_evento:
            participante = next((p for p in db.participantes if p["id"] == inscricao["participante_id"]), None)
            if participante:
                resultado.append({
                    "id": inscricao["id"],
                    "evento_id": evento_id,
                    "data_inscricao": inscricao["data_inscricao"],
                    "participante": participante
                })

        return resultado

    @classmethod
    def cancelar_inscricao(cls, evento_id: int, participante_id: int) -> None:
        """Permite que um participante cancele sua inscrição em um evento."""
        evento = next((e for e in db.eventos if e["id"] == evento_id), None)
        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento não encontrado."
            )

        participante = next((p for p in db.participantes if p["id"] == participante_id), None)
        if not participante:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante não encontrado."
            )

        inscricao = next(
            (i for i in db.inscricoes if i["evento_id"] == evento_id and i["participante_id"] == participante_id),
            None
        )
        if not inscricao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inscrição não encontrada para este participante neste evento."
            )

        db.inscricoes.remove(inscricao)
