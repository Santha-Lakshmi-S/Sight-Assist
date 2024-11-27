import streamlit as st
from PIL import Image
import pyttsx3
import os
import pytesseract  
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

GEMINI_API_KEY = "AIzaSyCsC_YDsc56I6V7jmeJbC5nkc14A4Ql2ow"
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)
engine = pyttsx3.init()

st.set_page_config(page_title="Sight Assist", page_icon="👁️")
st.markdown(
    """
    <style>
        .main-title {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: #0662f6;
            margin-top: -20px;
        }
        .subtitle {
            font-size: 18px;
            color: #555;
            text-align: center;
            margin-bottom: 20px;
        }
        .feature-header {
            font-size: 24px;
            color: #333;
            font-weight: bold;
        }
        .instructions {
            font-size: 16px;
            color: #333;
            margin-bottom: 30px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">SIGHT ASSIST</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI App for Visually Impaired Text Reading and Image Analysis</div>', unsafe_allow_html=True)

st.sidebar.markdown("""
    <h3 class="feature-header">Key Features</h3>
    <ul>
        <li><b>Scene Description</b>: AI-generated insights about the image.</li>
        <li><b>Text Extraction</b>: OCR-based text extraction from images.</li>
        <li><b>Text-to-Speech</b>: Converts extracted text to speech for accessibility.</li>
    </ul>
    <h3 class="feature-header">How It Helps</h3>
    <p class="instructions">Assist visually impaired users by providing scene descriptions, extracting text, and enabling speech.</p>
    <h3 class="feature-header">Powered By</h3>
    <ul>
        <li><b>Google Gemini API</b>: AI-powered scene understanding.</li>
        <li><b>Tesseract OCR</b>: Text extraction from images.</li>
        <li><b>pyttsx3</b>: Converts text to speech.</li>
    </ul>
""", unsafe_allow_html=True)

st.sidebar.text_area(
    "📜 Instructions",
    """Upload an image to start. 
    Choose a feature to interact with:
    1. Describe the Scene
    2. Extract Text
    3. Listen to it"""
)

# Functions
def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    return pytesseract.image_to_string(image)

def text_to_speech(text):
    """Converts the given text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Image Upload
st.markdown("<h3 class='feature-header'>📤 Upload an Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Feature buttons for description, text extraction, and text-to-speech
st.markdown("""
    <h3 class='feature-header'>⚙️ Choose a Feature</h3>
    <p style="text-align: center; color: #555;">Select one of the following actions:</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    scene_button = st.button("🔍 **Describe Scene**", help="Generate an AI description of the scene in the image.")
with col2:
    ocr_button = st.button("📝 **Extract Text**", help="Extract visible text from the image using OCR.")
with col3:
    tts_button = st.button("🔊 **Text-to-Speech**", help="Convert the extracted text to speech.")

# Prepare the image data for processing
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
"""

if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Generating scene description..."):
            response = generate_scene_description(input_prompt, image_data)
            st.markdown("<h3 class='feature-header'>🔍 Scene Description</h3>", unsafe_allow_html=True)
            st.write(response)

    if ocr_button:
        with st.spinner("Extracting text from the image..."):
            text = extract_text_from_image(image)
            st.markdown("<h3 class='feature-header'>📝 Extracted Text</h3>", unsafe_allow_html=True)
            st.text_area("Extracted Text", text, height=150)

    if tts_button:
        with st.spinner("Converting text to speech..."):
            text = extract_text_from_image(image)
            if text.strip():
                text_to_speech(text)
                st.success("✅ Text-to-Speech Conversion Completed!")
            else:
                st.warning("No text found to convert.")