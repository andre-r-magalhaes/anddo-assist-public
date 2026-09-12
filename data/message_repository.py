from itertools import islice
import logging
from typing import Optional, List
from models import MessageModel
from utils.monitor import monitor_telemetry
from azure.data.tables import  TableClient

logger = logging.getLogger(f"anddo-app.{__name__}")

class MessageRepository: #implements DatabaseProvider de forma 'virtual' (ABC)
    def __init__(self, table_client: TableClient):
        self.table = table_client

    @monitor_telemetry
    def get_list(self, partition_key: str, row_key: str) -> List[MessageModel]:
        query_filter = f"PartitionKey eq '{partition_key}_{row_key}'"
        
        entities = self.table.query_entities(query_filter=query_filter, results_per_page=5)
        messages = list(islice(entities, 5))
        msg_history:List[MessageModel] = []
        
        for msg_ent in messages:
            msg_model = MessageModel(
                message_id=msg_ent['RowKey'],
                business_id=partition_key,
                client_id=row_key,
                text=msg_ent['text'],
                role=msg_ent['role'],
                timestamp=msg_ent['timestamp'] # O SDK do Azure já converte para datetime
            )
            msg_history.append(msg_model)
        
        msg_history.reverse()
        logger.debug(f"MESSAGE HISTORY: {[h.text + '|' for h in msg_history]}")

        return msg_history
    
    @monitor_telemetry
    def get(self, partition_key: str, row_key: str) -> Optional[MessageModel]: #
        try:
            # A PartitionKey para mensagens é uma combinação de business_id e client_id
            entity = self.table.get_entity(partition_key=f"{partition_key}_{row_key}", row_key=row_key)
            return MessageModel(**entity)
        except Exception:
            # Retorna None se a mensagem não for encontrada ou ocorrer um erro
            return None

    @monitor_telemetry   
    def save(self, model: MessageModel) -> bool:

        entity = {
            "PartitionKey": f"{model.business_id}_{model.client_id}",
            "RowKey": model.message_id,  # Ou um timestamp invertido para ordenação
            "text": model.text,
            "platform": model.platform,
            "role": model.role,
            "timestamp": model.timestamp.isoformat() # ATS lida bem com strings ISO
        }

        self.table.upsert_entity(mode="merge", entity=entity)
        
        return True