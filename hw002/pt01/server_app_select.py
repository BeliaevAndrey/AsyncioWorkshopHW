import socket
import select
import time
import errno

from datetime import datetime as _dt
from typing import TypeAlias
import traceback

from util import SLogger

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
            # The optional 4th argument specifies a timeout in seconds;

            for sck in readable:
                if sck is server_socket:
                    client_sock, addr = server_socket.accept()
                    print(f"Connection: {addr}")
                    client_sock.setblocking(False)
                    inputs.append(client_sock)
                    clients[client_sock] = {'addr': addr, 'data': b''}
                else:
                    try:
                        data = sck.recv(CHUNK_SIZE)
                        if data:
                            print(f"Have: {data} bytes from {clients[sck]['addr']}")
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

            for sck in writable:
                if sck in clients and clients[sck]['data']:
                    try:
                        sck.sendall(b'success')
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


def get_time() -> str:
    t_format = '%y-%m-%d %H:%M:%S.%f'
    return _dt.now().strftime(t_format)


def starter():
    host_addr = '127.0.0.1'
    host_port = 8020
    listener(host_addr, host_port)


if __name__ == '__main__':
    starter()
