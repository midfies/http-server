# -*- coding: utf-8 -*-
"""
Server.py for python server.

server() - Basic server which once activated continuosly listens for client until keyboard interupt is given.

response_ok() - Returns a generic 200 status code response.

response_error() - Returns a specific 500 status code response depending on the issues with the header.

parse_request() - Splits header into parts and send header to response_ok() or response_error() depending on the validity of the header.  The response from those methods are then returned.
"""

import sys
import os
import io
import mimetypes


MEDIA_TYPES = [
    'image/jpeg',
    'image/png',
    'audio/mpeg',
    'audio/ogg',
    'video/mp4',
]


def server(socket, address):
    """Place server into listening mode wating for connection."""
    while True:
        print("Waiting for connection...")
        try:
            if socket:
                logged_message = ''
                buffer_length = 8
                message_complete = False
                while not message_complete:
                    part = socket.recv(buffer_length)
                    logged_message += part.decode('utf8')
                    if len(part) < buffer_length:
                        break
            if logged_message[-3:] == 'EOF':
                logged_message = logged_message[:-3]
            print(logged_message)
            header_lines = logged_message.split('\r\n')
            split_header = header_lines[0].split()
            if parse_request(split_header):
                response = resolve_uri(split_header[1])

            else:
                response = response_error(split_header)
            if len(response) % buffer_length == 0:
                response += 'EOF'
            print('Response:', response)
            socket.sendall(response.encode('utf8'))
        except KeyboardInterrupt:
            break
        except(TypeError, SyntaxError):
            print("DANGER INTERNAL SERVER ERROR!! OVERLOAD OVERLOAD")
        finally:
            if socket:
                socket.close()
    print('Closing Connection with client...')
    socket.close()
    print('Closing Server...')
    server.close()
    print('Thanks for visiting!')
    sys.exit()


def response_ok(type):
    """Send a 200 response."""
    return "HTTP/1.1 200 OK Content-Type:" + type + '\r\n\r\n'


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


def parse_request(header, ):
    """Return True if valid header."""
    print('In Parse Request...')
    if len(header) != 3:
        return False
    elif header[0] != 'GET' or header[2] != 'HTTP/1.1':
        return False
    return True


def resolve_uri(uri):
    """Resolve the uri."""
    root = 'webroot/'
    print("file is", search_directory(root + uri))
    retrieved_file = search_directory(root + uri)
    file_type = mimetypes.guess_type(uri)[0]
    print('File Type is: ', file_type)
    try:
        if os.path.exists(retrieved_file):
            if file_type in MEDIA_TYPES:
                f = io.open(retrieved_file, 'rb')
                response = response_ok(file_type) + str(f.read())
                f.close()
            elif file_type == 'text/plain':
                response = response_ok(file_type)
                f = io.open(retrieved_file)
                response += f.read().replace("\n", " ")
                f.close()
            elif os.path.isdir(root + uri):
                response = response_ok('directory') + prepare_directory(root + uri)
        else:
            response = response_file_not_found(uri)
    except IOError():
        return response_file_not_found(uri)
    return response


def prepare_directory(folder):
    """Create a html doc with an unordered list of files in directory."""
    listing = os.listdir(folder)
    response = '<!DOCTYPE html><html><head><title>' + folder + '</title></head><body><ul>'
    for file in listing:
        response += '<li>' + file + '</li>'
    response += '</ul></body></html>'
    return response


def search_directory(uri):                         
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), uri)


if __name__ == '__main__':
    """Run server if run from command line"""
    server()
