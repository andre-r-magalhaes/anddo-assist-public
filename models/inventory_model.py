from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class InventoryModel(BaseModel):
    business_id: str  # PartitionKey no ATS
    item_id: str      # RowKey no ATS (ex: SKU, código de barras ou slug)
    category: str     # "pizzas", "peças_suspensao", "servicos_estetica"
    name: str        # Nome visível (ex: "Pizza Muçarela", "Filtro de Óleo", "Drenagem")
    #description: str  # Detalhes (ingredientes, especificações técnicas, duração)
    #price: float      # Valor unitário
    #unit: str = "un"  # "un", "kg", "hora", "sessão"
    #available: bool = True
    data: Dict[str, Any] = Field(default_factory=dict) # Para campos específicos (ex: 'tamanho': 'G', 'compatibilidade': 'Vectra')