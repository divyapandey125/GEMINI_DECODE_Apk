from dotenv import load_dotenv

load_dotenv()  # load all the environment variables
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Initialize our streamlit app
input_prompt = """
You are an expert pharmaceutical/Chemist where you need to see the tablets from the image,
and also provide the details of every drug/tablet items with the below format:

Examine the image carefully and identify the tablets depicted.
Describe the uses and functionalities of each tablet shown in the image.

Provide information on the intended purposes, features, and typical applications of the tablets.

If possible, include any notable specifications or distinguishing characteristics of each tablet.

Ensure clarity and conciseness in your descriptions, focusing on key details and distinguishing factors.
"""

## Initialize Streamlit app
st.set_page_config(page_title="AI Chemist App")
st.header("AI Chemist App")
input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me")

## If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input_text)
    st.subheader("The Response is")
    st.write(response)
