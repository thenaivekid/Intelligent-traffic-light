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
import aiohttp
from contextlib import asynccontextmanager
from utils import *

cam1 = "http://192.168.137.203"
cam2 = "http://192.168.137.191"
# cam3 = "http://192.168.137.22"

# Global variable for background task

traffic_data = {
    "num_vehicles": {"cam1": 3, "cam2": 5, 
                    #  "cam3": 7
                     },
    "green_duration": {"cam1": 14, "cam2": 9, 
                    #    "cam3": 4
                       },
    "camera_urls": {"cam1": cam1, "cam2": cam2,
                    # "cam3": cam3
                    },
}


background_tasks = set()

total_cycle_time = 30


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(update_vehicle_count())
    task1 = asyncio.create_task(update_ligth())
    background_tasks.add(task)
    background_tasks.add(task1)
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


def allocate_durations(traffic_data, total_time):
    total_vehicles = sum(traffic_data["num_vehicles"].values())
    durations = {}
    for lane, vehicles in traffic_data["num_vehicles"].items():
        durations[lane] = int((vehicles / total_vehicles) * total_time)
    return durations


async def update_vehicle_count():
    global traffic_data
    while True:
        try:
            images = []
            for cam in traffic_data["camera_urls"]:
                print(f"{traffic_data['camera_urls'][cam]}/capture")
                response = requests.get(f"{traffic_data['camera_urls'][cam]}/capture")


                if response.status_code == 200:
                    print(f"Captured pic {cam}")
                    img_array = np.array(bytearray(response.content), dtype=np.uint8)
                    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(frame_rgb)
                    images.append(image)
                else:
                    print("Failed to fetch the image")

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

                num_vehicles = get_detections_batch(images, viz=False)
                # print(num_vehicles, "main")
                # global traffic_datas``
                try:
                    for i, cam in enumerate(traffic_data["num_vehicles"]):
                        traffic_data["num_vehicles"][cam] = num_vehicles[i]
                except IndexError as e:
                    print(f"IndexError: {e}")
                    print(f"num_vehicles: {num_vehicles}")
                    print(f"traffic_data['num_vehicles']: {traffic_data['num_vehicles']}")
                except Exception as e:
                    print(f"Unexpected error: {e}")

            except:
                print("could not count")

            await asyncio.sleep(5)  # Using asyncio.sleep instead of time.sleep
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Error in update_vehicle_count: {e}")
            await asyncio.sleep(5)  # Wait before retrying


async def update_ligth():
    global traffic_data
    while True:
        traffic_data_copy = traffic_data.copy()
        async with aiohttp.ClientSession() as session:
            for cam in traffic_data_copy["num_vehicles"]:
                camera_url = traffic_data_copy["camera_urls"][cam]

                # Turn the current camera light GREEN
                await session.get(f"{camera_url}:85/GREEN")
                print(f"{cam}: GREEN light ON")

                # Turn other cameras' lights RED
                for other_cam in traffic_data_copy["camera_urls"]:
                    if other_cam != cam:
                        other_camera_url = traffic_data_copy["camera_urls"][other_cam]
                        await session.get(f"{other_camera_url}:85/RED")
                        print(f"{other_cam}: RED light ON")

                # Wait for the green duration of the current camera
                green_duration = traffic_data_copy["green_duration"][cam]
                await asyncio.sleep(green_duration)

                # Turn the current camera light YELLOW
                await session.get(f"{camera_url}:85/YELLOW")
                print(f"{cam}: YELLOW light ON")

                # Wait for 1 second before the next cycle
                await asyncio.sleep(1)


@app.get("/traffic")
async def get_traffic_data():
    traffic_data["green_duration"] = allocate_durations(
        traffic_data, total_cycle_time - 3
    )

    return traffic_data
