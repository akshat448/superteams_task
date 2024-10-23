# FastAPI and Streamlit Application

This project features a FastAPI backend application integrated with Replicate’s image generation and fine-tuning endpoints. It also includes a Streamlit frontend to enable user interaction, where users can upload images, create and fine-tune models, and generate images based on text prompts.

## Key Features:
1. **File Upload**: Supports image uploads for fine-tuning models.
2. **Model Creation**: Creates new models on Replicate via API.
3. **Fine-Tuning**: Fine-tunes models using training data provided by the user.
4. **Image Generation**: Generates images from a user-provided prompt.

## Table of Contents

- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Endpoints](#endpoints)
- [Streamlit Application](#streamlit-application)
- [Environment Variables](#environment-variables)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/akshat448/superteams_task.git
    cd superteams_task
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate
    # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

### FastAPI Application

1. Run the FastAPI application by executing:

    ```bash
    uvicorn app.main:app --reload
    ```

2. The FastAPI app will be running on `http://localhost:8000`.

### Streamlit Application

1. To run the Streamlit application, execute:

    ```bash
    streamlit run app/streamlit_app.py
    ```

2. The StreamLit app will run on `http://localhost:8501`.


## Endpoints

### 1. POST /upload_files

**Description**: Upload image files or a ZIP archive for training data.

**Request Body**:
- List of images in .jpg, .png, or a .zip file.

**Response**:
```json
{ "message": "Files uploaded successfully." }
```

### 2. POST /create_model

**Description**: Create a new model on Replicate with details like model owner, name, and hardware type.

**Request Body**:
- owner: Model owner's name.
- name: Name of the model.
- hardware: Hardware type (e.g., A100, T4, etc.).

**Response**:
```json
{ "message": "Model created successfully." }
```

### 3. POST /fine_tune_model

**Description**: Fine-tune a model using uploaded training data.

**Request Body**:
- model_id: ID of the model to fine-tune.
- dataset_path: Path to the uploaded dataset.

**Response**:
```json
{ "message": "Training started successfully.", "training_id": "abc123" }
```

### 4. POST /generate_image

**Description**: Generate an image using a prompt and a specified model.

**Request Body**:
- prompt: Text prompt to generate the image.
- model_id: ID of the model to use for image generation.

**Response**:
```json
{ "image_url": "https://..." }
```


