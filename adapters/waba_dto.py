from pydantic import BaseModel, Field
from typing import List, Optional
from adapters.providers import IClientProvider, IMessageProvider
from models import MessageModel, ClientModel
from utils import RoleTypes
import logging

logger = logging.getLogger(f"anddo-app.{__name__}")


class Text(BaseModel):
    body: str

class WabaBase(BaseModel):
    class Config:
        extra = 'ignore'

class Message(BaseModel):
    from_id: str = Field(alias="from")
    id: str
    text: Text

class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    wa_id: str
    profile: Optional[Profile] = None

class Metadata(BaseModel):
    phone_number_id: str
    display_phone_number: Optional[str] = None

class WabaValue(BaseModel):
    messages: Optional[List[Message]] = None
    contacts: Optional[List[Contact]] = None
    metadata: Optional[Metadata] = None
    statuses: Optional[List[dict]] = None

class WabaChange(BaseModel):
    value: WabaValue

class WabaEntry(BaseModel):
    changes: List[WabaChange]

class WabaDTO(BaseModel, IClientProvider):
    entry: List[WabaEntry]

    def to_model(self) -> ClientModel:
        try:
            entry = self.entry[0]
            change = entry.changes[0]
            value = change.value

            if value.statuses:
                logger.debug(f"Status recebido: {value.statuses}")
                return None
            
            if not value.messages or not value.contacts:
                return None

            contact = value.contacts[0]
            msg = value.messages[0]
            user_name = contact.profile.name if contact.profile else "Vizinho"

            logger.debug(f"WabaDTO: {value.model_dump_json()}")

            current_message = MessageModel(
                business_id=value.metadata.phone_number_id,
                client_id=contact.wa_id, # ou o campo que você usa para ID
                text=msg.text.body if hasattr(msg.text, 'body') else "", # Garanta que pega o corpo da msg
                role=RoleTypes.USER,
            )

            return ClientModel(
                client_id=contact.wa_id,
                contact=contact.wa_id,
                name=user_name,
                msg_history=[current_message]
            )
        except (IndexError, AttributeError, TypeError) as e:
            logger.error(f"Erro ao converter WabaDTO: {e}", exc_info=True)
            return None