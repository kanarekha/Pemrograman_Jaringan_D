import sys
import socket

ip = ['192.168.122.30', '192.168.122.119']
num = 1

for i in ip:
  # Create a TCP/IP socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Connect the socket to the port where the server is listening
  server_address = (i, 10000)
  print(f"connecting to {server_address}")
  sock.connect(server_address)


  try:
    # Send image
    image = 'buah.jpg'
    imageFile = open(image, 'rb')
    imageBytes = imageFile.read()
    print(f"sending {image}")
    sock.sendall(imageBytes)
    # Look for the response
    amount_received = 0
    amount_expected = len(imageBytes)
    rcv_image = 'buah_' 'alpine' + str(num) + '.jpg'
    num+=1
    with open(rcv_image, 'wb') as file:
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            if data:
                file.write(data)
            else:
                break
  finally:
    print("closing")
    sock.close()