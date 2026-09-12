from azure.storage.queue import QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy
from azure.core.exceptions import ResourceExistsError
from utils.monitor import monitor_telemetry

class AzureQueueSvcAdapter:
    def __init__(self, queue_name: str, connection_string: str):
        self.client = QueueClient.from_connection_string(
            conn_str=connection_string,
            queue_name=queue_name,
            message_encode_policy=BinaryBase64EncodePolicy(),
            message_decode_policy=BinaryBase64DecodePolicy()
        )

    @monitor_telemetry
    def enqueue(self, message_body: str):
        try:
            self.client.create_queue()
        except ResourceExistsError:
            pass

        self.client.send_message(message_body.encode('utf-8'))
