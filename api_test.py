import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import numpy as np
import base64
import cv2

#import face_enhancement

# uvicorn api_test:app --reload

app = FastAPI()

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

def improve_image(orig_image):
    #faceenhancer = face_enhancement.FaceEnhancement(size=512, model="GPEN-BFR-512", use_sr="store_true", sr_model="rrdb_realesrnet_psnr", channel_multiplier=2, narrow=1, device='cuda')
    #np_img = np.array(orig_image)
    #generated = faceenhancer.process(np_img)

    return orig_image

@app.post("/base64file")
async def use_base64file(data: dict=None):
    image = data['base64_file'].encode('utf-8')

    decoded_image = decode_base64_to_np(image)

    result = improve_image(decoded_image)

    processed_image = encode_np_to_base64(result)

    return JSONResponse({
        "result_file": processed_image
    })
