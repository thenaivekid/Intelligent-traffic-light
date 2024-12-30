from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import numpy as np
import cv2
from fastapi import HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
# from utils import *
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import time

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

traffic_data = {
    "lights": {"cam1": "green", "cam2": "yellow", "cam3": "red"},
    "num_vehicles": {"cam1": 3, "cam2": 5, "cam3": 7},
}


@app.get("/traffic")
async def get_traffic_data():
    return traffic_data

# @app.post("/vehicles")
# async def detect_vehicles(file: UploadFile):
#     print(file.filename)
#     if file.content_type not in ["image/jpeg", "image/png"]:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid file type. Please upload a JPEG or PNG image.",
#         )
#     print("file")
#     image_data = await file.read()
#     nparr = np.frombuffer(image_data, np.uint8)
#     image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     if image is None:
#         raise HTTPException(status_code=400, detail="Invalid image data")
#     print("valid image received")
#     # Assuming get_detections is defined elsewhere
#     detections = get_detections(image, viz=True)
#     return {"detections": detections}

# @app.get("/count")
# async def count_vehicles():
#     cam1 = "http://192.168.0.111/capture"
#     response = requests.get(cam1)
#     print("captured pic")
#     if response.status_code == 200:
#         img_array = np.array(bytearray(response.content), dtype=np.uint8)


#         frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         # plt.imshow(frame_rgb)
#         # plt.axis("off")
#         # plt.show()
#         # time.sleep(1)  # Add a small delay (1 second) between frames
#         # plt.close()  # Close the previous frame before showing the next
#         image = Image.fromarray(frame_rgb)
#         num_vehicles_cam1 = call https://7648-34-125-249-110.ngrok-free.app/vehicles with image file
#         global traffic_data
#         traffic_data["num_vehicles"]["cam1"] = num_vehicles_cam1
#         return traffic_data
#     else:
#         print("Failed to fetch the image. Status code:", response.status_code)


@app.get("/count")
async def count_vehicles():
    cam1 = "http://192.168.0.111/capture"
    response = requests.get(cam1)

    if response.status_code == 200:
        print("Captured pic")
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)

        # Create a temporary file and save the image
        temp_path = "temp_image.png"
        image.save(temp_path)

        try:
            # Upload the temporary file
            url = "https://9fb5-34-125-249-110.ngrok-free.app/vehicles"
            with open(temp_path, "rb") as img_file:
                files = {"file": ("image.png", img_file, "image/png")}
                vehicle_response = requests.post(url, files=files)

            if vehicle_response.status_code == 200:
                num_vehicles_cam1 = vehicle_response.json().get("num_vehicles", 0)
                traffic_data["num_vehicles"]["cam1"] = num_vehicles_cam1
                return traffic_data
            else:
                return {
                    "error": "Failed to get vehicle count",
                    "status_code": vehicle_response.status_code,
                }
        finally:
            # Clean up the temporary file
            os.unlink(temp_path)

    return {
        "error": "Failed to fetch the image",
        "status_code": response.status_code,
    }
