# Redes de Computadores I 
# Projeto Final - Implementação UDP
# Christopher Alec Tavares, Enthony Miguel Gomes de Araújo e Samantha Dantas Medeiros
# Maio de 2024

from termcolor import colored
from socket import socket, AF_INET, SOCK_DGRAM

class UDP_Client:
  def __init__(self, server_name:str, server_port:int, identificador:int) -> None:
    self.server_name = server_name
    self.server_port = server_port
    self.identificador = identificador
    self.client_socket = socket(AF_INET, SOCK_DGRAM)

  def send_udp_request(self, request:bytes) -> bytes:
    """Envia requisição para o servidor e retorna a resposta"""
    self.client_socket.sendto(request, (self.server_name, self.server_port))
    response, _ = self.client_socket.recvfrom(80000)
    return response

  def format_request(self, req_type:bytes, identifier:int) -> bytes:
    """Formata a requisição em Bytes"""
    return bytes([0b0000 << 4 | req_type, identifier >> 8, identifier & 0xFF])

  def parse_response(self, response:bytes):
    """Analisa a resposta vinda do servidor e a decodifica."""
    # Primeiro Byte da resposta
    res_req = response[0] >> 4 # deslocamento à direita do valor por 4 bits
    res_type = response[0] & 0x0F # operação OR bit a bit utilizando a máscara para extrair os 4 bits
    # Combinação do Segundo e Terceiro Byte da resposta (or bit a bit), formando um identificador de 16 bits
    # Deslocando 8 bits à esquerda do Segundo Byte
    identifier = (response[1] << 8) | response[2] 
    response_size = response[3]

    if res_req == 1:  # Verifica se é uma resposta (bits 0001)
      # agora verifica o tipo de requisição 
      # (data e hora, frase motivacional ou nº de requisições atendidas)
      # e decodefica 
      if res_type == 0:  # Requisição de data e hora
        response_data = response[4:].decode('utf-8')
      elif res_type == 1:
        response_data = response[4:].decode('utf-8')
      elif res_type == 2:
        response_data = int.from_bytes(response[4:], byteorder='big', signed=False)
      elif res_type == 3:
        response_data = "Requisição inválida"
      else:
        response_data = "Tipo de resposta desconhecido"
    else:
      response_data = "Não é uma resposta válida"

    return res_type, identifier, response_data

  def execute_method(self, opcao:int) -> None:
    """Executa um dos métodos do servidor dada a opção escolhida pelo usuário e exibe a resposta.
    Inicialmente formantando a requisição para então enviá-la para o servidor e finalmente exibir
    a resposta solicitação do usuário """
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

      # Estamos utilizando esta lista puramente para facilitar a exibição da resposta
      tipo_msg = ["","Data e hora", "Frase motivacional", "Nº de requisições atendidas"]
      print(colored("\n✅ Resposta recebida!", "green"))
      print(f"{tipo_msg[opcao]}: {data}\n")

    except Exception as e:
      print(colored(("Erro ao enviar/receber dados:", e),"red"))

  def close(self):
    """Fecha a conexão do cliente"""
    self.client_socket.close()