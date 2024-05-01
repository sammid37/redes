import time
from termcolor import colored
from datetime import datetime
from socket import socket, AF_INET, SOCK_DGRAM

class UDP_Client:
  def __init__(self, server_name:str, server_port:int):
    self.server_name = server_name
    self.server_port = server_port
    self.client_socket = socket(AF_INET, SOCK_DGRAM)

  def send_udp_request(self, request):
    self.client_socket.sendto(request, (self.server_name, self.server_port))
    response, _ = self.client_socket.recvfrom(1024)
    return response

  def format_request(self, req_type, identifier):
    return bytes([0b0000 << 4 | req_type, identifier >> 8, identifier & 0xFF])

  def parse_response(self, response):
    res_type = response[0] >> 4
    identifier = (response[0] & 0x0F) << 8 | response[1]
    response_size = response[2]
    response_data = response[3:3+response_size]
    return res_type, identifier, response_data.decode('utf-8')

  def execute_method(self, method_number):
    identifier = int(input("Identificador (entre 1 e 65535): "))
    if identifier < 1 or identifier > 65535:
        print("Identificador inválido. Por favor, escolha um número entre 1 e 65535.")
        exit()

    if method_number == 1:
      request = self.format_request(0b0000, identifier)
    elif method_number == 2:
      request = self.format_request(0b0001, identifier)
    elif method_number == 3:
      request = self.format_request(0b0010, identifier)
    else:
      raise ValueError("Número de método inválido para UDP_Server")

    try:
      response = self.send_udp_request(request)
      res_type, identifier, data = self.parse_response(response)
      print("Resposta recebida:")
      print(data)
    except Exception as e:
      print("Erro ao enviar/receber dados:", e)

  def close(self):
    self.client_socket.close()