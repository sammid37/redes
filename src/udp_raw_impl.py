# Redes de Computadores I 
# Projeto Final - Implementação RAW
# Christopher Alec Tavares, Enthony Miguel Gomes de Araújo e Samantha Dantas Medeiros
# Maio de 2024

import struct
import socket
from termcolor import colored
from utils import get_local_ip

class UDP_RAW_Client:
  def __init__(self, server_name: str, server_port: int, identificador: int) -> None:
    self.server_name = server_name
    self.server_port = server_port
    self.identificador = identificador
    self.local_ip = get_local_ip()

    try:
      # O IPPROTO_UDP informa que vamos criar pacotes UDP
      # AF_INET é a família de protocolos de endereços IP versão 4
      self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
    except Exception as e:
      print(colored(f"Erro ao criar o socket: {e}", "red"))
      self.client_socket = None

  def send_request(self, tipo_requisicao):
    """Empacotamento da requisição usando struct."""

    # Caso o socket não tinha sido criado ou ele não 
    # possua informações sobre o IP local, a requisição não é feita
    if self.client_socket is None or self.local_ip is None:
      return None

    # Empacotamento da requisição usando struct 
    # convertendo entre valores e representações bytes
    # '>BH' significa que o formato é big-endian (network byte order),
    # 'B' é um inteiro sem sinal de 1 byte e 'H' é um inteiro sem sinal de 2 bytes.
    payload = struct.pack('>BH', tipo_requisicao, self.identificador)
    
    # Criação do cabeçalho UDP que será colocado antes do payload.
    udp_header = self.create_udp_header(payload)

    # O pacote final é o cabeçalho UDP seguido pelo payload.
    packet = udp_header + payload
    
    # Tenta realizar o envio da requisição
    try:    
      self.client_socket.sendto(packet, (self.server_name, self.server_port))
      # Espera uma resposta com buffer de tamanho 1024 bytes.
      data, _ = self.client_socket.recvfrom(1024)
    except socket.error as e:
      print(colored(f"Erro ao enviar/receber dados: {e}", "red"))
      return None
    
    # Caso a requisição seja bem sucedida, a resposta não codificada é retornada
    return data

  def create_udp_header(self, payload):
    """Constrói o cabeçalho UDP com base nos parâmetros, incluindo o checksum."""
    # Especifica a porta de origem e de destino para o pacote UDP.
    source_port = 59155
    dest_port = self.server_port

    # O tamanho total do datagrama UDP é 8 bytes de cabeçalho + tamanho do payload.
    length = 8 + len(payload)
    checksum = 0  # O checksum é inicializado com 0 para poder ser calculado.
    
    # Empacota o cabeçalho UDP sem o checksum final.
    # Quatro valores inteiros sem sinal de 16 bits (dois bytes cada) na ordem big-endian
    udp_header = struct.pack('!HHHH', source_port, dest_port, length, checksum)
    
    # Pseudo-header necessário para o cálculo do checksum conforme definido pelo protocolo IP
    # !: Empacotado na ordem big-endian
    # 4s4s: dois campos de 4 bytes cada, representados por strings de 4 caracteres (representando o IP)
    # BB: dois campos de 1 byte cada, representa valores específicos
    # H: campo de 2 bytes, representa o valor da porta
    pseudo_header = struct.pack('!4s4sBBH',
                                socket.inet_aton(self.local_ip),
                                socket.inet_aton(self.server_name),
                                0, socket.IPPROTO_UDP, length)

    # Calcula o checksum com pseudo-header, cabeçalho UDP e payload.
    # print(colored("Calculando checksum para o cabeçalho UDP e payload...","blue"))
    checksum = self.calculate_checksum(pseudo_header + udp_header + payload)

    # Reempacota o cabeçalho UDP agora incluindo o checksum calculado e o retorna
    udp_header = struct.pack('!HHHH', source_port, dest_port, length, checksum)
    return udp_header

  def calculate_checksum(self, data):
    """Calcula o checksum usando soma de complemento a um"""
    if len(data) % 2 != 0:
      # Se o comprimento dos dados for ímpar, adiciona um byte zero no final.
      data += b'\x00'
    
    checksum = 0

    # Itera sobre cada par de bytes e os soma mantendo apenas os últimos 16 bits.
    # Do 0 até o tamanho dos dados, pulando de em 2 em 2
    for i in range(0, len(data), 2):
      word = (data[i] << 8) + data[i + 1] # formação do valor de 16bits
      checksum += word # adiciona a palavra ao checksum
      checksum = (checksum & 0xFFFF) + (checksum >> 16) # garantindo que o checksum tenha apenas 16 bits
      
      # Descomente para ver o cálculo do checksum sendo realizado
      # print(f"Word formado: {word:016b} (decimal: {word})")
      # print(f"Checksum parcial: {checksum:016b} (decimal: {checksum})\n")

    # Finaliza o cálculo do checksum invertendo os bits.
    checksum = ~checksum & 0xFFFF
    
    # Descomente para ver o resultado final do checksum
    # print(colored(f"✅ Cálculo final do Checksum: {checksum:016b} (decimal: {checksum})","green"))

    return checksum

  def parse_response(self, response):
    """Desempacota a resposta, ignorando os cabeçalhos IP e UDP."""
    
    if response is None:
      return None, None, "Erro na comunicação"
    
    # Ignora os cabeçalhos IP e UDP que são os primeiros 28 Bytes.
    resposta = response[28:]

    # O byte de resposta é dividido para identificar o tipo de requisição e o tipo de resposta.
    res_req = resposta[0] >> 4
    res_type = resposta[0] & 0x0F
    
    # O identificador é formado pelos próximos 2 Bytes.
    identificador = (resposta[1] << 8) | resposta[2]
    
    # Tamanho da resposta está no próximo Byte.
    tamanho_resposta = resposta[3]

    if res_req == 1:  # Se é uma resposta
      # agora verifica o tipo de requisição 
      # (data e hora, frase motivacional ou nº de requisições atendidas)
      # e decodefica (em utf-8 para os dois primeiros tipos de requisição 
      # e inteiro para o último tipo de requisição válido)
      if res_type == 0:
        response_data = resposta[4:4 + tamanho_resposta].decode('utf-8')
      elif res_type == 1:
        response_data = resposta[4:4 + tamanho_resposta].decode('utf-8')
      elif res_type == 2: # ordem dos bytes: big-endian, números sem sinal
        response_data = int.from_bytes(resposta[4:4 + tamanho_resposta], byteorder='big', signed=False)
      elif res_type == 3:
        response_data = "Requisição inválida"
      else:
        response_data = "Tipo de resposta desconhecido"
    else:
      response_data = "Não é uma resposta válida"
    # e retorna os dados
    return res_type, identificador, response_data

  def execute_method(self, opcao: int, max_retries=3):
    """Envia uma requisição específica e lida com a resposta ou retransmissão em caso de erro."""

    # Limitando a 3 tentativas
    retries = 0
    while retries < max_retries:
      # Envia requisição, lembrando que na especificação os tipos são 0, 1 e 2,
      # por isso decrementamos 1 da opção enviada pelo usuário
      response = self.send_request(opcao - 1)
      # retorna uma tupla, mas o que interessa são os dados
      res_type, identificador, dados = self.parse_response(response)
      
      if dados == "Erro na comunicação":  # Se houver erro na comunicação, tenta novamente.
        print(colored("Erro detectado. Tentando novamente...", "yellow"))
        retries += 1
      else:
        # Estamos utilizando esta lista puramente para facilitar a exibição da resposta
        tipo_msg = ["", "Data e hora", "Frase motivacional", "Nº de requisições atendidas"]
        print(colored("\nResposta recebida!", "green"))
        print(f"{tipo_msg[opcao]}: {dados}\n")
        break
    else:
      print(colored("Número máximo de tentativas alcançado. Falha na comunicação.", "red"))

  def close(self):
    """Fecha o socket do cliente."""
    if self.client_socket is not None:
      self.client_socket.close()
