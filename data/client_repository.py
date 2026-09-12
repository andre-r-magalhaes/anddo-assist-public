import logging
from typing import Optional
from models import ClientModel
from utils.monitor import monitor_telemetry
from azure.data.tables import TableClient
from azure.core.exceptions import ResourceNotFoundError

logger = logging.getLogger(f"anddo-app.{__name__}")

class ClientRepository: #implements DatabaseProvider
    def __init__(self, table_client: TableClient):
        self.table = table_client

    @monitor_telemetry
    def get(self, partition_key: str, row_key: str) -> Optional[ClientModel]:
        try:
            entity = self.table.get_entity(partition_key=partition_key, row_key=row_key)

            return ClientModel(
                client_id=entity["PartitionKey"],
                contact=entity["RowKey"],
                name=entity.get("name", "Vizinho"),
                msg_history=[]
            )

        except ResourceNotFoundError:
            logger.info(f"Client {row_key} não encontrado no banco.")
            return None

    @monitor_telemetry            
    def save(self, model: ClientModel) -> bool:
        
        entity = {
            "PartitionKey": model.client_id,
            "RowKey": model.client_id,
            "name": model.name,
            "contact": model.contact
        }

        self.table.upsert_entity(mode='merge', entity=entity)