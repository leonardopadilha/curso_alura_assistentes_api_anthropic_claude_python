import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(
  api_key=ANTHROPIC_API_KEY
)

modelo = "claude-3-5-sonnet-20240620"

def funcao():
  prompt_do_sistema = f"""
  """

  prompt_do_usuario = f"""
  """

  try:
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
  except anthropic.APIConnectionError as e:
    print("O servidor não pode ser acessado! Erro: ", e.__cause__)
  except anthropic.RateLimitError as e:
    print("Um status code 429 foi recebido! Limite de acesso foi atingido.")
  except anthropic.APIStatusError as e:
    print(f"Um erro {e.status_code} foi recebido. Mais informações: {e.response}")
  except Exception as e:
    print(f"Um erro inesperado ocorreu: {e}")