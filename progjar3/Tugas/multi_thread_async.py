from library import download_broadcast_gambar,get_url_list
import time
import datetime
import concurrent.futures

TARGET_IP = '192.168.122.0'
TARGET_PORT = 5005

def download_broadcast_semua():
    texec = dict()
    urls = get_url_list()
    status_task = dict()
    task = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    catat_awal = datetime.datetime.now()

    for k in urls:
        print(f"mendownload dan broadcast file {urls[k]}")
        waktu = time.time()
        args = (urls[k], True, TARGET_IP, TARGET_PORT)
        #bagian ini merupakan bagian yang mengistruksikan eksekusi fungsi download gambar secara multithread
        texec[k] = task.submit(lambda p: download_broadcast_gambar(*p), args)

    #setelah menyelesaikan tugasnya, dikembalikan ke main thread dengan memanggil result
    for k in urls:
        status_task[k]=texec[k].result()

    catat_akhir = datetime.datetime.now()
    selesai = catat_akhir - catat_awal
    print(f"Waktu TOTAL yang dibutuhkan {selesai} detik {catat_awal} s/d {catat_akhir}")
    print("hasil task yang dijalankan")
    print(status_task)


#fungsi download_gambar akan dijalankan secara multithreading

if __name__=='__main__':
    download_broadcast_semua()