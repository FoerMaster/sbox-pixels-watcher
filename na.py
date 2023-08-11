import asyncio
import json
import websockets
import numpy as np
import cv2
from PIL import Image

url = "ws://pixels-web.conna.org:8080"
headers = {
    "User-Agent": "facepunch-sbox",
    "Authorization": 'sbox "test"',
    "Referer": "https://sbox.facepunch.com/",
    "Connection": "Upgrade",
    "Upgrade": "websocket"
}

image_width = 1024
image_height = 1024
image = np.zeros((image_height, image_width, 3), dtype=np.uint8)

# Palette colors not real colors, sry...
palette = np.array([
    [0, 0, 0],       # Black
    [255, 255, 255], # White
    [255, 0, 0],     # Red
    [0, 255, 0],     # Green
    [0, 0, 255],     # Blue
    [255, 255, 0],   # Yellow
    [0, 255, 255],   # Cyan
    [255, 0, 255],   # Magenta
    [128, 0, 0],     # Maroon
    [0, 128, 0],     # Green (lime)
    [0, 0, 128],     # Navy
    [128, 128, 0],   # Olive
    [0, 128, 128],   # Teal
    [128, 0, 128],   # Purple
    [128, 128, 128], # Gray
    [192, 192, 192], # Silver
    [128, 0, 0],     # Maroon (repeated)
    [0, 128, 0],     # Green (lime) (repeated)
    [0, 0, 128],     # Navy (repeated)
    [128, 128, 0],   # Olive (repeated)
    [0, 128, 128],   # Teal (repeated)
    [128, 0, 128],   # Purple (repeated)
    [128, 128, 128]  # Gray (repeated)
], dtype=np.uint8)

# Load previously saved image (if available)
try:
    saved_image = cv2.imread("saved_image.png")
    if saved_image is not None:
        image = saved_image
except Exception as e:
    print(f"Error loading saved image: {e}")

# WebSocket connection and data handling
async def connect_to_server():
    while True:
        try:
            async with websockets.connect(url, extra_headers=headers) as websocket:
                async for message in websocket:
                    if "setpixel" in message:
                        try:
                            data = json.loads(message.split("#")[1])
                            x = data["Y"]
                            y = data["X"]
                            color_index = data["Color"]
                            color = palette[color_index]

                            image[y, x] = color

                            cv2.imshow("Real-Time Pixel Preview", image)
                            cv2.waitKey(1)

                        except Exception as e:
                            print(f"Error processing message: {e}")
        except Exception as e:
            print(f"Connection error: {e}")
            await asyncio.sleep(1)


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(connect_to_server())
except KeyboardInterrupt:
    pass

cv2.imwrite("saved_image.png", image)
cv2.destroyAllWindows()
