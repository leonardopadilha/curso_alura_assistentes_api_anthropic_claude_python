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

def analisador_sentimentos(restaurante):
  prompt_do_sistema = """
  Você é um analisador de sentimentos de avaliações de restaurantes.
  Escreva um parágrafo com até 50 palavras resumindo as avaliações e depois atribua qual o sentimento geral para
  o produto.
  Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

  # Formato de Saída:

  Nome do Restaurante: {restaurante}
  Resumo das avaliações:
  Sentimento Geral: [utilize aqui apenas Positivo, Negativo ou Neutro]
  Pontos fortes: Lista com três bullets
  Pontos fracos: Lista com três bullets
  """

  prompt_do_usuario = carrega(f'./dados/avaliacoes/avaliacoes-restaurante-{restaurante}.txt')

  print(f'Iniciou a análise do {restaurante}')

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
  print(f'Finalizou a análise do {restaurante}')
  salva(f'./dados/analise/analise-{restaurante}.txt', resposta)


analisador_sentimentos('bolos-doces')
