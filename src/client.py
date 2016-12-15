# -*- coding: utf-8 -*-
"""Client.py for python echo server."""
import socket
import sys


def client(message):
    """Client side of the http-echo-server."""
    if sys.version_info[0] == 2:
        msg = message.decode("utf8")
        msg = msg.encode("utf8")
    else:
        msg = message.encode("utf8")

    destination_info = socket.getaddrinfo("127.0.0.1", 5006)
    stream_info = [i for i in destination_info if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])

    try:
        client.connect(stream_info[-1])
    except:
        raise ValueError("Connection not available.")

    print('CONNECTED!')
    buffer_length = 8
    if len(msg) % buffer_length == 0:
        msg += b'EOF'
    client.sendall(msg)
    return_message = ''
    message_complete = False
    while not message_complete:
        part = client.recv(buffer_length)
        return_message += part.decode('utf8')
        if len(part) < buffer_length:
            break
    if return_message[-3:] == 'EOF':
        return_message = return_message[:-3]
    client.close()
    print(return_message)
    return return_message


if __name__ == "__main__":
    client(sys.argv[1])
