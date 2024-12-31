from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional
from datetime import datetime

class Event(BaseModel):
    event: str
    properties: Dict[str, Optional[str | int | bool | dict]] = Field(...)
    timestamp: str

    @field_validator("timestamp")
    def validate_timestamp(cls, value):
        """
        Valida que el timestamp sea una fecha ISO 8601 válida.
        """
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return value
        except ValueError:
            raise ValueError("Invalid ISO 8601 timestamp format.")
