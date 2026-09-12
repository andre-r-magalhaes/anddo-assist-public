from functools import partial
import logging
from adapters import GeminiAdapter, WabaAdapter
from models import MessageModel, ClientModel, BusinessModel
from data import DatabaseProvider
from models.inventory_model import InventoryModel
from utils.monitor import monitor_telemetry
from utils import RoleTypes

logger = logging.getLogger(f"anddo-app.{__name__}")

class Processor:
    
    def __init__(
        self, 
        db_inventory: DatabaseProvider[InventoryModel],
        db_business: DatabaseProvider[BusinessModel],
        db_clients: DatabaseProvider[ClientModel],
        db_messages: DatabaseProvider[MessageModel],
        business_id: str = "SOTEMUM", # TODO: Identificar o negócio na instância
        ia_adapter=None
    ):
        self.db_inventory = db_inventory
        self.db_business = db_business
        self.db_clients = db_clients
        self.db_messages = db_messages
        self.ia = ia_adapter or GeminiAdapter() # TODO: IAProvider
        self.waba_output = WabaAdapter() # TODO: IMAPIOuputProvider

    @monitor_telemetry
    def execute(self, client: ClientModel, business: BusinessModel) -> str:
        
        # 1. Recupera dados do business ou insere um novo/genérico 
        logger.info(f"Iniciando processamento do cliente {client.client_id} com a business_id: {business.business_id}")
        business_data = self.db_business.get(partition_key="BUSINESS", row_key=business.business_id)
        if not business_data:
            self.db_business.save(business)
        else:
            business = business_data

        # 2. Salva a nova mensagem do cliente
        self.db_messages.save(client.msg_history[0]) # Salva a msg do cliente para garantir que o histórico esteja completo para a IA (evita perda de msg se der erro depois);

        # 3. Carrega dados do cliente se houver 
        client_data = self.db_clients.get(
            partition_key=client.client_id, 
            row_key=client.client_id
        )

        # 4. se o cliente não existe, salva o novo cliente. Se já existe, carrega o histórico de mensagens
        if not client_data:
            self.db_clients.save(client)
        else:
            client = client_data
            msg_history = self.db_messages.get_list(partition_key=business.business_id, row_key=client.client_id)
            client.msg_history.extend(msg_history) 
        
        logger.info(f"Cliente '{client.name}' (ID: {client.client_id}) tem {len(client.msg_history)} mensagens no histórico.")

        # 5. Prepara as ferramentas para a IA (funções parciais com o business_id já preenchido)
        #tool_estoque = partial(self.db_inventory.consultar_item_estoque, business_id=business.business_id)
        def pesquisar_produtos(termo: str):
            """
            Pesquisa produtos no catálogo. Use esta função para encontrar preços, 
            disponibilidade e detalhes técnicos de acabamentos e revestimentos.
            :param termo: O nome do produto, categoria ou material (ex: 'porcelanato polido').
            """
            return self.db_inventory.pesquisar_produtos(business_id=business.business_id, termo=termo)

        logger.debug(f"MESSAGE HISTORY: {[h.text + ' | ' for h in client.msg_history]}")
            
        resposta = self.ia.get_answer(business, client, tools_list=[pesquisar_produtos])
        
        # 6. Salva a resposta da IA como 'model' para o próximo histórico ser real
        nova_msg_ia = MessageModel(
            business_id=business.business_id,
            client_id=client.client_id,
            text=resposta,
            role=RoleTypes.MODEL
        )
        self.db_messages.save(nova_msg_ia)

        logger.info(f"Resposta gerada para o cliente {client.client_id}: {resposta[:25]}...")

        # 7. Envia a resposta da IA para o cliente via WABA
        try:
            response = self.waba_output.send_text_message(
                business_phone_id=business.business_id, # O seu phone_number_id
                to_number=client.client_id,   # O wa_id do cliente
                text=resposta
            )
            logger.info(f"Mensagem enviada para WABA. Status: {response.get('messages', [{}])[0].get('status', 'N/A')}")
            
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem para WABA: {str(e)}")
            return resposta # Mesmo que dê erro no envio, a resposta da IA é válida e pode ser usada para outros fins (ex: análise, fallback, etc)

        logger.debug(f"Resposta do WABA {response.get("messages")}")

        return resposta