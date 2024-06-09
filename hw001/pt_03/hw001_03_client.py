import socket
import traceback

from util import *

MENU = [
    'list files',
    'upload file',
    'download file',
    'leave',
]
FILES_PATH = 'downloads'
CHUNK_SIZE = 1024


def send(host_addr: str, host_port: int):
    data_to_send = b'handshake'
    file_name = ''
    server_file_list = []

    client_socket = socket.socket()
    client_socket.connect((host_addr, host_port))
    client_socket.send(data_to_send)

    while True:
        answer = client_socket.recv(CHUNK_SIZE)
        if answer.startswith(b'MENU:'):
            menu = answer.decode('utf-8').split(':')[1]  # get a menu
            print(menu)
        elif answer.startswith(b'FILE_LIST:'):
            server_file_list = answer.decode('utf-8').split(':')[1].split('\n')
            file_list = '\n'.join([f'{n:<4}{name}'
                                   for n, name in enumerate(server_file_list, start=1)])
            print(file_list)
        command = read_command(MENU)
        match command:
            case '1':  # ask file-list
                data_to_send = f'COMMAND:{command}'.encode()
                client_socket.send(data_to_send)
            case '2':  # upload file
                # command_to_send = f'COMMAND:{command}'.encode()
                # print(f'{command_to_send = }')
                # client_socket.send(command_to_send)
                break
            case '3':  # download file
                if not server_file_list:
                    print('Choose a file, please.')
                    return
                file_name = server_file_list[read_int(len(server_file_list)) - 1]
                command_to_send = f'COMMAND:{command}:{file_name}'.encode()
                print(f'{command_to_send = }')
                client_socket.send(command_to_send)
                break
            case 'EXIT':  # leave
                client_socket.send(command.encode())
                client_socket.close()
                return
            case _:
                print("I didn't catch...")

    # ===== upload file section =====
    if command == '2':
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

        command_to_send = f'COMMAND:{command}:{file_name}'.encode()

        file_string = f'FILE:{file_name}:{str(len(data_to_send))}'.encode()

        print(f'{file_string=}')
        if not short_answer():
            return
        client_socket.send(command_to_send)
        client_socket.send(file_string)

        try:
            client_socket.settimeout(2)
            answer = client_socket.recv(CHUNK_SIZE)
            print(answer)
            if not answer == b'READY':
                print(answer.decode())
                print('I send \'y\'.')
                client_socket.send(b'y')
                client_socket.recv(CHUNK_SIZE)
        except TimeoutError as exc:
            traceback.print_exc()
            traceback.print_tb(exc.__traceback__)
            return

        # print(client_socket.recv(10))

        send_limit = data_to_send.__sizeof__()

        for i in range(0, send_limit, CHUNK_SIZE):
            # if short_answer('Crash test?'):
            #     crash_test(client_socket)
            portion = data_to_send[i:i + CHUNK_SIZE]
            client_socket.send(portion)

        client_socket.close()

    # ==== download file section
    if command == '3':
        buffer = b''

        data = client_socket.recv(CHUNK_SIZE).decode('utf-8')
        file_string = data.split(':')[1:]
        print(file_string)
        if not short_answer():
            return

        client_socket.send(b'READY')

        file_size = int(file_string[-1])

        # if short_answer('Crash test?'):
        #     crash_test(client_socket)

        while True:
            data = client_socket.recv(CHUNK_SIZE)
            if len(data) and len(data) < CHUNK_SIZE or len(buffer) == file_size:
                buffer += data
                print(f'{len(buffer)=}')
                if buffer:
                    write_file(buffer, file_name, file_dir=FILES_PATH)
                break
            else:
                buffer += data

        client_socket.close()


def short_answer(question: str = 'correct?') -> bool:
    while True:
        answer = input(f"{question} (y/n): ")
        if answer in 'Nn':
            return False
        if answer in 'Yy':
            return True
        print("I didn't catch... Try again.")


def read_command(commands: list) -> str:
    while True:
        command = input("Input command (integer): ")
        if command.isdigit():
            if int(command) < len(commands):
                return command
            if int(command) == len(commands):
                return 'EXIT'
        print("Wrong input. Try again.")


def read_int(lim: int):
    while True:
        num = int(input(f'Input number (1 - {lim}):  '))
        if 0 < num <= lim:
            return num
        print("Wrong input. Try again.")


def crash_test(client_socket):
    client_socket.recv(CHUNK_SIZE)
    client_socket.recv(CHUNK_SIZE)
    client_socket.recv(CHUNK_SIZE)
    client_socket.recv(CHUNK_SIZE)
    raise SystemError

# =============================================================================
def starter():
    host_addr = '127.0.0.1'
    host_port = 8020
    send(host_addr, host_port)


# =============================================================================
if __name__ == '__main__':
    starter()
