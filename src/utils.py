import os

def limpar_tela():
  """Limpa o console"""
  if os.name == 'nt': # Windows
    os.system('cls')
  else: # Linux, macOS
    os.system('clear')