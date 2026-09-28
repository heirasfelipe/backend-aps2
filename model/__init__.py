from .evento import EventoBase, EventoCreate, EventoUpdate, EventoResponse
from .participante import ParticipanteBase, ParticipanteCreate, ParticipanteUpdate, ParticipanteResponse
from .inscricao import InscricaoResponse, DetalhesInscricaoResponse

__all__ = [
    "EventoBase",
    "EventoCreate",
    "EventoUpdate",
    "EventoResponse",
    "ParticipanteBase",
    "ParticipanteCreate",
    "ParticipanteUpdate",
    "ParticipanteResponse",
    "InscricaoResponse",
    "DetalhesInscricaoResponse",
]
