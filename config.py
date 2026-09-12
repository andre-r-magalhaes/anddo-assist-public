import os

# APIs Externas
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WABA_ACCESS_TOKEN = os.getenv("WABA_ACCESS_TOKEN")
WABA_VERIFY_TOKEN = os.getenv("WABA_VERIFY_TOKEN")
WABA_VERSION = os.getenv("WABA_VERSION")

# Armazenamento e Filas (Azure Storage)
AZURE_QUEUE_CONN_STRING = os.getenv("AZURE_QUEUE_CONN_STRING")
AZURE_TABLE_CONN_STRING = os.getenv("AZURE_TABLE_CONN_STRING")
WABA_QUEUE_NAME = os.getenv("WABA_QUEUE_NAME")

# Flags de Controle
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
DEBUG_IA = os.getenv("DEBUG_IA", "False").lower() == "true"
DISABLE_BROKER = os.getenv("DISABLE_BROKER", "False").lower() == "true"