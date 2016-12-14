# -*- coding: utf-8 -*-
"""Server.py for python echo server."""

import socket
import sys


def server():
    """Place server into listening mode wating for connection."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5030)
    server.bind(address)
    server.listen(1)
    print("Waiting for connection...")
    while True:
        try:
            conn, addr = server.accept()
            if conn:
                logged_message = ''
                buffer_length = 8
                message_complete = False
                while not message_complete:
                    part = conn.recv(buffer_length)
                    logged_message += part.decode('utf8')
                    if len(part) < buffer_length:
                        break
            if logged_message[-3:] == 'EOF':
                logged_message = logged_message[:-3]
            print(logged_message)
            response_ok()
        except KeyboardInterrupt:
            break
        except(RuntimeError, SyntaxError, UnicodeError):
            response_error()
        finally:
            if conn:
                conn.close()
    server.close()
    sys.exit()

def response_ok():
    pass

def response_error():
    pass
        

if __name__ == '__main__':
    """Run server if run from command line"""
    server()
