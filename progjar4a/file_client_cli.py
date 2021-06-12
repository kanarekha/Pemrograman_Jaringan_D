import socket
import json
import base64
import logging
import threading
import time
import datetime

server_address=('0.0.0.0',6666)

def send_command(command_str="", count=None):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        hasil = json.loads(data_received)
        logging.warning(f"{count} - data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename="", count=None):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        #proses file dalam bentuk base64 ke bentuk bytes
        namafile= hasil['data_namafile'] + " " + str(count)
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False

def get_image(filename="",count=""):
    texec =dict()
    waktu_mulai = datetime.datetime.now()
    for k in range(count):
        print(" iterasi- ", k, "download", filename)
        waktu = time.time()
        texec[k] = threading.Thread(target=remote_get, args=(filename,k))
        texec[k].start()

    for k in range(count):
        texec[k].join()

    waktu_akhir = datetime.datetime.now()
    durasi = waktu_akhir - waktu_mulai
    print(f"Waktu yang dibutuhkan {durasi} detik")



if __name__=='__main__':
    server_address=('0.0.0.0',6666)
    #remote_list()
    get_image('donalbebek.jpg', 100)

