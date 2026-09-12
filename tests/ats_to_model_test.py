from data.azure_table_service import AzureTableService
from utils.monitor import app_logger
from data.business_repository import BusinessRepository
from models import ClientModel, BusinessModel, business_model


class ATSToModelTest:
    def __init__(self):
        self.db_service = AzureTableService()
        self.db_handler = BusinessRepository(service=self.db_service)
        #self.get_store(store_id="00000")
        self.hidratate_client_history(store_id="12345", client_id="00000000000")
        
    def hidratate_client_history(self, store_id: str, client_id: str) -> ClientModel:
        return None
        #client_model: ClientModel = self.db_handler.get_client(client_id=client_id, store_id=store_id)
        #app_logger.info(f"[ATS_TO_MODEL_TEST] Client = {client_model.name}, Número = {client_model.contact}")
        
        
        #try:
        #    assert client_model.client_id == "00000"
        #    app_logger.info("✅ [ATS_TO_MODEL_TEST] Assert passed: Client lido pra Model.")
        #except AssertionError:
        #    app_logger.error(f"❌ [ATS_TO_MODEL_TEST] Assert failed.")

    def get_store(self, store_id: str) -> BusinessModel:
        
        business_model: BusinessModel = self.db_handler.get_business_info(store_id)
        app_logger.info(f"[ATS_TO_MODEL_TEST] Nome da loja = { business_model.name }")

        try:
            assert business_model.business_id == "00000"
            app_logger.info(f"✅ [ATS_TO_MODEL_TEST] Assert passed: ID { business_model.business_id } correspondente.")
        except AssertionError:
            app_logger.error(f"❌ [ATS_TO_MODEL_TEST] Assert failed: Esperado 00000000000, recebido {self.business_model.client_id}")


if __name__ == "__main__":
    ut = ATSToModelTest()
