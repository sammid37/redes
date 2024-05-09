# Redes de Computadores I 
# Projeto Final - Utilitários do Projeto
# Christopher Alec Tavares, Enthony Miguel Gomes de Araújo e Samantha Dantas Medeiros
# Maio de 2024

import os
import socket
from termcolor import colored

# Acabou não indo para a versão final do projeto, mas era algo puramente estético
def limpar_tela():
  """Limpa o console"""
  if os.name == 'nt': # Windows
    os.system('cls')
  else: # Linux, macOS
    os.system('clear')

# Utilizado apenas para a implementaçaõ do RAW
def get_local_ip():
  """Obtém o endereço IP local da máquina retornando 
  o nome host local e o convertendo em um endereço IP"""
  try:
    return socket.gethostbyname(socket.gethostname())
  except socket.error as e:
    print(colored(f"Erro ao obter o IP local: {e}", "red"))
    return None