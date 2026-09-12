import json
import logging
from typing import Optional
from models import BusinessModel
from utils.monitor import monitor_telemetry
from azure.data.tables import  TableClient
from azure.core.exceptions import ResourceNotFoundError

logger = logging.getLogger(f"anddo-app.{__name__}")

class BusinessRepository: #implements DatabaseProvider de forma 'virtual' (ABC)
    def __init__(self, table_client: TableClient):
        self.table = table_client

    @monitor_telemetry
    def get(self, partition_key: str, row_key: str) -> Optional[BusinessModel]:

        try:
            # Tenta buscar a entidade
            entity = self.table.get_entity(partition_key=partition_key or "BUSINESS", row_key=row_key)
            
            #raw_context = entity.get("Context", "{}")
                        
            return BusinessModel(
                business_id=entity["RowKey"],
                name=entity.get("name", "Nome não definido"),
                number=entity.get("number", "desconhecido")
            )
        except ResourceNotFoundError:
            # Se não existir, retorna None em vez de estourar erro
            return None

    @monitor_telemetry   
    def save(self, model: BusinessModel) -> bool:
        entity = {
            "PartitionKey": "BUSINESS",
            "RowKey": model.business_id,
            "name": model.name,
            "number": model.number,
            "platform": "whatsapp"
        }
        
        self.table.upsert_entity(mode='merge', entity=entity)
        return True