import socket
import re
import argparse
from datetime import datetime as dt

HOST = '127.0.0.1'
PORT = 8020


def ping_out(host=HOST, port=PORT):
    def read_and_send_msg():
        while (msg := input("Input message: ")) != "STOP":
            time_now = (dt.now().strftime('%Y-%m-%d %H:%M:%S'))
            msg = f':< {time_now} >: {msg}'
            client_socket.sendall(msg.encode('utf-8'))
            print(f"Sent: {msg}")
            response = client_socket.recv(1024)
            print(f"Received: {response.decode('utf-8')}")

    print(f'{host} {port}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            print(f"Connected to {host}:{port}")

            message = "handshake"
            client_socket.sendall(message.encode('utf-8'))
            print(client_socket.recv(16).decode('utf-8'))

            read_and_send_msg()

            return 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return 1
        finally:
            client_socket.close()


def starter():
    parser = argparse.ArgumentParser(description="Client-server simple pair. Client part")
    parser.add_argument('-p', type=int, dest='port', default=8020,
                        help='A number of port to poll (8020 by default)')
    parser.add_argument('-a', type=str, dest='address', default='127.0.0.1',
                        help='Address of server part. (127.0.0.1 by default)')

    args = parser.parse_args()
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.(\d){1,3}$", args.address):
        print("Wrong parameter: a -- must be an IPv4 address strictly.")
        exit(1)
    print(f'host address: {args.port}, port: {args.address}')

    flag = -1
    while flag == -1:
        flag = ping_out(args.address, args.port)
    else:
        print("Exiting...")


if __name__ == '__main__':
    starter()
