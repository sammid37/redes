import socket
import struct
from termcolor import colored


def get_local_ip():
    """Obtém o endereço IP local da máquina."""
    return socket.gethostbyname(socket.gethostname())

class UDP_RAW_Client:
    def __init__(self, server_name: str, server_port: int, identificador: int) -> None:
        self.server_name = server_name
        self.server_port = server_port
        self.identificador = identificador
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.local_ip = get_local_ip()  # Armazena o IP local

    #constrói o payload da requisição e cria o cabeçalho UDP adequado
    def send_request(self, tipo_requisicao):
        payload = struct.pack('>BH', tipo_requisicao, self.identificador)
        udp_header = self.create_udp_header(payload)
        packet = udp_header + payload
        self.client_socket.sendto(packet, (self.server_name, self.server_port))
        data, addr = self.client_socket.recvfrom(1024)
        return data

    #constroi o cabeçalho UDP com base nos parâmetros
    def create_udp_header(self, payload):
        source_port = 59155
        dest_port = self.server_port
        length = 8 + len(payload)
        checksum = 0
        udp_header = struct.pack('!HHHH', source_port, dest_port, length, checksum)
        pseudo_header = struct.pack('!4s4sBBH', socket.inet_aton(self.local_ip), socket.inet_aton(self.server_name), 0, socket.IPPROTO_UDP, length)
        checksum = self.calculate_checksum(pseudo_header + udp_header + payload)
        udp_header = struct.pack('!HHHH', source_port, dest_port, length, checksum)
        return udp_header

    #calculo do checksum e ajuste
    def calculate_checksum(self, data):
        if len(data) % 2 != 0:
            data += b'\x00'  # Adiciona um byte zero se o tamanho dos dados for ímpar
        checksum = 0
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i + 1]  # Soma os valores dos bytes em pares
        checksum = (checksum >> 16) + (checksum & 0xFFFF)  # Wraparound
        checksum += (checksum >> 16)  # Outra etapa de wraparound se necessário
        return ~checksum & 0xFFFF  # Inverte os bits do checksum resultante


    #desempacota a resposta, ignorando os cabeçalhos IP e UDP, e extraindo informações
    def parse_response(self, response):
        resposta = response[28:]  # Ignora os cabeçalhos IP e UDP
        
        res_req = resposta[0] >> 4
        res_type = resposta[0] & 0x0F
        identificador = (resposta[1] << 8) | resposta[2]
        tamanho_resposta = resposta[3]


        if res_req == 1:  # Verifica se é uma resposta
            if res_type == 0:  # Requisição de data e hora
                response_data = resposta[4:4+tamanho_resposta].decode('utf-8')
            elif res_type == 1:  # Requisição de frase motivacional
                response_data = resposta[4:4+tamanho_resposta].decode('utf-8')
            elif res_type == 2:  # Requisição de número de respostas
                response_data = int.from_bytes(resposta[4:4+tamanho_resposta], byteorder='big', signed=False)
            elif res_type == 3:  # Requisição inválida
                response_data = "Requisição inválida"
            else:
                response_data = "Tipo de resposta desconhecido"
        else:
            response_data = "Não é uma resposta válida"

        return res_type, identificador, response_data


    #solicita o envio de uma requisição específica e imprime a resposta para o usuario
    def execute_method(self, opcao: int):
        response = self.send_request(opcao - 1)
        res_type, identificador, dados = self.parse_response(response)
        tipo_msg = ["","Data e hora", "Frase motivacional", "Nº de requisições atendidas"]
        print(colored("\nResposta recebida!", "green"))
        print(f"{tipo_msg[opcao]}: {dados}")
        

    def close(self):
        self.client_socket.close()

