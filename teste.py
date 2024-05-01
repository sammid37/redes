import socket

SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000

def send_udp_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(request, (SERVER_IP, SERVER_PORT))
        response, _ = sock.recvfrom(1024)
        return response

def send_raw_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) as sock:
        sock.sendto(request, (SERVER_IP, SERVER_PORT))
        response, _ = sock.recvfrom(1024)
        return response

def format_request(req_type, identifier):
    return bytes([0b0000 << 4 | req_type, identifier >> 8, identifier & 0xFF])

def parse_response(response):
    res_type = response[0] >> 4
    identifier = (response[0] & 0x0F) << 8 | response[1]
    response_size = response[2]
    response_data = response[3:3+response_size]
    return res_type, identifier, response_data.decode('utf-8')

def main():
    while True:
        print("Escolha uma opção:")
        print("1. Data e hora atual")
        print("2. Uma mensagem motivacional para o fim do semestre")
        print("3. A quantidade de respostas emitidas pelo servidor até o momento")
        print("4. Sair")

        choice = input("Opção: ")
        if choice == '4':
            print("Saindo...")
            break

        try:
            choice = int(choice)
            if choice < 1 or choice > 4:
                raise ValueError
        except ValueError:
            print("Opção inválida. Por favor, escolha um número de 1 a 4.")
            continue

        identifier = int(input("Identificador (entre 1 e 65535): "))
        if identifier < 1 or identifier > 65535:
            print("Identificador inválido. Por favor, escolha um número entre 1 e 65535.")
            continue

        if choice == 1:
            request = format_request(0b0000, identifier)
        elif choice == 2:
            request = format_request(0b0001, identifier)
        elif choice == 3:
            request = format_request(0b0010, identifier)

        if choice != 4:
            try:
                
                response = send_udp_request(request)
                # else:
                #     response = send_raw_request(request)
                res_type, identifier, data = parse_response(response)
                print("Resposta recebida:")
                print(data)
            except Exception as e:
                print("Erro ao enviar/receber dados:", e)

if __name__ == "__main__":
    main()
