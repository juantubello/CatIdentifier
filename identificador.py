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

    # Recortar área central del plato (ajustable)
    crop = image_cv[h//3:h*2//3, w//3:w*2//3]

    # Calcular color promedio
    avg_color = crop.mean(axis=(0, 1))  # BGR
    b, g, r = avg_color

    print(f"Color promedio: R={r:.0f}, G={g:.0f}, B={b:.0f}")

    # Comparar contra colores aproximados
    if r > 180 and g > 180 and b > 180:
        return "Luna"     # Blanca
    elif r < 80 and g < 80 and b < 80:
        return "Diana"    # Negra
    else:
        return "Artemis"  # Gris (intermedio)

@app.post("/identificar")
async def identificar(request: Request):
    data = await request.body()
    image = Image.open(BytesIO(data)).convert("RGB")
    gato = identificar_gato_por_color(image)
    return JSONResponse(content={"gato": gato})
