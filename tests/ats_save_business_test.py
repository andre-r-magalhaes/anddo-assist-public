from utils.monitor import app_logger
from data.business_repository import BusinessRepository
from models import ClientModel, BusinessModel
from data.azure_table_service import AzureTableService

class ATSSaveBusinessTest:
    def __init__(self):
        self.set_store_test()

    def set_store_test(self) -> ClientModel:

        db_service = AzureTableService()
        db_service.setup_tables()
        
        db_handler = BusinessRepository(service=db_service)
        business = BusinessModel(
            business_id="00000",
            name="Loja Exemplo",
            number="00000000000",
            context={
                "menu": ["Produto A", "Produto B", "Produto C"],
                "delivery_fee": 5.0,
                "rules": "Regras de atendimento padrão."
            }
        )

        try:
            success = db_handler.save_business_info(business)
            assert success == True
            app_logger.info("✅ [ATS_SAVE_BUSINESS_TEST] Assert passed: Loja cadastrada.")
        except AssertionError:
            app_logger.error(f"❌ [ATS_SAVE_BUSINESS_TEST] Assert failed.")

if __name__ == "__main__":
    ut = ATSSaveBusinessTest()
