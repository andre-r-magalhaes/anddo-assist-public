import logging
import requests
import config
from utils.monitor import monitor_telemetry

logger = logging.getLogger(f"anddo-app.{__name__}")

class WabaAdapter:
    def __init__(self):
        self.token = config.WABA_ACCESS_TOKEN
        self.api_version = config.WABA_VERSION or "v25.0"

    @monitor_telemetry
    def send_text_message(self, business_phone_id: str, to_number: str, text: str):
        try:
            url = f"https://graph.facebook.com/{self.api_version}/{business_phone_id}/messages"
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "text",
                "text": {
                    "body": text
                }
            }

            response = requests.post(url, json=payload, headers=headers)
            response_data = response.json()
            
            logger.debug(f"Resposta do WABA: {response_data}")
            
            if response.status_code != 200:
                logger.error(f"Erro ao enviar para WABA: {response.status_code} - {response.text}")
                response.raise_for_status()
                
        except Exception as e:
            logger.error(f"Falha na comunicação com a API da Meta: {str(e)}")

        return response.json()
