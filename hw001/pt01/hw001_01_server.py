"""Simple socket server with infinite listening"""

import socket

HOST = '127.0.0.1'
PORT = 8020



def server_run():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server is listening on {HOST}:{PORT}")

        while True:
            client_socket, client_address = server_socket.accept()
            try:
                print(f"Connected by {client_address}")
                while True:
                    data = client_socket.recv(512)
                    if not data:
                        break
                    print(f"Received data: {data.decode()}")
                    client_socket.sendall(b'success')

            except ConnectionResetError:
                print(f"Connection reset by {client_address}")
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                print(f"Closing connection to {client_address}")
                client_socket.close()


if __name__ == '__main__':
    server_run()
