import socket
from typing import TypeAlias
from datetime import datetime as _dt
from multiprocessing import Process, connection
import os
import time


from util import SLogger

SOCKET: TypeAlias = socket.socket
CHUNK_SIZE = 1024

logger = SLogger('Client', logfile='client.log')


def polling(host_addr: str, host_port: int):
    data_to_send = f'handshake {os.getpid()}'.encode()
    with socket.socket() as client_socket:
        client_socket.connect((host_addr, host_port))
        client_socket.send(data_to_send)
        answer = client_socket.recv(CHUNK_SIZE).decode('utf-8')
        time.sleep(1)
        logger.log(answer)
        # answer = client_socket.recv(CHUNK_SIZE).decode('utf-8')
        if 'success' in answer:
            client_socket.send(b'finish')


def start(p_amt: int):
    host_addr = '127.0.0.1'
    host_port = 8020
    processes = []
    for i in range(p_amt):
        print(f"\n{'='* 80}\n{i + 1:^80}\n{'=' * 80}\n")
        processes.append(
            Process(target=polling, args=(host_addr, host_port))
        )
        # polling(host_addr, host_port)
    for p in processes:
        p.start()

    for p in processes:
        p.join()


# =============================================================================
if __name__ == '__main__':
    start(1)
