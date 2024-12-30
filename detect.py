from utils import *
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time

# Ngrok URL
# url = "http://192.168.0.101/capture"
url = "http://192.168.0.111/capture"

# Continuously fetch and display the image
try:
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            img_array = np.array(bytearray(response.content), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # plt.imshow(frame_rgb)
            # plt.axis("off")
            # plt.show()
            # time.sleep(1)  # Add a small delay (1 second) between frames
            # plt.close()  # Close the previous frame before showing the next
            image = Image.fromarray(frame_rgb)
            get_detections(image, viz=True)
        else:
            print("Failed to fetch the image. Status code:", response.status_code)
except KeyboardInterrupt:
    print("Stopped fetching images.")
