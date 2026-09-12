# Anddo Assistant Public

## Objetivo

Este projeto é um assistente de integração entre a WhatsApp Business API (WABA) e o modelo Gemini da Google. Ele processa mensagens recebidas via webhook, envia para uma fila Azure, processa com o modelo Gemini e responde via WABA.

## Arquitetura

O fluxo principal é:

1. Webhook da Meta (WABA) -> Queue (Azure) -> Processor (Gemini) -> Resposta via WABA

## Tecnologias

- Python
- Azure Functions
- Azure Storage Queue
- Azure Table Storage
- Google Gemini API
- WhatsApp Business API

## Instalação

1. Clone o repositório:

```bash

git clone https://github.com/seu-usuario/anddo-assist-public.git
cd anddo-assist-public
```

2. Instale as dependências:

```bash

pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env` na raiz do projeto com base no `.env.example` e preencha as variáveis de ambiente necessárias.

## Executando Testes

```bash

pytest
```

## Limitações Conhecidas

- A versão do WABA deve ser compatível com a implementação atual.
- A chave da API do Google Gemini deve ser válida e ter cotas suficientes.

## Segurança

- Nunca comite credenciais ou tokens no repositório.
- Configure secrets no ambiente de deploy.
- Valide a assinatura do webhook da Meta antes de usar em produção.
- Evite registrar dados pessoais nos logs.

## Contribuição

Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT.
