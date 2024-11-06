from datetime import datetime
import cv2
import os
import glob

def get_timestamp():
    # Get the current time
    now = datetime.now()
    
    # Format the timestamp as photo_ddmmyy_hhmmss
    timestamp = now.strftime("%d%m%y_%H%M%S")
    
    return timestamp

def capture_image(filename):
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
    os.makedirs('images', exist_ok=True)
    cv2.imwrite(f"images/{filename}.png", frame)
    print(f"Image saved as {filename}")

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