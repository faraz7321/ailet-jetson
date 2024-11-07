from datetime import datetime
import cv2
import os
import glob
import numpy as np
import time

def get_timestamp():
    # Get the current time
    now = datetime.now()
    
    # Format the timestamp as photo_ddmmyy_hhmmss
    timestamp = now.strftime("%d%m%y_%H%M%S")
    
    return timestamp
def get_visitID():
    # Get the current time
    now = datetime.now()
    
    # Format the timestamp as photo_ddmmyy_hhmmss
    timestamp = now.strftime("faraz%d%m%y")
    
    return timestamp
def capture_image(filename):
    time.sleep(1)
    camera_path = get_camera_path()  # Get the dynamically assigned camera path
    if camera_path is None:
        return  # Exit if the camera is not found
    
    cap = cv2.VideoCapture(camera_path, cv2.CAP_V4L2)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    ret, frame = cap.read()
    if not ret or frame is None:
        print("Error: Failed to capture image.")
        cap.release()
        return None

    # Save the frame
    full_image_path = f"images/{filename}.png"
    os.makedirs('images', exist_ok=True)
    cv2.imwrite(full_image_path, frame)
    blur_face(image_path=full_image_path)
    print(f"Image saved as {filename}.png")

    # Release the webcam
    cap.release()
    return frame

def get_camera_path(camera_name="usb-NOVATEK_Berxel_iHawk100_HK100QB3508P1151-video-index0"):
    # Search for the camera path in /dev/v4l/by-id/
    camera_paths = glob.glob(f"/dev/v4l/by-id/*{camera_name}*")
    
    # Check if any matching path was found
    if camera_paths:
        #print(f"Found camera path: {camera_paths[0]}")
        return camera_paths[0]  # Return the path to the camera
    else:
        print("Error: Camera not found.")
        return None

def remove_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been removed successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' does not exist.")
    except PermissionError:
        print(f"Permission denied: Unable to delete '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while trying to delete the file: {e}")
        
def blur_face(image_path):
    
    prototxt_path = "face-to-blur/weights/deploy.prototxt.txt"
    model_path = "face-to-blur/weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
    #image_path = sys.argv[1]

    output_directory = "images/"
    os.makedirs(output_directory, exist_ok=True)
    image = cv2.imread(image_path)
    filename = os.path.basename(image_path)
    name, extension = os.path.splitext(filename)
    output_image_path = os.path.join(output_directory, f"{name}{extension}")
    
    height, width = image.shape[:2]
    kernel_width = (width // 7) | 1
    kernel_height = (height // 7) | 1
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))
    model.setInput(blob)
    output = np.squeeze(model.forward())

    for i in range(0, output.shape[0]):
        face_accuracy = output[i, 2]
        
        if face_accuracy > 0.4:
            box = output[i, 3:7] * np.array([width, height, width, height])
            start_x, start_y, end_x, end_y = box.astype(np.int64)
            face = image[start_y:end_y, start_x:end_x]
            face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
            image[start_y:end_y, start_x:end_x] = face

    width = 1080
    height = 540

    # cv2.namedWindow("The results", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("The results", width, height)

    # cv2.imshow("The results", image)
    # cv2.waitKey(0)
    cv2.imwrite(output_image_path, image)
