import sys
import socket

ip = ['192.168.122.223', '192.168.122.204']

for i in ip:

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = (i, 10000)
    print(f"connecting to {server_address}")
    sock.connect(server_address)


    try:
        # Send data
        message = ''.join(random.choices(string.ascii_letters, k = 2000000))
        print(f"sending {message}")
        sock.sendall(message.encode())
        # Look for the response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print(f"{data}")
    finally:
        print("closing")
        sock.close()