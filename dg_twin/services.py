import requests
import base64
from django.conf import settings
import os
import time
import shutil

def upload_to_imgbb(image_path):
    """
    Upload image to ImgBB and return the URL
    """
    api_key = settings.IMGBB_API_KEY
    url = "https://api.imgbb.com/1/upload"
    
    try:
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            data = {'key': api_key}
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
            result = response.json()
            return result['data']['url']
    except Exception as e:
        print(f"Error uploading to ImgBB: {str(e)}")
        return None

def generate_avatar(image_path):
    """
    Generate avatar using D-ID API
    """
    api_key = settings.DID_API_KEY
    url = "https://api.d-id.com/talks"
    
    try:
        # Upload image to ImgBB first
        image_url = upload_to_imgbb(image_path)
        if not image_url:
            raise Exception("Failed to upload image to ImgBB")
        
        print(image_url)
        
        payload = {
            "source_url": image_url,
            "script": {
                "type": "text",
                "subtitles": "false",
                "provider": {
                    "type": "microsoft",
                    "voice_id": "Sara"
                },
                "input": "David is the best name ever. Even Aaron is not as good as David is",
                "ssml": "false"
            },
            "config": { "fluent": "false" }
        }

        auth_string = f"{api_key}:"
        base64_auth_string = base64.b64encode(auth_string.encode()).decode()

        headers = {
            "accept": "application/json",
            "content-Type": "application/json",
            "authorization": f"Basic {api_key}"
        }

        response = requests.post(url, headers=headers, json=payload)
        # response.raise_for_status()
        print(response.status_code)
        result = response.json()
        

        headers_get = {
            "accept": "application/json",
            "authorization": f"Basic {base64_auth_string}"
        }
        id_url = result['id']
        url_get = url+f"/{id_url}"
        response_get = requests.get(url_get, headers=headers_get).json()
        result_url = response_get['result_url']
        return result_url
        
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response content: {response.content}")
        return None
    except Exception as e:
        print(f"Error generating avatar: {str(e)}")
        return None