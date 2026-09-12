from enum import Enum

class TableNames(str, Enum):
    """Nomes das tabelas no Azure Table Service para garantir consistência."""
    BUSINESS = "BusinessTable"
    INVENTORY = "InventoryTable"
    CLIENTS = "ClientTable"
    MESSAGES = "MessageHistoryTable"

class RoleTypes(str, Enum):
    """Padrão Gemini para o histórico de mensagens."""
    USER = "user"
    MODEL = "model"