"""
Вам поставили задачу: реализовать сервер, который будет принимать в запросе
от клиентов целое число в диапазоне от 1 до 1_000_000_000 и возвращать сумму
всех чисел этого диапазона. Реализуйте подобный сервер любым удобным для вас
способом, но помните, что клиентов может быть существенно больше одного и
они очень не хотят долго ждать ответа.
"""
import socket
import time
from datetime import datetime as _dt
from typing import TypeAlias
import errno
import traceback

from util import SLogger

SOCKET: TypeAlias = socket.socket
CHUNK_SIZE = 1024

logger = SLogger('Server')


def listener(host_addr: str, host_port: int):
    connections = []
    conn_remove = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host_addr, host_port))
    server_socket.listen(1024)
    server_socket.setblocking(False)  # set non-blocking mode

    logger.log(f'Listening at {host_addr}:{host_port}')

    count = 0

    try:
        while True:
            try:
                connect, client_address = server_socket.accept()
                print(f"connect: {client_address}")
                connect.setblocking(False)
                connections.append((connect, client_address))
                time.sleep(0.3)

            except socket.error as exc:
                # logger.log_exc(exc)
                if exc.errno != errno.EWOULDBLOCK:
                    print(f"\033[34mSOCKET.ERROR: {exc = }")
                    logger.log_exc(exc)
                    break

            # print(f'{len(connections) = }')
            for conn, address in connections.copy():

                print(f'{address=}')
                try:
                    count += 1
                    if count > 200:
                        break
                    data = conn.recv(CHUNK_SIZE)
                    if data.startswith(b'handshake'):
                        logger.log(f"{get_time()} {data.decode('utf-8')}")

                    print(f'{get_time()} :: {data.decode()}')
                    response = f'{get_time()}, success: {data.decode().upper()}'.encode()
                    conn.send(response)
                    # data = conn.recv(CHUNK_SIZE)
                    logger.log(data)
                except socket.error as exc1:
                    if exc1.errno != errno.EWOULDBLOCK:
                        traceback.print_tb(exc1.__traceback__)
                        conn_remove.append(conn)
                        break

            while connections:
                conn, addr = connections.pop()
                print()
                print(f'CLOSING: {conn}')
                conn.close()

            # time.sleep(0.3)


    finally:
        server_socket.close()


def sender(connect: SOCKET, data: bytes) -> bool:
    pass


def receiver(connect: SOCKET) -> bytes:
    pass


def counter(num: int):
    pass


def get_time() -> str:
    t_format = '%y-%m-%d %H:%M:%S.%f'
    return _dt.now().strftime(t_format)


def starter():
    host_addr = '127.0.0.1'
    host_port = 8020
    listener(host_addr, host_port)


if __name__ == '__main__':
    starter()
