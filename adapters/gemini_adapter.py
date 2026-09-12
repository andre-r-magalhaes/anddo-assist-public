import logging
import config
import google.genai as genai
from google.genai import types
from models import BusinessModel, ClientModel
from utils.monitor import monitor_telemetry

logger = logging.getLogger(f"anddo-app.{__name__}")

class GeminiAdapter:
    def __init__(self):
        self.api_key = config.GOOGLE_API_KEY
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = 'gemini-2.5-flash'

    @monitor_telemetry
    def get_answer(self, business: BusinessModel, client: ClientModel, tools_list: list) -> str:
        
        if config.DEBUG and not config.DEBUG_IA: 
            return f"DEBUG MODE: Resposta simulada. Prompt: {client.last_message[:50]}..."
        
        try:

            # 1. Configura a Identidade (System Instruction)
            sys_inst = f"""Você é o assistente virtual da {business.name}, falando com {client.name}.
            OBJETIVO: Venda consultiva de acabamentos. Seja conciso e amigável.
            CATÁLOGO: Você NÃO conhece os produtos de cor. Para qualquer dúvida sobre estoque, preços ou modelos, use a função 'pesquisar_produtos'.
            REGRAS DE RESPOSTA:
            1. Execute as funções imediatamente quando necessário, sem avisar ao usuário.
            2. Responda apenas com o resultado final após obter os dados da ferramenta.
            3. Máximo de 2 parágrafos. Se o cliente estiver indeciso, faça uma pergunta de filtro (ex: 'Ambiente interno ou externo?')."""
            
            logger.info(f"System Instruction configurada para {business.name} e cliente {client.name}")

            # 2. Prepara o Histórico para o Formato do Gemini
            # Transformamos seu MessageModel no formato do SDK
            history = [
                types.Content(role=msg.role, parts=[types.Part(text=msg.text)])
                for msg in client.msg_history
            ]
            
            config_gen = types.GenerateContentConfig(
                tools=tools_list,
                system_instruction=sys_inst
            )

            # 3. Inicia o chat com o histórico carregado (as 5 msgs que você buscou)
            chat = self.client.chats.create(model=self.model_id, config=config_gen, history=history)

            response = chat.send_message(client.last_message)

            # Processamento de Function Calling (suporta chamadas múltiplas/paralelas)
            while response.candidates and response.candidates[0].content.parts and any(p.function_call for p in response.candidates[0].content.parts):
                function_responses = []
                
                for part in response.candidates[0].content.parts:

                    if part.function_call:
                        call = part.function_call
                        # Busca a função correspondente na lista de tools
                        tool_func = next((t for t in tools_list if t.__name__ == call.name), None)
                        
                        if tool_func:
                            resultado = tool_func(**call.args)
                            logger.info(f"Tool '{call.name}' executada. Args: {call.args}")
                            
                            # Garante que o resultado seja serializável (converte Pydantic para dict)
                            if isinstance(resultado, list):
                                resultado = [r.model_dump() if hasattr(r, 'model_dump') else r for r in resultado]
                            elif hasattr(resultado, 'model_dump'):
                                resultado = resultado.model_dump()

                            function_responses.append(
                                types.Part.from_function_response(
                                    name=call.name,
                                    response={'result': resultado}
                                )
                            )
                
                if function_responses:
                    response = chat.send_message(function_responses)
                else:
                    break
            
            for part in response.candidates[0].content.parts:
                if part.text:
                    return part.text
    
        except Exception as e:
            logger.error(f"Erro em {e}", exc_info=True)
            return f"Desculpe. Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."