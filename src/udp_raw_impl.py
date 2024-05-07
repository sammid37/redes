import time
from utils import limpar_tela
from termcolor import colored
from socket import socket, AF_INET, SOCK_DGRAM
from constantes import SERVER_NAME, SERVER_PORT


class UDP_RAW_Client:
  def __init__(self, server_name:str, server_port:int, identificador:int) -> None:
    self.server_name = server_name
    self.server_port = server_port
    self.identificador = identificador
    self.client_socket = socket(AF_INET, SOCK_DGRAM)
    self.client_socket.connect(SERVER_NAME, SERVER_PORT)

  def execute_method():
    pass