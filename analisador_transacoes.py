import os
import json
import anthropic
from helpers import *
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(
  api_key=ANTHROPIC_API_KEY
)

modelo = "claude-3-5-sonnet-20240620"

def analisar_transacoes(transacoes):
  prompt_do_sistema = """
  Analise as transações financeiras a seguir e identifique se cada uma delas é uma "Possível Fraude" ou se deve ser
  "Aprovada".
  Adicione um atributo "Status" com um dos valores: "Possível Fraude" ou "Aprovado".

  Cada nova transação deve ser inserida dentro da lista do JSON.

  # Possíveis indicações de fraude
  - Transações com valores muito discrepantes
  - Transações que ocorrem em locais muito distantes um do outro

  Adote o formato de resposta abaixo para compor uma resposta.

  # Formato Saída
  {
    "transacoes": [
      {
        "id": "id",
        "tipo": "crédito ou débito",
        "estabelecimento": "nome do estabelecimento",
        "horário": "horário da transação",
        "valor": "R$XX,XX",
        "nome_produto": "nome do produto",
        "localização": "cidade - estado (País)",
        "status": ""
      }
    ]
  }
  """

  prompt_do_usuario = f"""
  Considere o CSV abaixo, onde cada linha é uma transação diferente: {transacoes}.
  Sua resposta deve adotar o #Formato de Resposta (apenas um json sem outros comentários)
  """

  try:
    print("1 - Iniciou a análise de fraude")
    mensagem = client.messages.create(
      model=modelo,
      max_tokens=4000,
      temperature=0,
      system=prompt_do_sistema,
      messages = [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt_do_usuario
            }
          ]
        }
      ]
    )
    resposta = mensagem.content[0].text
    json_resposta = json.loads(resposta)
    salva('./dados/transacoes/transacoes.json', json_resposta)
    print("2 - Finalizou a análise de fraude")
    return json_resposta
  except anthropic.APIConnectionError as e:
    print("O servidor não pode ser acessado! Erro: ", e.__cause__)
  except anthropic.RateLimitError as e:
    print("Um status code 429 foi recebido! Limite de acesso foi atingido.")
  except anthropic.APIStatusError as e:
    print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
  except Exception as e:
    print(f"Um erro inesperado ocorreu: {e}")


def gerar_parecer(transacao):
  prompt_do_sistema = f"""
  Para a seguinte transação, forneça um parecer, apenas se o status for de "Possível Fraude". Indique no parecer
  uma justificativa para que você identifique uma fraude.
  Transação: {transacao}

  ## Formato de Resposta
  "id": "id",
  "tipo": "crédito ou débito",
  "estabelecimento": "nome do estabelecimento",
  "horario": "horário da transação",
  "valor": "R$XX,XX",
  "nome_produto": "nome do produto",
  "localizacao": "cidade - estado (País)",
  "status": "",
  "parecer": "Colocar Não Aplicável se o status for Aprovado"
  """

  try:
    print("3 - Iniciou a geração de parecer")
    mensagem = client.messages.create(
      model=modelo,
      max_tokens=4000,
      temperature=0,
      #system=prompt_do_sistema,
      messages = [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt_do_sistema
            }
          ]
        }
      ]
    )
    resposta = mensagem.content[0].text
    print("4 - Finalizou a geração de parecer")
    return resposta

  except anthropic.APIConnectionError as e:
    print("O servidor não pode ser acessado! Erro: ", e.__cause__)
  except anthropic.RateLimitError as e:
    print("Um status code 429 foi recebido! Limite de acesso foi atingido.")
  except anthropic.APIStatusError as e:
    print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
  except Exception as e:
    print(f"Um erro inesperado ocorreu: {e}")


def gerar_recomendacao(parecer):
  prompt_do_sistema = f"""
  Para a seguinte transação, forneça uma recomendação apropriada baseada no status e nos detalhes 
  da Transação: {parecer}

  As recomendações podem ser "Notificar Cliente", "Acionar setor Anti-fraude" ou "Realizar Verificação Manual".
  Elas devem ser escritas no formato técnico.

  Inclua também uma classificação do tipo de fraude, se aplicável. 
  """

  try:
    print("5 - Iniciou a geração de recomendação")
    mensagem = client.messages.create(
      model=modelo,
      max_tokens=4000,
      temperature=0,
      #system=prompt_do_sistema,
      messages = [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": prompt_do_sistema
            }
          ]
        }
      ]
    )
    resposta = mensagem.content[0].text
    print("6 - Finalizou a geração de recomendação")
    return resposta

  except anthropic.APIConnectionError as e:
    print("O servidor não pode ser acessado! Erro: ", e.__cause__)
  except anthropic.RateLimitError as e:
    print("Um status code 429 foi recebido! Limite de acesso foi atingido.")
  except anthropic.APIStatusError as e:
    print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
  except Exception as e:
    print(f"Um erro inesperado ocorreu: {e}")


transacoes = carrega('transacoes.csv')
transacoes_analisadas = analisar_transacoes(transacoes)

for transacao in transacoes_analisadas['transacoes']:
  if transacao['status'] == 'Possível Fraude':
    parecer = gerar_parecer(transacao)
    recomendacao = gerar_recomendacao(parecer)

    caminho = f"./dados/recomendacoes/transacao-{transacao['id']}-{transacao['nome_produto']}-{transacao['status']}.txt"
    salva(caminho, recomendacao)