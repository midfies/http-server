# -*- coding: utf-8 -*-
"""
Server.py for python server.

server() - Basic server which once activated continuosly listens for client until keyboard interupt is given.

response_ok() - Returns a generic 200 status code response.

response_error() - Returns a specific 500 status code response depending on the issues with the header.

parse_request() - Splits header into parts and send header to response_ok() or response_error() depending on the validity of the header.  The response from those methods are then returned.
"""

import socket
import sys
import os


def server():
    """Place server into listening mode wating for connection."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5006)
    server.bind(address)
    server.listen(1)
    while True:
        print("Waiting for connection...")
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
            response = parse_request(logged_message)
            if len(response) % buffer_length == 0:
                response += 'EOF'
            conn.sendall(response.encode('utf8'))
        except KeyboardInterrupt:
            break
        except(TypeError, SyntaxError):
            response_error()
            print("DANGER INTERNAL SERVER ERROR!! OVERLOAD OVERLOAD")
        finally:
            if conn:
                conn.close()
    print('Closing Connection with client...')
    conn.close()
    print('Closing Server...')
    server.close()
    print('Thanks for visiting!')
    sys.exit()


def response_ok():
    """Send a 200 response."""
    return "HTTP/1.1 200 OK\r\nContent-Type: text/plain \r\n\r\nThanks for connecting, friend."


def response_error(error):
    """Build a 500 Server Error,define the error and return error message."""
    err_msg = 'HTTP/1.1 500 Internal Server Error\r\n'
    if len(error) < 3:
        err_msg += 'HTTP Request requires 3 Method, URI, and Protocol.\r\n'
    elif len(error) > 3:
        err_msg += 'Unknown arguements passed with request.\r\n'
    else:
        if error[0] != 'GET':
            err_msg += 'This server only accepts GET requests\r\n'
        if error[2] != 'HTTP/1.1':
            err_msg += 'Client must use HTTP/1.1\r\n'
    err_msg += '\r\n'
    return err_msg


def parse_request(request):
    """Split Header from request and send header to response_ok or response_error depending on validity. Return message returned from those methods."""
    header = request.split('\r\n')
    split_header = header[0].split()
    if len(split_header) != 3:
        response = response_error(split_header)
    elif split_header[0] != 'GET' or split_header[2] != 'HTTP/1.1':
        response = response_error(split_header)
    else:
        response = response_ok()
    return response


def resolve_uri(uri):
    """Resolve the uri."""
    root = 'webroot/'
    files_in_directory = os.listdir(root)
    uri_split = uri.split('/')
    if len(uri_split) > 1:
        if uri_split[0] in files_in_directory:
            if uri_split[1] in os.listdir(root + uri_split[0]):
                return 'Found in sub directory'
            else:
                return 'File not found in sub directory.'
        else:
            return 'Folder not found in root directory.'
    elif uri in files_in_directory:
            return 'Found in root.'
    else:
        return 'File not found'



if __name__ == '__main__':
    """Run server if run from command line"""
    server()
