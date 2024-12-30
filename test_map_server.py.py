from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
import time

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def generate_traffic_data():
    """Generate random traffic data for testing"""
    colors = ["red", "yellow", "green"]
    return {
        "lights": {
            "cam1": random.choice(colors),
            "cam2": random.choice(colors),
            "cam3": random.choice(colors),
        },
        "num_vehicles": {
            "cam1": random.randint(0, 20),
            "cam2": random.randint(0, 20),
            "cam3": random.randint(0, 20),
        },
    }


@app.get("/traffic")
async def get_traffic_data():
    """Endpoint to get traffic data"""
    return generate_traffic_data()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
