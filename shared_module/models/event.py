from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional, Union
from datetime import datetime
import json

class ElementAttributes(BaseModel):
    class_: Optional[str] = Field(None, alias="class")
    href: Optional[str] = None
    # Agrega otros atributos según sea necesario.

class Properties(BaseModel):
    distinct_id: str
    session_id: str
    journey_id: Optional[str] = None
    current_url: str = Field(..., alias="$current_url")
    host: str = Field(..., alias="$host")
    pathname: str = Field(..., alias="$pathname")
    browser: str = Field(..., alias="$browser")
    device: str = Field(..., alias="$device")
    screen_height: int = Field(..., alias="$screen_height")
    screen_width: int = Field(..., alias="$screen_width")
    eventType: str
    elementType: str
    elementText: str
    elementAttributes: Optional[ElementAttributes] = None
    timestamp: str
    x: int
    y: int
    mouseButton: int
    ctrlKey: bool
    shiftKey: bool
    altKey: bool
    metaKey: bool

    @field_validator("timestamp")
    def validate_timestamp(cls, value):
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return value
        except ValueError:
            raise ValueError("Invalid ISO 8601 timestamp format.")

class Event(BaseModel):
    event: str
    properties: Properties
    timestamp: str

    @field_validator("timestamp")
    def validate_event_timestamp(cls, value):
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return value
        except ValueError:
            raise ValueError("Invalid ISO 8601 timestamp format.")
        
    def to_json(self) -> dict:
        """
        Convierte la instancia de Event a un formato JSON compatible con el alias.
        """
        return self.model_dump(by_alias=True)  
    
          
