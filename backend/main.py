from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
import numpy as np
import tensorflow as tf
from PIL import Image
import io
import time

# App init
app = FastAPI(
    title="U-Net Butterfly Segmentation API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

# Load Model
MODEL_PATH = "saved_model/final_UNET_Butterfly_Segmentation.keras"
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

# Utils
def preprocess_image(image: Image.Image):
    image = image.resize((256, 256))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)

# Prediction API
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    input_tensor = preprocess_image(image)

    start = time.time()
    pred = model.predict(input_tensor)[0, :, :, 0]
    inference_time = round(time.time() - start, 4)

    mask = (pred > 0.5).astype(np.uint8) * 255
    mask_img = Image.fromarray(mask)

    buf = io.BytesIO()
    mask_img.save(buf, format="PNG")
    buf.seek(0)

    headers = {
        "X-Inference-Time": str(inference_time)
    }

    return Response(
        content=buf.read(),
        media_type="image/png",
        headers=headers
    )
