import os
import pytest
from google import genai

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    pytest.skip("GOOGLE_API_KEY não configurada no ambiente. Pulando teste de integração com Gemini.", allow_module_level=True)

client = genai.Client(api_key=api_key)

contexto_cardapio = "Hoje temos: 1. Nhoque da Fortuna, 2. Risoto de Alho Poró."
pergunta = "Quais as opções de prato do dia?"

prompt = f"Contexto: {contexto_cardapio}\nPergunta: {pergunta}\nResponda de forma curta."

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    
    print("--- Resposta do Gemini ---")
    print(response.text)

except Exception as e:
    print(f"Erro na geração: {e}")
