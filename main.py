# Redes de Computadores I 
# Projeto Final - Arquivo Principal
# Christopher A. T, Samantha D. M. e ??? 
# Maio de 2024

import os
import sys
import time
sys.path.append('src')

from termcolor import colored
from udp_impl import UDP_Client
# from raw_impl import RAW_Client

class ServerFactory:
  def create_server(self, protocol):
    if protocol == "UDP":
      return UDP_Client("15.228.191.109",50000)
    elif protocol == "RAW":
      # return RAW_Server()
      pass
    else:
      raise ValueError("Protocolo não suportado")

def menuMsg() -> None:
  print(colored("Bem-vindo ao servidor!","blue"))
  print(colored((("-"*8) + " MENU"),"blue"))
  print("1 - Data e hora atual")
  print("2 - Mensagem motivacional")
  print("3 - Qtd. de requisições atendidas")
  print("4 - Sair\n")

while True:
  try:
    factory = ServerFactory()
    menuMsg()
    protocolo = input("Digite o protocolo (UDP ou TCP): ").upper()
    opcao = int(input("Digite o número do método (1, 2 ou 3): "))
    if opcao == 4:
      print("Encerrando...")
      break
    # time.sleep(1)
    # os.system("clear")
    server = factory.create_server(protocolo)
    server.execute_method(opcao)
    server.close()
  
  except ValueError as e:
    print(colored(("Erro:", e), "red"))