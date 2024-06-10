import socket
import select
import time
import errno

from datetime import datetime as _dt
from typing import TypeAlias
import traceback
import os

from util import SLogger, multiproc_count

SOCK: TypeAlias = socket.socket
CHUNK_SIZE = 1024

logger = SLogger('Server')


def listener(host_addr: str, host_port: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host_addr, host_port))
    server_socket.listen()
    server_socket.setblocking(False)

    print(f"Listening at {host_addr}:{host_port}")

    clients = {}

    inputs = [server_socket]  # rlist -- wait until ready for reading
    outputs = []  # wlist -- wait until ready for writing
    # xlist = []    # xlist -- wait for an "exceptional condition"

    try:
        while True:
            readable, writable, exceptional = select.select(
                inputs, outputs, inputs, 1)

            if (not readable and not writable and not exceptional) and exit_check():
                print("Exiting...")
                break

            for sck in readable:
                if sck is server_socket:
                    client_sock, addr = server_socket.accept()
                    print(f"Connection: {addr}")
                    client_sock.setblocking(False)
                    inputs.append(client_sock)
                    clients[client_sock] = {'addr': addr, 'data': b'', 'result': None}
                else:
                    try:
                        data = sck.recv(CHUNK_SIZE)
                        if data:
                            print(f"Have: >>{data}<< bytes from {clients[sck]['addr']}")
                            clients[sck]['data'] += data
                            if sck not in outputs:
                                outputs.append(sck)
                        else:
                            if sck in outputs:
                                outputs.remove(sck)
                            inputs.remove(sck)
                            sck.close()
                            del clients[sck]
                    except socket.error as err:
                        if err.errno != errno.EWOULDBLOCK:
                            print(f"Error receiving data: {err}")
                            if sck in outputs:
                                outputs.remove(sck)
                            inputs.remove(sck)
                            sck.close()
                            del clients[sck]

            check_buffer(clients)

            for sck in writable:
                if sck in clients and clients[sck]['result']:
                    print(f"result is: {clients[sck]['result']}")
                    try:
                        answer = f"success: {clients[sck]['result']}".encode()
                        sck.sendall(answer)
                        # sck.sendall(b'success')
                        outputs.remove(sck)
                    except socket.error as err:
                        if err.errno != errno.EWOULDBLOCK:
                            print(f"Error sending data {err}")
                            outputs.remove(sck)
                            inputs.remove(sck)
                            sck.close()
                            del clients[sck]

            for sck in exceptional:
                print(f"Exceptional conditions for {clients[sck]['addr']}")
                inputs.remove(sck)
                if sck in outputs:
                    outputs.remove(sck)
                sck.close()
                del clients[sck]

            time.sleep(0.1)

    finally:
        server_socket.close()


def check_buffer(questions: dict):
    for key, quest in questions.items():
        if quest['result'] is None:
            print(f"CB1: {quest['result'] = }")
            quest['result'] = counter(quest['data'].decode('utf-8'))
        print(f"CB2: {questions = }")


def counter(question: str) -> bytes:
    proc_amt = 4
    num = ''
    if question.startswith('handshake'):
        num = question.split(' ', 1)[1]
        print(f"CNT1: {num}")
    if not num.isdigit():
        return f"success: {question}".encode()

    num = int(question)
    print(f"CNT2: {num}")
    answer: int = multiproc_count(num, proc_amt)
    print(f"CNT3: {answer}")

    return str(answer).encode()


def get_time() -> str:
    t_format = '%y-%m-%d %H:%M:%S.%f'
    return _dt.now().strftime(t_format)


def starter():
    host_addr = '127.0.0.1'
    host_port = 8020
    exit_check()
    listener(host_addr, host_port)


def exit_check() -> bool:
    result = False
    if 'exit.flag' in os.listdir():
        os.remove('exit.flag')
        result = True
    return result


if __name__ == '__main__':
    starter()
