from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import Optional
import numpy as np
import cv2
from fastapi import HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import time
import asyncio
from contextlib import asynccontextmanager
from utils import *

# Global variable for background task
background_tasks = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create background task
    task = asyncio.create_task(update_vehicle_count())
    background_tasks.add(task)
    yield
    # Shutdown: Cancel background task
    for task in background_tasks:
        task.cancel()


app = FastAPI(lifespan=lifespan)

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


async def update_vehicle_count():
    while True:
        try:
            cam1 = "http://192.168.0.128/capture"
            response = requests.get(cam1)

            if response.status_code == 200:
                print("Captured pic")
                img_array = np.array(bytearray(response.content), dtype=np.uint8)
                frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_rgb)

                # Create a temporary file and save the image
                # temp_path = "temp_image.png"
                # image.save(temp_path)

                try:
                    # Upload the temporary file
                    #     url = "https://9fb5-34-125-249-110.ngrok-free.app/vehicles"
                    #     with open(temp_path, "rb") as img_file:
                    #         files = {"file": ("image.png", img_file, "image/png")}
                    #         vehicle_response = requests.post(url, files=files)

                    #     if vehicle_response.status_code == 200:
                    #         num_vehicles_cam1 = vehicle_response.json().get(
                    #             "num_vehicles", 0
                    #         )
                    #         traffic_data["num_vehicles"]["cam1"] = num_vehicles_cam1
                    #     else:
                    #         print("Failed to get vehicle count")
                    # finally:
                    #     # Clean up the temporary file
                    #     if os.path.exists(temp_path):
                    #         os.unlink(temp_path)

                    num_vehicles = get_detections(image, viz=True)
                    global traffic_data
                    traffic_data["num_vehicles"]["cam1"] = num_vehicles
                    print(num_vehicles, "in cam 1")
                except:
                    print("could not count")
            else:
                print("Failed to fetch the image")

            await asyncio.sleep(5)  # Using asyncio.sleep instead of time.sleep
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in update_vehicle_count: {e}")
            await asyncio.sleep(5)  # Wait before retrying


@app.get("/traffic")
async def get_traffic_data():
    return traffic_data
