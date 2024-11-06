from utils import *
import requests
from collections import namedtuple

ROBOT_BASE_URL = "192.168.178.182:8090"

MoveAction = namedtuple("MoveAction", ["type", "x", "y", "z"])
    
def get_pois():
    url = "192.168.12.1:8090" #rest api
    # get json
    # parse
    # get overlays
    # data fill with x,y coordinates.
    # 
    pass

def move_to_poi():
    #get overlays
    #get poi
    #send robot to overlay -> x, y
    pass

def create_move_action(action_params: MoveAction, auth_token=None):
    url = f"{ROBOT_BASE_URL}/moves/create"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "action_type": action_params.type,
        "coordinates": {"x": action_params.x, "y": action_params.y, "z": action_params.z},
    }
 

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()  # Returns JSON response on success
    else:
        response.raise_for_status()  # Raises error for unsuccessful requests

