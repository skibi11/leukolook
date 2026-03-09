# app.py
# Adapted to follow the logic from the provided Django api/views.py with added logging
import os
import cv2
import tempfile
import numpy as np
import uvicorn
import base64
import io
from PIL import Image
from inference_sdk import InferenceHTTPClient
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tensorflow as tf
from huggingface_hub import hf_hub_download
import gradio as gr

# --- 1. Configuration and Model Loading ---
# Constants from the new Django logic
MAX_INFER_DIM = 1024
ENHANCED_SIZE = (224, 224)

# Roboflow and TF Model setup
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")
CLIENT_FACE = InferenceHTTPClient(api_url="https://detect.roboflow.com", api_key=ROBOFLOW_API_KEY)
CLIENT_EYES = InferenceHTTPClient(api_url="https://detect.roboflow.com", api_key=ROBOFLOW_API_KEY)
CLIENT_IRIS = InferenceHTTPClient(api_url="https://detect.roboflow.com", api_key=ROBOFLOW_API_KEY)

leuko_model = None
try:
    model_path = hf_hub_download("skibi11/leukolook-eye-detector", "MobileNetV1_best.keras")
    leuko_model = tf.keras.models.load_model(model_path)
    print("--- LEUKOCORIA MODEL LOADED SUCCESSFULLY! ---")
except Exception as e:
    print(f"--- FATAL ERROR: COULD NOT LOAD LEUKOCORIA MODEL: {e} ---")
    raise RuntimeError(f"Could not load leukocoria model: {e}")

# --- 2. Helper Functions (Adapted from Django views.py) ---

def enhance_image_unsharp_mask(image, strength=0.5, radius=5):
    """Enhances image using unsharp masking."""
    blur = cv2.GaussianBlur(image, (radius, radius), 0)
    return cv2.addWeighted(image, 1.0 + strength, blur, -strength, 0)

def detect_faces_roboflow(image_path):
    """Detects faces using Roboflow."""
    return CLIENT_FACE.infer(image_path, model_id="face-detector-v4liw/2").get("predictions", [])

def detect_eyes_roboflow(image_path):
    """
    Detects eyes, resizing the image if necessary for inference,
    then scales coordinates back to the original image size.
    """
    raw_image = cv2.imread(image_path)
    if raw_image is None:
        return None, []

    h, w = raw_image.shape[:2]
    scale = min(1.0, MAX_INFER_DIM / max(h, w))
    
    if scale < 1.0:
        small_image = cv2.resize(raw_image, (int(w*scale), int(h*scale)))
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            cv2.imwrite(tmp.name, small_image)
            infer_path = tmp.name
    else:
        infer_path = image_path

    try:
        resp = CLIENT_EYES.infer(infer_path, model_id="eye-detection-kso3d/3")
    finally:
        if scale < 1.0 and os.path.exists(infer_path):
            os.remove(infer_path)

    crops = []
    for p in resp.get("predictions", []):
        cx, cy = p["x"] / scale, p["y"] / scale
        bw, bh = p["width"] / scale, p["height"] / scale
        
        x1 = int(cx - bw / 2)
        y1 = int(cy - bh / 2)
        x2 = int(cx + bw / 2)
        y2 = int(cy + bh / 2)
        
        crop = raw_image[y1:y2, x1:x2]
        if crop.size > 0:
            crops.append({"coords": (x1, y1, x2, y2), "image": crop})
            
    return raw_image, crops

