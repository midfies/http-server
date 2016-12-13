"""Server.py for python echo server."""

import socket
import sys


def server():
    """Place server into listening mode wating for connection."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5030)
    server.bind(address)
    server.listen(5)
    print("Waiting for connection...")
    while True:
        try:
            conn, addr = server.accept()
            if conn:
                return_message = ''
                buffer_length = 8
                message_complete = False
                while not message_complete:
                    part = conn.recv(buffer_length)
                    return_message += part.decode('utf8')
                    if len(part) < buffer_length:
                        break
            if return_message[-3:] == 'EOF':
                return_message = return_message[:-3]
            conn.sendall(return_message.encode('utf8'))
        except KeyboardInterrupt:
            conn.close()
            server.close()
            sys.exit()
        finally:
            conn.close()
        

if __name__ == '__main__':
    """Run server if run from command line"""
    server()
