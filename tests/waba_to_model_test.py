import os
import json

from pathlib import Path
from adapters.waba_dto import WabaDTO
from utils.monitor import app_logger

class WabaToModelTest:
    def __init__(self):
        self.script_dir = Path(__file__).parent.resolve()
        self.payload_path = self.script_dir / "waba_payload.json"
        self.waba_to_model()
        
    def waba_to_model(self):

        if not os.path.exists(self.payload_path):
            app_logger.error(f"[WABA_MODEL_UT] Arquivo {self.payload_path} não encontrado.")
            return

        with open(self.payload_path, 'r', encoding='utf-8') as f:
            payload = json.load(f)

        self.waba_dto = WabaDTO(**payload)
        self.client_model = self.waba_dto.to_model()

        app_logger.info(f"[WABA_MODEL_UT] ID {self.client_model.client_id}, CONTACT {self.client_model.contact}, MESSAGE {self.client_model.message}")
        
        try:
            assert self.client_model.client_id == "00000000000"
            app_logger.info("✅ [WABA_MODEL_UT] Assert passed: ID correspondente.")
        except AssertionError:
            app_logger.error(f"❌ [WABA_MODEL_UT] Assert failed: Esperado 00000000000, recebido {self.client_model.client_id}")

if __name__ == "__main__":
    ut = WabaToModelTest()
