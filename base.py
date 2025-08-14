import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(
  api_key=ANTHROPIC_API_KEY
)

modelo = "claude-3-5-sonnet-20240620"

prompt_do_sistema = """
"""

prompt_do_usuario = """
"""

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

resposta = mensagem.content[0].text