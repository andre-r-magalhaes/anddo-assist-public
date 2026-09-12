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

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Erro ao enviar para WABA: HTTP {response.status_code}")
                response.raise_for_status()

            response_data = response.json()
            logger.debug(f"Mensagem entregue ao WABA com sucesso. Status HTTP: {response.status_code}")
            return response_data
                
        except requests.exceptions.Timeout:
            logger.error("Timeout na comunicação com a API da Meta/WABA.")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Falha na comunicação com a API da Meta: HTTP/Request error ({type(e).__name__})")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado no envio de mensagem WABA: ({type(e).__name__})")
            return None
