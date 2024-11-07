import time
from ailet_api import *
from utils import *
import threading
import queue
import os

token = auth_login("efrobotics.poc", "efrobotics1")
camera_name="usb-NOVATEK_Berxel_iHawk100_HK100QB3508P1151"

upload_queue = queue.Queue()

def main_loop():
    # Start the background upload thread
    upload_thread = threading.Thread(target=background_upload, args=(token,))
    upload_thread.start()

    try:
        while True:
            imagename = get_timestamp()
            capture_image(filename=imagename)
            time.sleep(2)
            # Add the image to the queue for background upload
            upload_queue.put(imagename)
    except KeyboardInterrupt:
        print("Stopping capture process.")
    finally:
        # Signal the upload thread to stop
        upload_queue.put(None)
        upload_thread.join()

def background_upload(token):
    while True:
        # Wait for an image to be available in the queue
        photo_id = upload_queue.get()
        if photo_id is None:
            break
        post_photo(token=token, photo_id=photo_id)
        remove_file(f"images/{photo_id}.png")
        upload_queue.task_done()
        
main_loop()