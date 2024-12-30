from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from datetime import datetime


def draw_bounding_boxes(image_path, vehicles):
    # Open the image from the file path
    image = Image.open(image_path)

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


# Example usage
vehicles = [
    {
        "label": "car",
        "score": 0.95,
        "box": {"xmin": 50, "ymin": 100, "xmax": 200, "ymax": 250},
    },
    {
        "label": "bus",
        "score": 0.89,
        "box": {"xmin": 250, "ymin": 150, "xmax": 400, "ymax": 300},
    },
]

draw_bounding_boxes("../a.jpg", vehicles)
