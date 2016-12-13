"""Client.py for python echo server."""
import socket
import sys


def client(message):
    """Client side of the http-echo-server."""
    destination_info = socket.getaddrinfo("127.0.0.1", 5006)
    stream_info = [i for i in destination_info if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])

    try:
        client.connect(stream_info[-1])
    except:
        raise ValueError("Connection not available.")

    print('CONNECTED!')
    client.sendall(message.encode("utf-8"))
    return_message = ''

    buffer_length = 8
    message_complete = False
    while not message_complete:
        part = client.recv(buffer_length)
        return_message += part.decode('utf8')
        if len(part) < buffer_length:
            break
    client.close()
    print(return_message)


if __name__ == "__main__":
    client(sys.argv[1])
