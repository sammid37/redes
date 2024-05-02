import time
from utils import limpar_tela
from termcolor import colored
from socket import socket, AF_INET, SOCK_DGRAM

class UDP_Client:
  def __init__(self, server_name:str, server_port:int, identificador:int):
    self.server_name = server_name
    self.server_port = server_port
    self.identificador = identificador
    self.client_socket = socket(AF_INET, SOCK_DGRAM)

  # def f_avancar():
  #   avancar = input("Pressione ENTER para continuar...")
  #   if not avancar: 
  #     limpar_tela()

  def send_udp_request(self, request:bytes) -> bytes:
    """Envia requisição para o servidor"""
    self.client_socket.sendto(request, (self.server_name, self.server_port))
    response, _ = self.client_socket.recvfrom(80000)
    return response

  def format_request(self, req_type:bytes, identifier:int) -> bytes:
    """Formata a requisição em Bytes"""
    return bytes([0b0000 << 4 | req_type, identifier >> 8, identifier & 0xFF])

  def parse_response(self, response:bytes):
    res_type = response[0] >> 4 # Desloca 4 bits para a direita
    identifier = (response[0] & 0x0F) << 8 | response[1]
    response_size = response[2]
    response_data = response[3:3+response_size]
    return res_type, identifier, response_data.decode('utf-8', errors='ignore')

  def execute_method(self, opcao:int) -> None:
    """Executa um dos métodos do servidor dada a opção escolhida pelo usuário e exibe a resposta"""
    if opcao == 1:
      request = self.format_request(0b0000, self.identificador)
    elif opcao == 2:
      request = self.format_request(0b0001, self.identificador)
    elif opcao == 3:
      request = self.format_request(0b0010, self.identificador)
    else:
      raise ValueError("Número de método inválido para Cliente UDP.")

    try:
      response = self.send_udp_request(request)
      res_type, idt, data = self.parse_response(response)
      tipo_msg = ["","Data e hora", "Frase motivacional", "Nº de requisições atendidas"]
      print(colored("\nResposta recebida!", "green"))
      print(f"{tipo_msg[opcao]}: {data}")

      # self.f_avancar()
    except Exception as e:
      print(colored(("Erro ao enviar/receber dados:", e),"red"))
      # self.f_avancar()

  def close(self):
    """Fecha a conexão do cliente"""
    self.client_socket.close()