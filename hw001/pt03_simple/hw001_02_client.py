import socket
from util import *


def send(host_addr: str, host_port: int):
    chunk_size = 1024
    data_to_send = b''

    file_path = get_path()
    print_files(file_path)
    file_name = get_filename()

    try:
        data_to_send = read_file(file_name, file_path)
    except FileNotFoundError as exc:
        print(f'NOT FOUND! {exc}')
        return
    except Exception as exc:
        print(f'{exc}')

    client_socket = socket.socket()
    client_socket.connect((host_addr, host_port))

    file_string = f'FILE:{file_name}:{str(len(data_to_send))}'.encode()

    print(f'{file_string=}')
    answer = input("correct? (y/n): ")
    if answer not in 'Yy':
        return

    client_socket.send(file_string)

    print(client_socket.recv(10))

    send_limit = data_to_send.__sizeof__()

    for i in range(0, send_limit, chunk_size):
        portion = data_to_send[i:i + chunk_size]
        client_socket.send(portion)

    client_socket.close()


# =============================================================================
def starter():
    host_addr = '127.0.0.1'
    host_port = 8020
    send(host_addr, host_port)


# =============================================================================
if __name__ == '__main__':
    starter()
