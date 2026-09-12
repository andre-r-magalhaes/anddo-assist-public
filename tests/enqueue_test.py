from pathlib import Path
import json
import os
import requests
from dotenv import load_dotenv
from utils.monitor import app_logger


class EnqueueTest:
    def __init__(self):
        self.script_dir = Path(__file__).parent.resolve()
        load_dotenv(self.script_dir.parent / ".env")
        self.function_url = os.getenv("WABA_WEBHOOK_URL")
        self.payload_path = self.script_dir / "waba_payload.json"
        self.send_local_payload()


    def send_local_payload(self):
        if not os.path.exists(self.payload_path):
            app_logger.error(f"[INTEGRATION_TEST] Arquivo {self.payload_path} não encontrado.")
            return
        
        with open(self.payload_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        app_logger.info(f"🚀 [INTEGRATION_TEST] Enviando payload de {self.payload_path} para a Function {self.function_url}")
        
        try:
            response = requests.post(self.function_url, json=data)
            app_logger.info(f"[INTEGRATION_TEST] Status: {response.status_code}, Resposta: {response.text}")

        except Exception as e:
            app_logger.error(f"[INTEGRATION_TEST] Falha na conexão: {e}")

if __name__ == "__main__":
    starter = EnqueueTest()
