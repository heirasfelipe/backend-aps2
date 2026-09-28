from pydantic import BaseModel, Field
from .participante import ParticipanteResponse


class InscricaoResponse(BaseModel):
    """Modelo de retorno para confirmação de inscrição."""
    id: int = Field(..., description="Identificador único da inscrição")
    evento_id: int = Field(..., description="ID do evento")
    participante_id: int = Field(..., description="ID do participante")
    data_inscricao: str = Field(..., description="Data e horário da realização da inscrição")
    mensagem: str = Field(default="Inscrição realizada com sucesso!", description="Mensagem de status")


class DetalhesInscricaoResponse(BaseModel):
    """Modelo de retorno detalhado de uma inscrição contendo os dados do participante."""
    id: int = Field(..., description="Identificador único da inscrição")
    evento_id: int = Field(..., description="ID do evento")
    data_inscricao: str = Field(..., description="Data e horário da inscrição")
    participante: ParticipanteResponse = Field(..., description="Dados completos do participante inscrito")
