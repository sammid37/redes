# Redes de Computadores I 
# Projeto Final - Arquivo Principal
# Christopher Alec Tavares, Enthony Miguel Gomes de Araújo e Samantha Dantas Medeiros
# Maio de 2024

import sys
import random
from termcolor import colored

# Adiciona o diretório ao path para acessar os 
# arquivos dentro do diretório src e não dar erro nas importações
sys.path.append('src') 

from udp_impl import UDP_Client 
from udp_raw_impl import UDP_RAW_Client 
from constantes import SERVER_NAME, SERVER_PORT

class ServerFactory:
  def create_server(self, protocolo, identificador):
    """Istancia um objeto Client de algum socket dado o seu tipo de protocolo."""
    if protocolo == "UDP":
      return UDP_Client(SERVER_NAME, SERVER_PORT, identificador)
    elif protocolo == "RAW":
      return UDP_RAW_Client(SERVER_NAME, SERVER_PORT, identificador)
    else:
      raise ValueError("Protocolo não suportado.")

def menuMsg() -> None:
    """Exibe a mensagem do menu comum a todos os protocolos implementados"""
    print(colored("🪆  BEM-VINDO!", "blue", attrs=["bold"]))
    print("1 - Data e hora atual")
    print("2 - Mensagem motivacional")
    print("3 - Qtd. de requisições atendidas")
    print("4 - Sair\n")

def main():
  while True:
    try:
      menuMsg()
      protocolo = input("Digite o protocolo (UDP ou RAW): ").upper() # tudo em uppercase para facilitar comparação
      opcao = int(input("Digite o número do método (1, 2 ou 3, 4 para Sair): "))
      identificador = random.randint(1, 65535) # gerando um identificador aleatório dentro do intervalo informado na especificação

      if opcao == 4:
        print("Encerrando...")
        break

      # Utilizando o Padrão de Projeto Factory para ficar criando objetos socket
      # Boa prática para caso haja futuras implementações de outros clientes de protocolo
      # Lembrando que todos devem ter o método execute_method() e closed()
      # implementado para que o padrão funcione
      factory = ServerFactory()
      server = factory.create_server(protocolo, identificador)
      server.execute_method(opcao) # faz a requisição com base na opção fornecida
      server.close() # sempre fechando a conexão após o envio de requisições

    # Tratamentos de exceção específico para erro de Valor e erro genéricos (inesperados)
    except ValueError as e:
      print(colored(f"Erro: {e}", "red"))
    except Exception as e:
      print(colored(f"Erro inesperado: {e}", "red"))
      break 

if __name__ == "__main__":
  main()
