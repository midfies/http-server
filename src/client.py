"""Client.py for python echo server."""
import socket

destination_info = socket.getaddrinfo("127.0.0.1", 5000)
stream_info = [i for i in destination_info if i[1] == socket.SOCK_STREAM][0]
client = socket.socket(*stream_info[:3])

if client.connect(stream_info[-1]):
    return 'CONNECTED!'

# message = ''
# buff = 8

# if len(client.recv(buff)) > 8:
#     message += client.recv(buff)
# else:
#     message = client.recv(buff)

# print(message.encode("utf-8"))

# client.sendall(message.encode("utf-8"))
