from typing import Any, Dict
from pydantic import BaseModel

class BusinessModel(BaseModel):
    business_id: str  # PartitionKey no ATS (Tabela 'Businesses')
    name: str = "Carregando..."     # Nome do estabelecimento
    number: str = "0000-0000"
    #description: str = "Descrição do negócio não disponível."
    #address: str = "Endereço não disponível."
    #behavior_guidelines: str = "Seja um atendente prestativo e técnico."
    platform: str = "whatsapp"