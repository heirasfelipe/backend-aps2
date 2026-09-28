from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from database import db
from model.evento import EventoCreate, EventoUpdate


class EventoService:
    """Camada de serviço responsável pelas regras de negócio relacionadas a Eventos."""

    @staticmethod
    def _calcular_metricas_evento(evento: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula o total de inscritos e vagas disponíveis para um evento."""
        total_inscritos = sum(1 for i in db.inscricoes if i["evento_id"] == evento["id"])
        vagas_disponiveis = max(0, evento["capacidade"] - total_inscritos)
        
        dados = dict(evento)
        dados["total_inscritos"] = total_inscritos
        dados["vagas_disponiveis"] = vagas_disponiveis
        return dados

    @classmethod
    def criar_evento(cls, dados: EventoCreate) -> Dict[str, Any]:
        """Cadastra um novo evento acadêmico no sistema."""
        novo_evento = {
            "id": db.gerar_id_evento(),
            "titulo": dados.titulo,
            "descricao": dados.descricao,
            "data": dados.data,
            "horario": dados.horario,
            "local": dados.local,
            "capacidade": dados.capacidade,
            "categoria": dados.categoria,
        }
        db.eventos.append(novo_evento)
        return cls._calcular_metricas_evento(novo_evento)

    @classmethod
    def listar_eventos(cls, categoria: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retorna todos os eventos cadastrados, com opção de filtro por categoria."""
        eventos = db.eventos
        if categoria:
            eventos = [e for e in eventos if e["categoria"].lower() == categoria.lower()]
        
        return [cls._calcular_metricas_evento(e) for e in eventos]

    @classmethod
    def buscar_por_id(cls, evento_id: int) -> Dict[str, Any]:
        """Busca um evento pelo seu identificador único."""
        for evento in db.eventos:
            if evento["id"] == evento_id:
                return cls._calcular_metricas_evento(evento)
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado."
        )

    @classmethod
    def atualizar_evento(cls, evento_id: int, dados: EventoUpdate) -> Dict[str, Any]:
        """Atualiza os dados de um evento existente com validações de regra de negócio."""
        evento = None
        for e in db.eventos:
            if e["id"] == evento_id:
                evento = e
                break

        if not evento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento não encontrado."
            )

        dados_dict = dados.model_dump(exclude_unset=True)

        # Regra de negócio: nova capacidade não pode ser inferior aos inscritos já confirmados
        if "capacidade" in dados_dict:
            nova_capacidade = dados_dict["capacidade"]
            total_inscritos = sum(1 for i in db.inscricoes if i["evento_id"] == evento_id)
            if nova_capacidade < total_inscritos:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A nova capacidade ({nova_capacidade}) não pode ser inferior ao número de inscritos atuais ({total_inscritos})."
                )

        evento.update(dados_dict)
        return cls._calcular_metricas_evento(evento)

    @classmethod
    def excluir_evento(cls, evento_id: int) -> None:
        """Exclui um evento e cancela/remove em cascata as inscrições associadas."""
        evento_encontrado = None
        for e in db.eventos:
            if e["id"] == evento_id:
                evento_encontrado = e
                break

        if not evento_encontrado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento não encontrado."
            )

        # Remove o evento
        db.eventos.remove(evento_encontrado)

        # Remove inscrições associadas (integridade referencial)
        db.inscricoes[:] = [i for i in db.inscricoes if i["evento_id"] != evento_id]
