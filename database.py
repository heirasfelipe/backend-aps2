"""
Módulo de armazenamento de dados em memória.
Simula o banco de dados da aplicação para Eventos, Participantes e Inscrições.
"""
from typing import Dict, List, Any


class InMemoryDatabase:
    """Gerenciador central do estado dos dados em memória."""

    def __init__(self):
        self.eventos: List[Dict[str, Any]] = []
        self.participantes: List[Dict[str, Any]] = []
        self.inscricoes: List[Dict[str, Any]] = []
        self._proximo_id_evento = 1
        self._proximo_id_participante = 1
        self._proximo_id_inscricao = 1

    def gerar_id_evento(self) -> int:
        novo_id = self._proximo_id_evento
        self._proximo_id_evento += 1
        return novo_id

    def gerar_id_participante(self) -> int:
        novo_id = self._proximo_id_participante
        self._proximo_id_participante += 1
        return novo_id

    def gerar_id_inscricao(self) -> int:
        novo_id = self._proximo_id_inscricao
        self._proximo_id_inscricao += 1
        return novo_id

    def reset(self):
        """Reinicia os dados em memória (útil para testes unitários/integração)."""
        self.eventos.clear()
        self.participantes.clear()
        self.inscricoes.clear()
        self._proximo_id_evento = 1
        self._proximo_id_participante = 1
        self._proximo_id_inscricao = 1


# Instância global compartilhada (Singleton em memória)
db = InMemoryDatabase()
