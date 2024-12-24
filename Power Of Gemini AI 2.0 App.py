from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()  # take environment variables from .env.

# Configure Google API key for Gemini
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key="GOOGLE_API_KEY")

# Initialize Gemini model
model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
chat = model.start_chat(history=[])

# Function to get response from Gemini model for text input
def get_gemini_text_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Function to get response from Gemini model for text and image input
def get_gemini_image_response(input_text, image):
    response = model.generate_content([input_text, image])
    return response.text

# Streamlit setup
st.set_page_config(page_title="Gemini Q&A Demo", layout="wide")

# Background image CSS (Adjust path if necessary)
background_image_url = "https://www.pngmagic.com/product_images/create-black-youtube-thumbnail-background-in-photoshop_10c.jpeg"  # Replace with the correct path
background_css = f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        color: white;
    }}
    </style>
"""
st.markdown(background_css, unsafe_allow_html=True)

# About the app section
st.markdown("""
    ## Power of Gemini-2.0
    
    This is a Gemini-powered Q&A application. The app uses Google's **Gemini 2.0** generative model to answer 
    your questions and provide insights about uploaded images. 
    - You can ask any questions related to various topics.
    - Upload an image, and the app will generate insights and descriptions based on it.
    
    Whether you want to learn something new or analyze an image, this app leverages advanced AI 
    to give you detailed responses, powered by the cutting-edge Gemini model from Google.
""")

# Input for text-based Q&A
input_text = st.text_input("Enter a Question: ", key="input_text")

# Input for image-based Q&A
uploaded_image = st.file_uploader("Upload an Image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
else:
    image = None

# Button to trigger text-based Q&A
if st.button("Answer the Question (Text-based)"):
    if input_text:
        response = get_gemini_text_response(input_text)
        st.subheader("Response:")
        for chunk in response:
            st.write(chunk.text)
        st.write(chat.history)
    else:
        st.warning("Please enter a question.")

# Button to trigger image-based Q&A
if st.button("About the Image"):
    if uploaded_image is not None:
        response = get_gemini_image_response(input_text, image)
        st.subheader("Response about the Image:")
        st.write(response)
    else:
        st.warning("Please upload an image.")
