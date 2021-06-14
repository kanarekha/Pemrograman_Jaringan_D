import logging
import requests
import os
import time
import datetime
import socket


def get_url_list():
    urls = dict()
    urls['kompas']='https://asset.kompas.com/crops/qz_jJxyaZgGgboomdCEXsfbSpec=/0x0:998x665/740x500/data/photo/2020/03/01/5e5b52f4db896.jpg'
    urls['its']='https://www.its.ac.id/wp-content/uploads/2017/10/logo-its-1.png'
    urls['kucing']='https://cdn.idntimes.com/content-images/post/20200303/1-17b763f032b2396d91d33582a4707d79.jpg'
    return urls


def download_broadcast_gambar(url=None,tuliskefile=False, target_ip=None, target_port=None):
    waktu_awal = datetime.datetime.now()
    if (url is None):
        return False
    ff = requests.get(url)

    # tipe = dict()
    # tipe['image/png']='png'
    # tipe['image/jpg']='jpg'
    # tipe['image/gif']='gif'
    # tipe['image/jpeg']='jpg'
    # tipe['application/zip']='jpg'
    # tipe['video/quicktime']='mov'

    time.sleep(2) #untuk simulasi, diberi tambahan delay 2 detik

    #download file
    filename = os.path.basename(url)
    if (tuliskefile):
        fp = open(f"{filename}", "wb")
        fp.write(ff.content)
        fp.close()

    # broadcast file
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print(f"broadcast file {filename}")
    img_file = open(f"{filename}", "rb")
    img_bytes = img_file.read()
    sock.sendto(img_bytes, (target_ip, target_port))

    waktu_process = datetime.datetime.now() - waktu_awal
    waktu_akhir = datetime.datetime.now()
    logging.warning(f"Waktu untuk download dan broadcast file {filename} dalam waktu {waktu_process} -> {waktu_awal} s/d {waktu_akhir}")
    return waktu_process


