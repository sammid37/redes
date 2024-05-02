# Redes de Computadores I 
# Projeto Final - Arquivo Principal
# Christopher A. T, Samantha D. M. e Enthony Miguel
# Maio de 2024

import os
import sys
import time
sys.path.append('src')

from utils import limpar_tela
from termcolor import colored
from udp_impl import UDP_Client
# from raw_impl import RAW_Client

SERVER_NAME = "15.228.191.109"
SERVER_PORT = 50000

class ServerFactory:
  def create_server(self, protocolo, identificador):
    if protocolo == "UDP":
      return UDP_Client(SERVER_NAME,SERVER_PORT, identificador)
    elif protocolo == "RAW":
      # return RAW_Server()
      pass
    else:
      raise ValueError("Protocolo não suportado")

def menuMsg() -> None:
  print(colored("🪆 BEM-VINDO!","black", "on_white", attrs=["bold"]))
  print("1 - Data e hora atual")
  print("2 - Mensagem motivacional")
  print("3 - Qtd. de requisições atendidas")
  print("4 - Sair\n")

while True:
  try:
    # limpar_tela()
    factory = ServerFactory()
    menuMsg()

    protocolo = "UDP" #input("Digite o protocolo (UDP ou RAW): ").upper()
    opcao = int(input("Digite o número do método (1, 2 ou 3): "))
    identificador = 65534
    if identificador < 1 or identificador > 65535:
      print("Identificador inválido. Por favor, escolha um número entre 1 e 65535.")

    if opcao == 4:
      print("Encerrando...")
      server.close()
      break

    # Cria um objeto de cliente de protocolo utilizando
    # o padrão Factory
    server = factory.create_server(protocolo, identificador)
    server.execute_method(opcao)

  except ValueError as e:
    print(colored(("Erro:", e), "red"))