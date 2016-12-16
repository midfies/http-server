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
import io

IMAGES = ['jpg', 'jpeg', 'png']


def server():
    """Place server into listening mode wating for connection."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5020)
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


def response_ok(type):
    """Send a 200 response."""
    return "HTTP/1.1 200 OK Content-Type:" + type + ' '


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


def response_file_not_found(error):
    """Build a 404 File Not Found error message."""
    return 'HTTP/1.1 404 File Not Found\r\n' + error + ' is not in directory.\r\n\r\n'


def parse_request(request):
    """Split Header from request and send header to response_ok or response_error depending on validity. Return message returned from those methods."""
    header = request.split('\r\n')
    split_header = header[0].split()
    if len(split_header) != 3:
        response = response_error(split_header)
    elif split_header[0] != 'GET' or split_header[2] != 'HTTP/1.1':
        response = response_error(split_header)
    else:
        response = resolve_uri(split_header[1])
    return response


def resolve_uri(uri):
    """Resolve the uri."""
    root = 'webroot/'
    files_in_directory = os.listdir(root)
    uri_split = uri.split('/')
    if len(uri_split) > 1:
        if uri_split[0] in files_in_directory:
            if uri_split[1] in os.listdir(root + uri_split[0]):
                if uri_split[1].split('.')[-1] in IMAGES:
                    f = io.open(root + uri, 'rb')
                    response = response_ok('image/' + uri_split[1].split('.')[-1]) + str(f.read())
                else:
                    response = response_ok('text/plain')
                    f = io.open(root + uri)
                    response += f.read().replace("\n", " ")
                f.close()
                return response
            else:
                return response_file_not_found(uri)
        else:
            return response_file_not_found(uri)
    elif uri in files_in_directory:
            if "." in uri:
                if uri.split('.')[-1] in IMAGES:
                    f = io.open(root + uri, 'rb')
                    response = response_ok('image/' + uri.split('.')[-1]) + str(f.read())
                else:
                    response = response_ok('text/plain')
                    f = io.open(root + uri)
                    response += f.read().replace("\n", " ")
                f.close()
                return response
            else:
                response = prepare_directory(root + uri)
                return response
    else:
        return response_file_not_found(uri)


def prepare_directory(folder):
    """Create a html doc with an unordered list of files in directory."""
    listing = os.listdir(folder)
    response = '<!DOCTYPE html><html><head><title>' + folder + '</title></head><body><ul>'
    for file in listing:
        response += '<li>' + file + '</li>'
    response += '</ul></body></html>'
    return response


if __name__ == '__main__':
    """Run server if run from command line"""
    server()
