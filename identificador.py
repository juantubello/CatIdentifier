from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

app = FastAPI()

def identificar_gato_por_color(image):
    # Convertir a OpenCV (BGR)
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    h, w, _ = image_cv.shape

    # Recortar área central del plato
    crop = image_cv[h//3:h*2//3, w//3:w*2//3]

    # Calcular color promedio
    avg_color = crop.mean(axis=(0, 1))  # BGR
    b, g, r = avg_color
    brightness = (r + g + b) / 3

    print(f"Color promedio: R={r:.0f}, G={g:.0f}, B={b:.0f}, Brightness={brightness:.0f}")

    # Nuevas condiciones
    if brightness > 170 and abs(r - g) < 30 and abs(r - b) < 30 and abs(g - b) < 30:
        return "Artemis"     # Blanca
    elif r < 80 and g < 80 and b < 80:
        return "Luna"    # Negra
    else:
        return "Diana"  # Gris

@app.post("/identificar")
async def identificar(request: Request):
    data = await request.body()
    image = Image.open(BytesIO(data)).convert("RGB")
    gato = identificar_gato_por_color(image)
    return JSONResponse(content={"gato": gato})
