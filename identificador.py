from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input

app = FastAPI()

# Cargar modelo TFLite
interpreter = tf.lite.Interpreter(model_path="modelo_gatas_3.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Cargar etiquetas
with open("labels.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# Umbral de confianza (ajustable)
UMBRAL_CONF = 0.7

# Preprocesamiento de imagen
def preprocess_image(image, size):
    image = image.resize(size)
    image = np.array(image).astype(np.float32)
    image = preprocess_input(image)  # Mismo preprocesamiento que durante el entrenamiento
    image = np.expand_dims(image, axis=0)
    return image

@app.post("/identificar")
async def identificar(request: Request):
    data = await request.body()
    image = Image.open(BytesIO(data)).convert("RGB")

    input_data = preprocess_image(image, (224, 224))

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])[0]

    max_prob = float(np.max(output_data))
    predicted_index = int(np.argmax(output_data))

    if max_prob < UMBRAL_CONF:
        predicted_label = "ninguna"
    else:
        predicted_label = class_names[predicted_index]

    return JSONResponse(content={
        "gato": predicted_label,
        "confianza": round(max_prob, 3)
    })
