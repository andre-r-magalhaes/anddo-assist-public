from pydantic import BaseModel, Field
from datetime import datetime, timezone
import time
import uuid

def generate_invert_timestamp():
    inverse_time = int(9999999999 - time.time())
    return f"{inverse_time}_{uuid.uuid4().hex[:4]}"

class MessageModel(BaseModel):
    message_id: str = Field(default_factory=generate_invert_timestamp)
    business_id: str    # <--- Importante para auditoria e filtros
    client_id: str   # <--- Relaciona a mensagem ao dono del
    text: str
    platform: str = "whatsapp"
    role: str  # "user" ou "model" (o Gemini usa 'model' em vez de 'assistant')
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))