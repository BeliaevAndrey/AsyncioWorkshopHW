import pprint
import socket
from typing import TypeAlias
from datetime import datetime as _dt
from multiprocessing import Process, connection, Array as MPArr
import os
from random import randint, seed

from util import SLogger, multiproc_count

SOCKET: TypeAlias = socket.socket
CHUNK_SIZE = 1024

logger = SLogger('Client', logfile='client.log')


def polling(host_addr: str,
            host_port: int,
            message: str,
            results: MPArr,
            index: int,
            ):
    data_to_send = f'handshake {message}'.encode()
    with socket.socket() as client_socket:
        client_socket.connect((host_addr, host_port))
        client_socket.send(data_to_send)
        answer = client_socket.recv(CHUNK_SIZE).decode('utf-8')
        # time.sleep(1)
        c = answer.split('-> ')[1].strip()
        print(f"{os.getpid() = } {os.getppid() = } {answer = } {c = }")
        if c.isdigit():
            print(f">>{c}<<")
        results[index] = int(c if c.isdigit() else 0)
        print(results[:])
        # answer = client_socket.recv(CHUNK_SIZE).decode('utf-8')
        # if 'success' in answer:
        #     client_socket.send(b'finish')


def checker(questions: list[int], res):
    print("\n\n", "=" * 80)
    progresses = {x: multiproc_count(x, 4) for x in questions}
    for i in questions:
        print(f"{i = }\t{progresses[i] = }")
    print("\n\n", "=" * 40)
    pprint.pp(progresses)
    print(f"{res = }")
    print("\n\n", "=" * 80)


def start(p_amt: int):
    host_addr = '127.0.0.1'
    host_port = 8020
    processes = []
    results = MPArr('Q', [0] * p_amt)

    questions = [randint(1, int(1e9)) for _ in range(p_amt)]
    # for i in range(p_amt):

    for i, num in enumerate(questions):
        print(f"\n{'=' * 80}\n{i} {(num):^80}\n{'=' * 80}\n")
        processes.append(
            Process(target=polling, args=(host_addr, host_port,
                                          str(num), results, i))
        )

        # polling(host_addr, host_port)
    for p in processes:
        p.start()

    for p in processes:
        p.join()

    res = results[:]
    checker(questions, res)


# =============================================================================
if __name__ == '__main__':
    start(3)
