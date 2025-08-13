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

def categoriza_alimento(lista_categorias_validas, nome_do_alimento):
  prompt_do_sistema = f"""
  Você é um categorizador de alimentos.
  Você não deve responder outros objetos que não sejam alimentos.
  Você deve assumir as categorias presentes na lista abaixo:

  # Lista de Categorias Válidas
  {lista_categorias_validas.split(",")}

  # Formato da Saída
  Produto: Nome do Produto
  Categoria: Apresente a categoria do produto

  # Exemplo de Saída
  Produto: Maçã
  Categoria: Frutas
  """
  prompt_do_usuario = nome_do_alimento
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
  return resposta


categorias_validas = input("Informe as categorias válidas, separando por vírgula: ")
while True:
  nome_do_alimento = input("Digite o nome do alimento: ")
  texto_resposta = categoriza_alimento(categorias_validas, nome_do_alimento)
  print(texto_resposta)