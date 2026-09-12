
import json
import logging
import config
import azure.functions as func
from utils.monitor import monitor_telemetry
from utils import global_factory
from adapters import WabaDTO, AzureQueueSvcAdapter
from models import ClientModel, BusinessModel

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
logger = logging.getLogger(f"anddo-app.{__name__}")

@app.route(route="waba_webhook", methods=["GET", "POST"])
@monitor_telemetry
def waba_webhook(req: func.HttpRequest) -> func.HttpResponse:
    
    if req.method == "GET":
        verify_token = config.WABA_VERIFY_TOKEN
        mode = req.params.get("hub.mode")
        token = req.params.get("hub.verify_token")
        challenge = req.params.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return func.HttpResponse(challenge, status_code=200)
        return func.HttpResponse("Token Inválido", status_code=403)
    elif req.method == "POST":
          
        try:
            raw_data = req.get_json()
        except ValueError:
            return func.HttpResponse("Invalid JSON", status_code=400)
        
        waba_dto = WabaDTO(**raw_data)
        model:ClientModel = waba_dto.to_model()
        
        if model is not None:
            queue_service = AzureQueueSvcAdapter(queue_name=config.WABA_QUEUE_NAME, connection_string=config.AZURE_QUEUE_CONN_STRING)
            queue_service.enqueue(model.model_dump_json())
        
        return func.HttpResponse("OK", status_code=200)

@app.queue_trigger(
    arg_name="azqueue", 
    queue_name=config.WABA_QUEUE_NAME,
    connection="AZURE_QUEUE_CONN_STRING",
    is_disabled="%DISABLE_BROKER%"
)
@monitor_telemetry
def queue_broker(azqueue: func.QueueMessage):

    try:
        processor = global_factory.get_processor()
        raw_data = azqueue.get_body().decode('utf-8')
        payload = json.loads(raw_data)
        
        client = ClientModel(**payload)
        business = BusinessModel(business_id=client.msg_history[0].business_id)
       
        resposta = processor.execute(client, business) 
        
    except Exception as e:
        logger.error(f"Erro fatal no Broker: {str(e)}")
        # Um 'raise' aqui a mensagem volta para a fila (retry)
        # Se não a Azure entende que você "resolveu" o problema e apaga a msg.
        raise e 