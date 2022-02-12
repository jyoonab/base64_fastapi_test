import requests
import numpy as np
import json
import base64
from matplotlib.pyplot import imread
from skimage.transform import resize
from datetime import datetime
from PIL import Image
import io
import cv2


def encode_np_to_base64(input: np.ndarray) -> str:
    input_bytes = cv2.imencode('.jpg', input)[1].tobytes()
    input_base64 = base64.b64encode(input_bytes)
    input_base64 = input_base64.decode('utf-8')
    return input_base64

def decode_base64_to_np(input: str) -> np.ndarray:
    decoded = base64.b64decode(input)
    nparr = np.frombuffer(decoded, np.uint8)
    image_result = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image_result

'''
Encode Image to Base64,
np.ndarray -> str'''
path_to_img = r"./imgs/1.jpg"
image = imread(path_to_img)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
base64_str = encode_np_to_base64(image)

'''send Base64 str to fastapi server'''
base64_request = { "base64_file": base64_str }
response = requests.post(url='http://127.0.0.1:8000/base64file', data=json.dumps(base64_request))

'''Decode Base64 to make np.ndarray'''
result_image = response.json()["result_file"]
image_result = decode_base64_to_np(result_image)

cv2.imshow('frame', image_result)
cv2.waitKey(0)
