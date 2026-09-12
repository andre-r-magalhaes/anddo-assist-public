import os
from adapters.aqs_adapter import AzureQueueSvcAdapter
from utils.monitor import app_logger

def check():

    qn = os.getenv("WABA_QUEUE_NAME")
    cn = os.getenv("AzureWebJobsStorage") or "UseDevelopmentStorage=true"
    app_logger.info(f"[CHECK_QUEUE_TEST] Verificando fila: {qn} em {cn}")
    
    adapter = AzureQueueSvcAdapter(queue_name=qn, connection_string=cn)
    mensagens = adapter.client.peek_messages(max_messages=5)

    for msg in mensagens:
        app_logger.info(f"[CHECK_QUEUE_TEST] ID: {msg.id}")
        app_logger.info(f"[CHECK_QUEUE_TEST] Conteúdo: {msg.content}\n==============================")

if __name__ == "__main__":
    check()