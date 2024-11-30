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

ACCESSIBLE_DESCRIPTION_PROMPT = ''' Describe the image in a way that is accessible to a visually impaired person. Focus on tactile and auditory details, and avoid using visual metaphors.
Additional Tips:
- Use words that evoke tactile sensations (e.g., "smooth," "rough," "soft").
- Use words that evoke auditory sensations (e.g., "loud," "quiet," "rumbling").
- Avoid using phrases like "looks like" or "seems like" as they rely on visual understanding.'''

SAFE_NAVIGATION_PROMPT = '''Prompt: "Describe the image in a way that is accessible to a visually impaired person. Focus on identifying objects, obstacles, and potential hazards critical for safe navigation. Provide clear details about their positions and relationships in the space. Use simple and direct language, avoiding visual metaphors. Recommend safety precautions or actions where applicable."

Additional Tips:

Specify the types of objects (e.g., furniture, barriers, pathways).
Describe spatial relationships clearly (e.g., "near," "to the left," "in front").
Use straightforward, sensory language where applicable (e.g., "solid," "textured," "silent").
Highlight key elements for safe movement, such as pathways or clearances.
Suggest practical safety measures or precautions (e.g., "maintain distance," "step carefully").'''

# Helper functions
def extract_text_from_image(image, prompt):
    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        return f"Error: {e}"

def generate_description(image, prompt):
    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content([image, prompt])
        return response.text
    except Exception as e:
        return f"Error: {e}"

def analyze_safe_navigation(image, prompt):
    try:
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content([image, prompt])
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
st.set_page_config(
    page_title="VisionAssist AI",
    page_icon="🌟",
    layout="centered"
)

# Initialize session state for active feature
if "active_feature" not in st.session_state:
    st.session_state.active_feature = None
if "description" not in st.session_state:
    st.session_state.description = ""

# Sidebar - Features and Info
st.sidebar.title("VisionAssist AI 🌟")
st.sidebar.markdown("""
### About VisionAssist AI
VisionAssist AI leverages advanced **Generative AI** to provide accessible solutions for visually impaired individuals. Our app transforms visual data into meaningful descriptions, extracted text, or safe navigation insights.

#### Features:
1. **Scene Description**  
   Analyze images and generate rich, detailed descriptions using accessible language. These descriptions focus on tactile and auditory elements to help visually impaired individuals understand their surroundings.

2. **Text Extraction**  
   Extract text embedded within images, making it accessible for those unable to view or read the content visually. This feature ensures accurate text recognition, including formatting.

3. **Safe Navigation Guidance**  
   Identify objects, obstacles, and spatial relationships in the environment. This feature prioritizes user safety by offering actionable insights for navigating the space effectively.

4. **Text-to-Speech Conversion**  
   Transform any generated text or description into clear, audible speech. This feature allows visually impaired users to listen to scene descriptions, extracted text, or navigation details effortlessly.

#### Our Mission
VisionAssist AI is dedicated to empowering independence and enhancing accessibility through cutting-edge AI technology.  
""")

# Main title and description
st.title("🌟 VisionAssist AI")
st.markdown("""
### Empowering Accessibility Through Generative AI
*Your assistant for understanding the world through touch and sound.*
""")

# Image upload section
st.header("🔍 Upload an Image")
uploaded_file = st.file_uploader(
    "Drag and drop or browse an image (JPG, JPEG, PNG)", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image")

    # Feature Selection Buttons
    # st.subheader("🛠️ Select a Feature")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔍 Describe Scene"):
            st.session_state.active_feature = "scene_description"
            st.session_state.description = generate_description(img, ACCESSIBLE_DESCRIPTION_PROMPT)
    with col2:
        if st.button("📝 Extract Text"):
            st.session_state.active_feature = "text_extraction"
            st.session_state.description = extract_text_from_image(img, TEXT_EXTRACTION_PROMPT)
    with col3:
        if st.button("🚶 Safe Navigation"):
            st.session_state.active_feature = "safe_navigation"
            st.session_state.description = analyze_safe_navigation(img, SAFE_NAVIGATION_PROMPT)

    # Display the description based on the active feature
    if st.session_state.active_feature:
        st.subheader("📝 Feature Output")
        st.write(st.session_state.description)

        # Text-to-Speech Button
        if st.button("🔊 Convert to Speech"):
            text_to_speech(st.session_state.description)
