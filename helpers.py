def carrega(nome_do_arquivo):
  try:
    with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
      dados = arquivo.read()
      return dados
  except IOError as e:
    print(f"Erro: {e}")

import json

def salva(nome_do_arquivo, conteudo):
  try:
    with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
      # Se o conteúdo for um dicionário, converte para JSON
      if isinstance(conteudo, dict):
        arquivo.write(json.dumps(conteudo, indent=2, ensure_ascii=False))
      else:
        arquivo.write(conteudo)
  except IOError as e:
    print(f"Erro ao salvar arquivo: {e}")