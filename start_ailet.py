import time
from ailet_api import *
from utils import *

token = auth_login("efrobotics.poc", "efrobotics1")
camera_name="usb-NOVATEK_Berxel_iHawk100_HK100QB3508P1151"

while(True):
    imagename = get_timestamp() 
    capture_image(filename=imagename)
    post_photo(token=token, photo_id=imagename)
    remove_file(f"images/{imagename}.png")
    time.sleep(5)