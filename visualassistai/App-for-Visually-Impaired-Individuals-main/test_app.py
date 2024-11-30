import google.generativeai as genai
import streamlit as st
from gtts import gTTS
from PIL import Image

# Configure the Gemini API key
API_KEY = "AIzaSyB-7cKMdUpA5kTccpNxd72IT5CjeSgSmkc"
genai.configure(api_key=API_KEY)

# Define the Gemini model
MODEL_NAME = "gemini-1.5-flash"

# Define prompts
TEXT_EXTRACTION_PROMPT = '''Analyze the input image and extract only the text present in the image. 
Ensure that the text is extracted accurately, including any formatting or spacing where applicable. 
If there is no text present in the image, respond politely with the message: 'There is no text in the image.' 
Do not include any additional information or output other than the extracted text or the polite message.'''

ACCESSIBLE_DESCRIPTION_PROMPT = '''Describe the image in a way that is accessible to a visually impaired person. Focus on tactile and auditory details, and avoid using visual metaphors.
Additional Tips:
- Use words that evoke tactile sensations (e.g., "smooth," "rough," "soft").
- Use words that evoke auditory sensations (e.g., "loud," "quiet," "rumbling").
- Avoid using phrases like "looks like" or "seems like" as they rely on visual understanding.'''

# Helper functions
def extract_text_from_image(image, prompt):
    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        return f"Error: {e}"

def generate_description(image_path, prompt):
    """Generate description using Gemini API."""
    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content([image_path, prompt])
        return response.text
    except Exception as e:
        return f"Error: {e}"

def text_to_speech(text, language='en', output_file='output.mp3'):
    """
    Convert text to speech and save it as an audio file. Play it directly on Streamlit.
    """
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_file)
        st.audio(output_file, format="audio/mp3")
    except Exception as e:
        st.error(f"Error: {e}")

# Streamlit App Layout
st.set_page_config(page_title="VisionAssist", page_icon="️", layout="centered")

# Main title and description
st.title("VisionAssist ️")
st.markdown("AI for Scene Understanding, Text Extraction & Speech for the Visually Impaired ")

# Image upload section
st.header("Upload an Image")
uploaded_file = st.file_uploader("Drag and drop or browse an image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)  # Updated to use_container_width

    # Feature Selection Buttons (Show only after image upload)
    st.subheader("Features")
    feature_choice = st.radio("", ["Select an Option", "Describe Scene", "Extract Text"], index=0)  # Default to 'Select an Option'

    # Feature actions based on selection
    if feature_choice == "Describe Scene":
        st.subheader("Image Description (Text-to-Speech Available)")
        description = generate_description(img, ACCESSIBLE_DESCRIPTION_PROMPT)
        st.write(description)
        if description:  # Only show Text-to-Speech button if description exists
            if st.button("Convert Description to Speech"):
                text_to_speech(description)

    elif feature_choice == "Extract Text":
        st.subheader("Extracted Text (Text-to-Speech Available)")
        extracted_text = extract_text_from_image(img, TEXT_EXTRACTION_PROMPT)
        st.text_area("Extracted Text", extracted_text, height=200)
        
        if extracted_text:  # Only show Text-to-Speech button if extracted text exists
            if st.button("Convert Text to Speech"):
                text_to_speech(extracted_text)
