import requests
import utils
import time

AILET_BASE_URL = 'https://poc.intrtl.com/api/v2/'

def auth_login(user, pwd):
    url = AILET_BASE_URL + 'auth/login'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        'login': user,
        'password': pwd
    }

    try:
        # Make a POST request to the login endpoint
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        # Parse the response as JSON
        response_json = response.json()

        # Extract the token from the response
        token = response_json.get('token')

        if token:
            return token
        else:
            print("Login failed: No token received.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    return None


# Function to post a photo
def post_photo(token, photo_id):
    time.sleep(1)
    url = AILET_BASE_URL + "photos/"
    visit_id = "faraz-test"
    scene_id = "1"
    external_store_id = "10001"
    photo_file_path = f"./images/{photo_id}.png"
    files = {
        'photo_data': open(photo_file_path, 'rb')
    }
    data = {
        'visit_id': utils.get_visitID(),
        'photo_id': photo_id,
        'scene_id': scene_id,
        'external_store_id': external_store_id
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(url, files=files, data=data, headers=headers)
    #print("post_photo:", response.text)
    print(f"Uploaded image: {photo_id}")
    return response.json()
