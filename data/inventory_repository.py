import json
import logging
from typing import List, Optional
from azure.data.tables import TableClient
from models import InventoryModel
from utils.monitor import monitor_telemetry

logger = logging.getLogger(f"anddo-app.{__name__}")

class InventoryRepository: # Sem 'extends', apenas a implementação
    def __init__(self, table_client: TableClient):
        self.table = table_client

    @monitor_telemetry
    def save(self, model: InventoryModel) -> None:
        entity = model.model_dump()
        entity["PartitionKey"] = model.business_id
        entity["RowKey"] = model.item_id
        # ... lógica do JSON string ...
        self.table.upsert_entity(entity)

    @monitor_telemetry
    def get(self, partition_key: str, row_key: str) -> Optional[InventoryModel]:
        try:
            entity = self.table.get_entity(partition_key, row_key)
            return InventoryModel(**entity)
        except:
            return None
        
    @monitor_telemetry
    def consultar_item_estoque(self, business_id: str, item_id: str) -> InventoryModel:
        """
        Busca informações detalhadas de um produto ou serviço no inventário usando o item_id (SKU ou slug).
        Use esta função para verificar preços, descrições técnicas ou disponibilidade.
        """ #
        # Sua lógica de busca no Azure Table Storage #
        entity = self.table.get_entity(partition_key=business_id, row_key=item_id) #
        if entity: #
            # Converte 'data' de string JSON para dict se necessário
            data_val = entity.get('data', '{}')
            if isinstance(data_val, str):
                try:
                    entity['data'] = json.loads(data_val)
                except:
                    entity['data'] = {}
            return InventoryModel(**entity)
        return None
    
    @monitor_telemetry
    def pesquisar_produtos_old(self, business_id: str, termo: str) -> List[InventoryModel]:
        """
        Pesquisa produtos no catálogo da Studio Caio por Nome ou Categoria.
        Otimizado para evitar prolixidade e focar em dados técnicos.
        """
        logger.debug(f"Pesquisando produtos para termo: '{termo}' no negócio: '{business_id}'")
        # Filtra pela PartitionKey (ID do negócio/vendedor)
        query = f"PartitionKey eq '{business_id}'" #
        results = self.table.query_entities(query) #
        
        termo_lower = termo.lower()
        # Divide o termo em palavras e remove conectores curtos (de, para, o, a)
        keywords = [kw for kw in termo_lower.split() if len(kw) > 2]

        matches = []
        for item in results:

            logger.debug(f"Verificando item: {item.get('name', 'N/A')} (ID: {item.get('RowKey', 'N/A')})")

            # Criamos uma string única para busca textual ampla (nome + categoria + dados extras)
            searchable_content = f"{item.get('name', '')} {item.get('category', '')} {item.get('data', '')}".lower()

            # Verifica se todas as palavras-chave relevantes estão presentes no conteúdo do item
            if all(kw in searchable_content for kw in keywords):
                # Garantimos que o campo 'data' seja um dicionário antes de criar o Model
                raw_data = item.get('data', '{}')
                if isinstance(raw_data, str) and raw_data.startswith('{'):
                    try:
                        item['data'] = json.loads(raw_data)
                    except:
                        item['data'] = {}
                
                matches.append(InventoryModel(**item))
        
        return matches

    @monitor_telemetry
    def pesquisar_produtos(self, business_id: str, termo: str) -> list[dict]:
        """
        Pesquisa produtos no catálogo por Categoria, Nome e Data.
        O campo Data é um dicionário com informações adicionais.
        """
        logger.info(f"Pesquisando produtos para termo: '{termo}' no negócio: '{business_id}'")
        # Filtra pela PartitionKey (ID do negócio/vendedor)
        query = f"PartitionKey eq '{business_id}'" #
        results = self.table.query_entities(query) #
        
        #termo_lower = termo.lower()
        # Divide o termo em palavras e remove conectores curtos (de, para, o, a)
        #keywords = [kw for kw in termo_lower.split() if len(kw) > 2]

        matches = []
        for item in results:

            logger.debug(f"Verificando item: {item.get('name', 'N/A')} (ID: {item.get('RowKey', 'N/A')})")

            # Criamos uma string única para busca textual ampla (nome + categoria + dados extras)
            raw_data = f"{item.get('name', '')} {item.get('category', '')} {item.get('data', '')}".lower()
            matches.append(raw_data)
        
        return matches