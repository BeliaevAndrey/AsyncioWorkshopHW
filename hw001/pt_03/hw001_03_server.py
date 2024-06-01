import os.path
import socket
from util import *

FILES_PATH = os.path.abspath('server_files')

MENU = [
    'list files',
    'upload file',
    'download file',
    'leave',
]


def start_listen(host_addr: str, host_port: int) -> int:
    buffer = b''
    commands_list = '\n'.join([
        f'{no}.{item}' for no, item in enumerate(MENU, start=1)
    ])

    receiver_socket = socket.socket()
    receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receiver_socket.bind((host_addr, host_port))
    receiver_socket.listen()

    print(f"Listening at: {host_addr}:{host_port}")

    connection, client_address = receiver_socket.accept()

    file_size = 0
    file_name = 'tmp_buffer'

    try:
        while True:
            data = connection.recv(1024)
            print('cycling:', data)
            if data == b'handshake':
                connection.send(commands_list.encode())
                if data:
                    data = b''
            elif data.startswith(b'COMMAND:'):
                command = int(data.decode('utf-8').split(':')[1])
                match command:
                    case 1:
                        break
                    case 2:
                        pass
                    case 3:
                        pass
                    case 4:
                        pass
                    case _:
                        connection.send("Unknown command".encode())

            elif data.startswith(b'FILE:'):
                line = data.decode()
                print(f'{line=}')
                file_params = line.split(':')
                file_name = file_params[1]
                file_size = file_params[-1]

                print(f'{file_name=}\n{file_size=}\n{file_params=}')

                try:
                    file_size = int(file_size)
                    print(f'Trying to get a file of size: {file_size}')
                    connection.send(b'Ready')
                except Exception as exc:
                    print(f'\033[31m{exc.__class__.__name__}: {exc}\033[0m')
                    connection.close()
                    return 1
                # finally:
                #     data = b''
            elif len(data) and len(data) < 1024 or len(buffer) == file_size:
                buffer += data
                print(f'{len(buffer)=}')
                write_file(buffer, file_name, file_dir=FILES_PATH)
                # buffer = b''
                return 0
            else:
                buffer += data
    finally:
        print('\n\n')
        receiver_socket.close()
        return 0


# =============================================================================
def starter():
    host_addr = '127.0.0.1'
    host_port = 8020
    flag = 0
    while not flag:
        flag = start_listen(host_addr, host_port)


# =============================================================================
if __name__ == '__main__':
    starter()
