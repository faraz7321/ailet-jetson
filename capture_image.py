import cv2
import utils
def capture_image(filename):
    
    campath = "/dev/v4l/by-id/usb-Creality_3D_Technology_CREALITY_CAM_00000000-video-index0"
    cap = cv2.VideoCapture(campath)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()

    if ret:
        cv2.imwrite(f"images/{filename}", frame)
        print(f"Image saved as {filename}")
    else:
        print("Error: Failed to capture image.")

    # Release the webcam
    cap.release()

capture_image("hjewd.png")