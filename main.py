# Redes de Computadores I 
# Projeto Final - Arquivo Principal
# Christopher A. T, Samantha D. M. e Enthony Miguel
# Maio de 2024

import sys
sys.path.append('D:\\UFPB\\Projeto\\redes\\src')  # Adiciona o diretório ao path do Python

from udp_raw_impl import UDP_RAW_Client  # Importa a classe UDP_RAW_Client
from constantes import SERVER_NAME, SERVER_PORT
from termcolor import colored

class ServerFactory:
    def create_server(self, protocolo, identificador):
        if protocolo == "UDP":
            from udp_impl import UDP_Client  # Certifique-se de que esta classe esteja implementada
            return UDP_Client(SERVER_NAME, SERVER_PORT, identificador)
        elif protocolo == "RAW":
            return UDP_RAW_Client(SERVER_NAME, SERVER_PORT, identificador)
        else:
            raise ValueError("Protocolo não suportado")

def menuMsg() -> None:
    print(colored("🪆 BEM-VINDO!", "black", "on_white", attrs=["bold"]))
    print("1 - Data e hora atual")
    print("2 - Mensagem motivacional")
    print("3 - Qtd. de requisições atendidas")
    print("4 - Sair\n")

def main():
    while True:
        try:
            menuMsg()
            protocolo = input("Digite o protocolo (UDP ou RAW): ").upper()
            opcao = int(input("Digite o número do método (1, 2 ou 3, 4 para Sair): "))
            identificador = 23777  # Exemplo de identificador fixo

            if opcao == 4:
                print("Encerrando...")
                break

            factory = ServerFactory()
            server = factory.create_server(protocolo, identificador)
            server.execute_method(opcao)
            server.close()

        except ValueError as e:
            print(colored(f"Erro: {e}", "red"))
        except Exception as e:
            print(colored(f"Erro inesperado: {e}", "red"))
            break  # Para segurança, encerra o loop em caso de erro inesperado.

if __name__ == "__main__":
    main()
