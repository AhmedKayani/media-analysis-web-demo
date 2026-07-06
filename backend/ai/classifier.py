import numpy as np
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions,
)

model = MobileNetV2(weights="imagenet")

def classify_image(image_path: str) -> dict:
    # Load and preprocess the image
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    # Make predictions
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=1)[0][0]

    label = decoded_predictions[1]
    confidence = float(decoded_predictions[2])

    return {
        "class": decoded_predictions[1],
        "probability": float(decoded_predictions[2])
    }
