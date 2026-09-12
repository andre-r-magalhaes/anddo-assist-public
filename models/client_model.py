from pydantic import BaseModel, Field
from typing import List, Optional
from models.message_model import MessageModel

class ClientModel(BaseModel):
    client_id: str  # PartitionKey no ATS
    contact: str    # Número do WhatsApp, RowKey na tabela de Clientes
    name: Optional[str] = "Vizinho" # Valor default amigável
    msg_history: List[MessageModel] = []
    
    @property
    def last_message(self) -> Optional[str]:
        if self.msg_history:
            return self.msg_history[-1].text
        return "Nenhuma mensagem encontrada."