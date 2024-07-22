"""Simple socket server with infinite listening"""

import socket

HOST = '127.0.0.1'
PORT = 8020


def server_run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        # server_socket.setblocking(False)
        server_socket.listen()
        print(f"Server is listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            # client_socket.setblocking(False)
            try:
                print(f"Connected by {client_address}")
                while True:
                    data = client_socket.recv(512)

                    if data == b'\xff\xf4\xff\xfd\x06':     # in case of telnet
                        break   # socket is closed in block finally

                    if not data:
                        break

                    print(f"Received data: {data.decode()}")
                    echo = f"echo: {data.decode('utf-8')}\t"
                    client_socket.sendall(echo.encode())
                    client_socket.sendall(b'success\n')

            except ConnectionResetError:
                print(f"Connection reset by {client_address}")
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                print(f"Closing connection to {client_address}")
                client_socket.close()


if __name__ == '__main__':
    server_run()
