from transformers import pipeline
import torch
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from datetime import datetime


# device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipeline(
    "object-detection", model="jozhang97/deta-swin-large", force_download=True
)
print("cuda available", torch.cuda.is_available())
# pipe = pipe.to(device)
# detections = pipe(image)
# detections


def draw_bounding_boxes(image_path, vehicles):
    # Open the image from the file path
    image = image_path
    # Ensure image is in RGB mode to draw text and shapes properly
    if image.mode != "RGB":
        image = image.convert("RGB")

    draw = ImageDraw.Draw(image)

    # Optionally, load a better font (adjust path as necessary)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20
        )
    except IOError:
        font = ImageFont.load_default()  # Use default if font is not found

    for vehicle in vehicles:
        box = vehicle["box"]
        # Draw the rectangle for bounding box
        draw.rectangle(
            [(box["xmin"], box["ymin"]), (box["xmax"], box["ymax"])],
            outline="red",
            width=3,
        )
        # Add label and score slightly above the box
        label = f"{vehicle['label']} {vehicle['score']:.2f}"
        draw.text(
            (box["xmin"], box["ymin"] - 10),  # Slightly above the box
            label,
            fill="red",
            font=font,
        )

    image.save(f"output/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg")


def get_detections(image, viz=False):
    detections = pipe(image)
    detections

    vehicle_labels = {"car", "truck", "bus", "motorcycle", "bicycle"}

    # Filter only vehicles
    vehicles = [d for d in detections if d["label"] in vehicle_labels]

    print("no of vehicles detected: ", len(vehicles))
    if viz:
        draw_bounding_boxes(image, vehicles)
    return len(vehicles)


def get_detections_batch(images, viz=False):
    """
    Process a batch of images to detect vehicles.

    Args:
        images (list): A list of image objects.
        pipe (callable): Detection pipeline function that supports batch processing and returns detections.
        viz (bool): Whether to visualize the bounding boxes on the images. Defaults to False.

    Returns:
        list: A list of integers representing the count of vehicles detected in each image.
    """

    vehicle_labels = {"car", "truck", "bus", "motorcycle", "bicycle"}

    # Process all images in a batch
    batch_detections = pipe(images)
    # print("detections", batch_detections)
    # print(batch_detections)
    results = []
    for image, detections in zip(images, batch_detections):
        vehicles = [d for d in detections if d["label"] in vehicle_labels]
        print("Number of vehicles detected:", len(vehicles))
        if viz:
            draw_bounding_boxes(image, vehicles)
        results.append(len(vehicles))

    return results


if __name__ == "__main__":
    print(get_detections(Image.open("a.jpg"), viz=True))
