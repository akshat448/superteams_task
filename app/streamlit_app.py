import streamlit as st
import requests
from pathlib import Path
from streamlit_option_menu import option_menu

# Set the FastAPI base URL
BASE_URL = "http://localhost:8000"

# Function to upload files
def upload_files(files):
    files_to_upload = [("files", (file.name, file, file.type)) for file in files]
    response = requests.post(f"{BASE_URL}/upload_files", files=files_to_upload)
    return response.json()

# Function to create a model
def create_model(owner, name, description, visibility, hardware):
    data = {
        "owner": owner,
        "name": name,
        "description": description,
        "visibility": visibility,
        "hardware": hardware
    }
    response = requests.post(f"{BASE_URL}/create_model", json=data)
    return response.json()

# Function to fine-tune a model
def fine_tune_model(destination, trigger_word):
    data = {
        "destination": destination,
        "trigger_word": trigger_word
    }
    response = requests.post(f"{BASE_URL}/fine_tune_model", json=data)
    return response.json()

# Function to generate an image
def generate_image(prompt, model_owner_name, model_name, model_version):
    data = {
        "prompt": prompt,
        "model_owner_name": model_owner_name,
        "model_name": model_name,
        "model_version": model_version
    }
    response = requests.post(f"{BASE_URL}/generate_image", json=data)
    return response.json()

# Page: Upload Files
def page_upload_files():
    st.header("Upload Training Images")
    uploaded_files = st.file_uploader("Choose files", type=["zip", "jpg", "png", "jpeg"], accept_multiple_files=True)
    if uploaded_files:
        if st.button("Upload"):
            result = upload_files(uploaded_files)
            st.write(result)

# Page: Create Model
def page_create_model():
    st.header("Create Model")
    owner = st.text_input("Owner")
    name = st.text_input("Model Name")
    description = st.text_input("Description", value="an example model")
    visibility = st.selectbox("Visibility", ["public", "private"])
    hardware = st.selectbox("Hardware", ["gpu-a40-large", "gpu-t4", "cpu"])
    if st.button("Create Model"):
        result = create_model(owner, name, description, visibility, hardware)
        st.write(result)

# Page: Fine-Tune Model
def page_fine_tune_model():
    st.header("Fine-Tune Model")
    destination = st.text_input("Destination (modelname/modelID)")
    trigger_word = st.text_input("Trigger Word")
    if st.button("Fine-Tune Model"):
        result = fine_tune_model(destination, trigger_word)
        st.write(result)

# Page: Generate Image
def page_generate_image():
    st.header("Generate Image")
    prompt = st.text_input("Prompt")
    model_owner_name = st.text_input("Model Owner Name")
    model_name = st.text_input("Model Name")
    model_version = st.text_input("Model Version")
    if st.button("Generate Image"):
        result = generate_image(prompt, model_owner_name, model_name, model_version)
        if "image_url" in result:
            st.image(result["image_url"], caption="Generated Image")
        else:
            st.write(result)

# Main app layout
st.title("Replicate Image Generation App")

# Sidebar menu for navigation
with st.sidebar:
    selected = option_menu(
        "Menu",
        ["Upload Files", "Create Model", "Fine-Tune Model", "Generate Image"],
        icons=["cloud-upload", "plus-circle", "tools", "image"],
        menu_icon="cast",
        default_index=0,
    )

# Page routing
if selected == "Upload Files":
    page_upload_files()
elif selected == "Create Model":
    page_create_model()
elif selected == "Fine-Tune Model":
    page_fine_tune_model()
elif selected == "Generate Image":
    page_generate_image()