import socket
import re
import argparse
from time import sleep

HOST = '127.0.0.1'
PORT = 8020


def ping_out(host=HOST, port=PORT):
    print(f'{host} {port}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        try:
            client_socket.connect((host, port))
            print(f"Connected to {host}:{port}")

            message = ""
            while message != "STOP":
                message = input("Input message: ")
                client_socket.sendall(message.encode('utf-8'))
                print(f"Sent: {message}")

                response = client_socket.recv(1024)
                print(f"Received: {response.decode('utf-8')}")
            else:
                return 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return 1


if __name__ == '__main__':

    flag = -1
    address = "192.168.20.144"
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.(\d){1,3}$", address):
        print('WRONG')
        exit(1)
    else:
        print(address)

    while flag == -1:
        flag = ping_out()
