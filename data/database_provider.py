from typing import List, Protocol, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class DatabaseProvider(Protocol, Generic[T]):
    """Define o contrato para qualquer provedor de persistência."""
    
    def get(self, partition_key: str, row_key: str) -> T:
        """Carrega dados."""
        ...

    def get_list(self, partition_key: str, row_key: str) -> List[T]:
        """Carrega uma lista de dados."""
        ...

    def save(self, model: T) -> bool:
        """Salva dados."""
        ...

    