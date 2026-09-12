import config
from data import *
from utils.enums import TableNames
from core.processor import Processor

# Singletons de infraestrutura e orquestração
_ats_service = None
_global_processor_instance = None

def get_ats_service() -> AzureTableService:
    global _ats_service
    if _ats_service is None:
        # Fail-fast: se a conexão estiver errada, quebra aqui na inicialização
        _ats_service = AzureTableService(config.AZURE_TABLE_CONN_STRING)
    return _ats_service

def get_processor() -> Processor:
    global _global_processor_instance
    if _global_processor_instance is None:
        
        ats = get_ats_service()  # Garantimos que a conexão com o Azure Table Service está pronta

        inventory_repo = InventoryRepository(ats.get_table(TableNames.INVENTORY))
        client_repo = ClientRepository(ats.get_table(TableNames.CLIENTS))
        business_repo = BusinessRepository(ats.get_table(TableNames.BUSINESS))
        message_repo = MessageRepository(ats.get_table(TableNames.MESSAGES))
        
        # O Processor agora recebe as fatias prontas
        _global_processor_instance = Processor(
            db_inventory=inventory_repo,
            db_clients=client_repo,
            db_business=business_repo,
            db_messages=message_repo
        )
    
    return _global_processor_instance