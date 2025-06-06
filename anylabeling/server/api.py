from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import cv2
import base64
from typing import Optional

from anylabeling.services.auto_labeling.model_manager import ModelManager

app = FastAPI()

model_manager = ModelManager()

class PredictRequest(BaseModel):
    model: str
    image: str
    filename: Optional[str] = None
    text_prompt: Optional[str] = None
    run_tracker: bool = False

class PredictResponse(BaseModel):
    shapes: list
    replace: bool = True
    description: str = ""

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    # Load model if necessary
    if (
        model_manager.loaded_model_config is None
        or model_manager.loaded_model_config.get("name") != req.model
    ):
        model_id = None
        for i, cfg in enumerate(model_manager.model_configs):
            if cfg.get("name") == req.model:
                model_id = i
                break
        if model_id is None:
            return {"shapes": [], "replace": True, "description": "model not found"}
        model_manager._load_model(model_id)

    img_bytes = base64.b64decode(req.image)
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    result = model_manager.predict_shapes(
        image,
        filename=req.filename,
        text_prompt=req.text_prompt,
        run_tracker=req.run_tracker,
        batch=True,
    )

    shapes = [s.to_dict() for s in result.shapes]
    return {
        "shapes": shapes,
        "replace": result.replace,
        "description": result.description,
    }

