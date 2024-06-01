import socket
from util import *


MENU = [
    'list files',
    'upload file',
    'download file',
    'leave',
]


def send(host_addr: str, host_port: int):
    chunk_size = 1024
    data_to_send = b'handshake'

    client_socket = socket.socket()
    client_socket.connect((host_addr, host_port))
    client_socket.send(data_to_send)
    data_to_send = b''  # clear data at this stage

    print(client_socket.recv(chunk_size).decode('utf-8'))

    file_path = get_path()
    print_files(file_path)
    file_name = get_filename()

    while True:
        try:
            data_to_send = read_file(file_name, file_path)
            break
        except FileNotFoundError as exc:
            print(f'NOT FOUND! {exc.__class__.__name__} {exc}')
            return
        except Exception as exc:
            print(f'{exc.__class__.__name__}: {exc}')

    file_string = f'FILE:{file_name}:{str(len(data_to_send))}'.encode()

    print(f'{file_string=}')
    while True:
        answer = input("correct? (y/n): ")
        if answer in 'Nn':
            return
        if answer in 'Yy':
            break
        print("I didn't catch... Try again.")

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
