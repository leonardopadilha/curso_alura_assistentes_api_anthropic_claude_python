import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(
  api_key=ANTHROPIC_API_KEY
)

modelo = "claude-3-5-sonnet-20240620"
# modelo = "claude-3-5-haiku-20240307"

prompt_do_sistema = "Classifique o alimento abaixo em uma das categorias: Bebida, Comida Salgada e Comida Doce. Dê uma descrição da categoria."

prompt_do_usuario = input("Digite um alimento: ")

message = client.messages.create(
  model=modelo,
  max_tokens=1000,
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

resposta = message.content[0].text
print(resposta)