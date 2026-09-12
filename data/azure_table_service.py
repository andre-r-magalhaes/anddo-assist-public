from azure.data.tables import TableServiceClient, TableClient
from utils.monitor import monitor_telemetry
from utils import TableNames

class AzureTableService:
    def __init__(self, connection_string: str = None):
        self.connection_string = connection_string
        self.service_client = TableServiceClient.from_connection_string(self.connection_string)
        self.setup_tables()

    @monitor_telemetry
    def setup_tables(self):
        for table_name in TableNames:
            self.service_client.create_table_if_not_exists(table_name)

    @monitor_telemetry
    def get_table(self, table_name: str) -> TableClient:
        return TableClient.from_connection_string(
            conn_str=self.connection_string, 
            table_name=table_name
        )