def get_largest_iris_prediction(eye_crop):
    """Finds the largest iris in an eye crop."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        cv2.imwrite(tmp.name, eye_crop)
        temp_path = tmp.name
    try:
        resp = CLIENT_IRIS.infer(temp_path, model_id="iris_120_set/7")
        preds = resp.get("predictions", [])
        return max(preds, key=lambda p: p["width"] * p["height"]) if preds else None
    finally:
        os.remove(temp_path)

def run_leukocoria_prediction(iris_crop):
    """Runs the loaded TensorFlow model on an iris crop."""
    enh = enhance_image_unsharp_mask(iris_crop)
    enh_rs = cv2.resize(enh, ENHANCED_SIZE)
    
    img_array = np.array(enh_rs) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    prediction = leuko_model.predict(img_array)
    confidence = float(prediction[0][0])
    has_leuko = confidence > 0.5
    return has_leuko, confidence

def to_base64(image):
    """Converts a CV2 image to a base64 string."""
    _, buffer = cv2.imencode(".jpg", image)
    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode()

# --- 3. FastAPI Application ---
app = FastAPI()

@app.post("/detect/")
async def full_detection_pipeline(image: UploadFile = File(...)):
    print("\n--- 1. Starting full detection pipeline. ---")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(await image.read())
        temp_image_path = tmp.name

    try:
        print("--- 2. Checking for faces... ---")
        if not detect_faces_roboflow(temp_image_path):
            print("--- 2a. No face detected. Aborting. ---")
            return JSONResponse(status_code=200, content={"warnings": ["No face detected."]})
        print("--- 2b. Face found. Proceeding. ---")

        print("--- 3. Detecting eyes... ---")
        raw_image, eye_crops = detect_eyes_roboflow(temp_image_path)
        if raw_image is None:
            return JSONResponse(status_code=400, content={"error": "Could not read uploaded image."})
        
        print(f"--- 4. Found {len(eye_crops)} eyes. ---")
        if len(eye_crops) != 2:
            return JSONResponse(status_code=200, content={
                "analyzed_image": to_base64(raw_image),
                "warnings": ["Exactly two eyes not detected."]
            })

        initial_coords = [e['coords'] for e in eye_crops]
        print(f"--- 5. Initial eye coordinates: {initial_coords} ---")

        sorted_eyes = sorted(eye_crops, key=lambda e: e["coords"][0])
        sorted_coords = [e['coords'] for e in sorted_eyes]
        print(f"--- 6. Sorted eye coordinates: {sorted_coords} ---")

        images_b64 = {}
        flags = {}
        
        for i, eye_info in enumerate(sorted_eyes):
            side = "right" if i == 0 else "left"
            print(f"--- 7. Processing side: '{side}' ---")
            eye_img = eye_info["image"]
            
            pred = get_largest_iris_prediction(eye_img)
            if pred:
                print(f"--- 8. Iris found for '{side}' eye. Running leukocoria prediction... ---")
                cx, cy, w, h = pred["x"], pred["y"], pred["width"], pred["height"]
                x1, y1 = int(cx - w / 2), int(cy - h / 2)
                x2, y2 = int(cx + w / 2), int(cy + h / 2)
                
                iris_crop = eye_img[y1:y2, x1:x2]
                
                has_leuko, confidence = run_leukocoria_prediction(iris_crop)
                print(f"--- 9. Prediction for '{side}' eye: Has Leukocoria={has_leuko}, Confidence={confidence:.4f} ---")
                flags[side] = has_leuko
            else:
                print(f"--- 8a. No iris found for '{side}' eye. ---")
                flags[side] = None

            images_b64[side] = to_base64(eye_img)
        
        print(f"--- 10. Final generated flags: {flags} ---")
        return JSONResponse(status_code=200, content={
            "analyzed_image": to_base64(raw_image),
            "two_eyes": images_b64,
            "leukocoria": flags,
            "warnings": []
        })

    finally:
        os.remove(temp_image_path)

# --- 4. Gradio UI (for simple testing) ---
def gradio_wrapper(image_array):
    try:
        pil_image = Image.fromarray(image_array)
        with io.BytesIO() as buffer:
            pil_image.save(buffer, format="JPEG")
            files = {'image': ('image.jpg', buffer.getvalue(), 'image/jpeg')}
            response = requests.post("http://127.0.0.1:7860/detect/", files=files)
            
        return response.json()
    except Exception as e:
        return {"error": str(e)}

gradio_ui = gr.Interface(
    fn=gradio_wrapper,
    inputs=gr.Image(type="numpy", label="Upload an eye image"),
    outputs=gr.JSON(label="Analysis Results"),
    title="LeukoLook Eye Detector",
    description="Demonstration of the full detection pipeline."
)

app = gr.mount_gradio_app(app, gradio_ui, path="/")

# --- 5. Run Server ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)