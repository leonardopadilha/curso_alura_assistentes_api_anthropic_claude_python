import os
import anthropic
from helpers import *
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(
  api_key=ANTHROPIC_API_KEY
)

modelo = "claude-3-5-sonnet-20240620"

def identificador_de_perfil():
  prompt_do_sistema = """
  Identifique o perfil de consumo de comida para cada cliente a seguir.

  # Formato da Saída
  Cliente - perfil do cliente em 3 palavras
  """

  prompt_do_usuario = carrega('./dados/lista_de_consumo_100_clientes.csv')

  mensagem = client.messages.create(
    model=modelo,
    max_tokens=2000,
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

  resposta = mensagem
  return resposta


resposta_assistente = identificador_de_perfil()
resposta_texto = resposta_assistente.content[0].text
resposta_tokens = resposta_assistente.usage
print(resposta_texto)
print(f"Tokens de entrada {resposta_tokens.input_tokens}")
print(f"Tokens de saida {resposta_tokens.output_tokens}")
