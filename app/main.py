from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import replicate
import os
from typing import List
from pathlib import Path
import zipfile

app = FastAPI()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
UPLOAD_DIR = "uploads"

# Pydantic models for API inputs
class CreateModel(BaseModel):
    owner: str
    name: str
    description: str = "an example model"
    visibility: str = "public"
    hardware: str = "gpu-a40-large"

class ImagePrompt(BaseModel):
    prompt: str
    owner_name: str 
    name: str 
    version: str 
    
class FineTuneModel(BaseModel):
    destination: str
    trigger_word: str
    

# Global variable to store the uploaded zip file path
uploaded_zip_path = None

@app.post("/upload_files")
async def upload_files(files: List[UploadFile] = File(...)):
    global uploaded_zip_path
    try:
        # Create a directory to store the uploaded files
        upload_path = Path(UPLOAD_DIR)
        upload_path.mkdir(parents=True, exist_ok=True)

        # Save uploaded files
        for file in files:
            file_path = upload_path / file.filename
            with file_path.open("wb") as f:
                f.write(await file.read())

        # Check if a zip file is uploaded
        if any(file.filename.endswith(".zip") for file in files):
            for file in files:
                if file.filename.endswith(".zip"):
                    with zipfile.ZipFile(file_path, "r") as zip_ref:
                        zip_ref.extractall(upload_path)
                    uploaded_zip_path = file_path
        else:
            # Zip individual image files if not already zipped
            zip_filename = upload_path / "training_data.zip"
            with zipfile.ZipFile(zip_filename, "w") as zipf:
                for file in files:
                    file_path = upload_path / file.filename
                    zipf.write(file_path, arcname=file.filename)
            uploaded_zip_path = zip_filename

        return JSONResponse(content={"message": "Files uploaded successfully."})
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading files: {str(e)}")


@app.post("/create_model")
async def create_model(model_details: CreateModel):
    try:
        model = replicate.models.create(
            owner=model_details.owner,
            name=model_details.name,
            visibility=model_details.visibility,
            hardware=model_details.hardware,
            description=model_details.description
        )
        print(f"Model created: {model.name}")
        print(f"Model URL: https://replicate.com/{model.owner}/{model.name}")

        return JSONResponse(content={"message": "Model created successfully."})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating model: {str(e)}")


@app.post("/fine_tune_model")
async def fine_tune_model(params: FineTuneModel):
    global uploaded_zip_path
    try:
        if uploaded_zip_path is None:
            raise HTTPException(status_code=400, detail="No zip file uploaded")

        # Create the training
        training = replicate.trainings.create(
            version="ostris/flux-dev-lora-trainer:4ffd32160efd92e956d39c5338a9b8fbafca58e03f791f6d8011f3e20e8ea6fa",
            input={
                "input_images": open(uploaded_zip_path, "rb"),
                "steps": 1000,
                "trigger_word": params.trigger_word,
            },
            destination=params.destination
        )

        print(f"Training started: {training.status}")
        print(f"Training URL: https://replicate.com/p/{training.id}")

        return JSONResponse(content={"message": "Training started successfully.", "training_id": training.id})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fine-tuning model: {str(e)}")
    
    
@app.post("/generate_image")
async def generate_image(image_prompt: ImagePrompt):
    try:
        prompt = image_prompt.prompt
        owner_name = image_prompt.owner_name  # Updated field name
        name = image_prompt.name  # Updated field name
        version = image_prompt.version  # Updated field name

        # Use Replicate to generate an image with the fine-tuned model
        output = replicate.run(
            f"{owner_name}/{name}:{version}",
            input={
                "prompt": prompt,
                "output_format": "webp",
                "prompt_upsampling": True,
                "model": "schnell",
            },
            timeout=30
        )

        # Extract URLs from the FileOutput objects
        urls = [str(file_output) for file_output in output]

        # Handle the output
        if len(urls) > 0:
            image_url = urls[0]  # Extract the first URL from the output list
            return JSONResponse(content={"image_url": image_url})
        else:
            raise ValueError("No valid image URL returned.")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error generating image: {str(e)}")