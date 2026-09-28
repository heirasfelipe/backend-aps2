from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class ParticipanteBase(BaseModel):
    """Modelo base para dados de Participante."""
    nome: str = Field(..., description="Nome completo do participante", min_length=1, max_length=150)
    email: EmailStr = Field(..., description="E-mail válido do participante", examples=["aluno@universidade.edu.br"])
    curso: str = Field(..., description="Curso do participante", min_length=1, max_length=100)

    @field_validator("nome", "curso")
    @classmethod
    def validar_campos_nao_vazios(cls, valor: str, info) -> str:
        if not valor or not valor.strip():
            raise ValueError(f"O campo '{info.field_name}' não pode ser vazio ou conter apenas espaços.")
        return valor.strip()


class ParticipanteCreate(ParticipanteBase):
    """Modelo para cadastro de um participante."""
    pass


class ParticipanteUpdate(BaseModel):
    """Modelo para atualização parcial ou total de um participante."""
    nome: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = Field(None, examples=["novo_email@universidade.edu.br"])
    curso: Optional[str] = Field(None, min_length=1, max_length=100)

    @field_validator("nome", "curso")
    @classmethod
    def validar_campos_opcionais(cls, valor: Optional[str], info) -> Optional[str]:
        if valor is not None:
            if not valor.strip():
                raise ValueError(f"O campo '{info.field_name}' não pode ser vazio ou conter apenas espaços.")
            return valor.strip()
        return valor


class ParticipanteResponse(ParticipanteBase):
    """Modelo de retorno com dados do participante."""
    id: int = Field(..., description="Identificador único do participante")
