"""Server.py for python echo server."""

import socket
import sys


def server():
    """Place server into listening mode wating for connection."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5011)
    server.bind(address)
    server.listen(1)
    print("Waiting for connection...")
    while True:
        try:
            conn, addr = server.accept()
            if conn:
                buffer_length = 8
                message_complete = False
                while not message_complete:
                    part = conn.recv(buffer_length)
                    print(part.decode('utf8'))
                    if len(part) < buffer_length:
                        break

            message = "Your message has been recieved!"
            conn.sendall(message.encode('utf8'))
        except KeyboardInterrupt:
            server.close()
            sys.exit()
        

if __name__ == '__main__':
    """Run server if run from command line"""
    server()
