from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class EventoBase(BaseModel):
    """Modelo base para dados de Eventos Acadêmicos."""
    titulo: str = Field(..., description="Título do evento acadêmico", min_length=1, max_length=150)
    descricao: str = Field(..., description="Descrição detalhada sobre o evento", min_length=1)
    data: str = Field(..., description="Data de realização do evento no formato AAAA-MM-DD", examples=["2026-10-20"])
    horario: str = Field(..., description="Horário de início no formato HH:MM", examples=["14:30"])
    local: str = Field(..., description="Local ou sala onde o evento ocorrerá", min_length=1, max_length=200)
    capacidade: int = Field(..., gt=0, description="Capacidade máxima de participantes (deve ser maior que zero)")
    categoria: str = Field(
        ...,
        description="Categoria do evento (Ex: Palestra, Workshop, Minicurso, Seminário, Competição)",
        min_length=1,
        max_length=80,
    )

    @field_validator("titulo", "descricao", "local", "categoria")
    @classmethod
    def validar_campos_nao_vazios(cls, valor: str, info) -> str:
        if not valor or not valor.strip():
            raise ValueError(f"O campo '{info.field_name}' não pode ser vazio ou conter apenas espaços.")
        return valor.strip()

    @field_validator("data")
    @classmethod
    def validar_formato_data(cls, valor: str) -> str:
        if not valor or not valor.strip():
            raise ValueError("A data do evento é obrigatória.")
        valor = valor.strip()
        try:
            # Valida se é uma data real no calendário e no formato AAAA-MM-DD
            data_parsed = datetime.strptime(valor, "%Y-%m-%d").date()
            return data_parsed.strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("A data do evento deve ser válida e estar no formato AAAA-MM-DD (ex: 2026-10-20).")

    @field_validator("horario")
    @classmethod
    def validar_formato_horario(cls, valor: str) -> str:
        if not valor or not valor.strip():
            raise ValueError("O horário do evento é obrigatório.")
        valor = valor.strip()
        try:
            # Valida se é um horário válido no formato HH:MM
            horario_parsed = datetime.strptime(valor, "%H:%M").time()
            return horario_parsed.strftime("%H:%M")
        except ValueError:
            raise ValueError("O horário do evento deve ser válido e estar no formato HH:MM (ex: 14:30).")

    @field_validator("capacidade")
    @classmethod
    def validar_capacidade(cls, valor: int) -> int:
        if valor <= 0:
            raise ValueError("A capacidade do evento deve ser maior que zero.")
        return valor


class EventoCreate(EventoBase):
    """Modelo para criação de um novo evento."""
    pass


class EventoUpdate(BaseModel):
    """Modelo para atualização parcial ou total de um evento."""
    titulo: Optional[str] = Field(None, min_length=1, max_length=150)
    descricao: Optional[str] = Field(None, min_length=1)
    data: Optional[str] = Field(None, examples=["2026-10-20"])
    horario: Optional[str] = Field(None, examples=["14:30"])
    local: Optional[str] = Field(None, min_length=1, max_length=200)
    capacidade: Optional[int] = Field(None, gt=0)
    categoria: Optional[str] = Field(None, min_length=1, max_length=80)

    @field_validator("titulo", "descricao", "local", "categoria")
    @classmethod
    def validar_campos_opcionais(cls, valor: Optional[str], info) -> Optional[str]:
        if valor is not None:
            if not valor.strip():
                raise ValueError(f"O campo '{info.field_name}' não pode ser vazio ou conter apenas espaços.")
            return valor.strip()
        return valor

    @field_validator("data")
    @classmethod
    def validar_data_opcional(cls, valor: Optional[str]) -> Optional[str]:
        if valor is not None:
            valor = valor.strip()
            try:
                data_parsed = datetime.strptime(valor, "%Y-%m-%d").date()
                return data_parsed.strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError("A data do evento deve ser válida e estar no formato AAAA-MM-DD (ex: 2026-10-20).")
        return valor

    @field_validator("horario")
    @classmethod
    def validar_horario_opcional(cls, valor: Optional[str]) -> Optional[str]:
        if valor is not None:
            valor = valor.strip()
            try:
                horario_parsed = datetime.strptime(valor, "%H:%M").time()
                return horario_parsed.strftime("%H:%M")
            except ValueError:
                raise ValueError("O horário do evento deve ser válido e estar no formato HH:MM (ex: 14:30).")
        return valor

    @field_validator("capacidade")
    @classmethod
    def validar_capacidade_opcional(cls, valor: Optional[int]) -> Optional[int]:
        if valor is not None and valor <= 0:
            raise ValueError("A capacidade do evento deve ser maior que zero.")
        return valor


class EventoResponse(EventoBase):
    """Modelo de resposta contendo os dados do evento cadastrado."""
    id: int = Field(..., description="Identificador único do evento")
    vagas_disponiveis: int = Field(..., description="Quantidade de vagas restantes")
    total_inscritos: int = Field(..., description="Quantidade total de participantes inscritos")
