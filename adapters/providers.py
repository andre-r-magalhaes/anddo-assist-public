from abc import ABC, abstractmethod
from models.client_model import ClientModel
from models.message_model import MessageModel

class IMessageProvider(ABC):
    @abstractmethod
    def to_model(self) -> MessageModel:
        pass

class IClientProvider(ABC):
    @abstractmethod
    def to_model(self) -> ClientModel:
        pass