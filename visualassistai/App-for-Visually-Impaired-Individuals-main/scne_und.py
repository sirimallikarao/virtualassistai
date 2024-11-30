import google.generativeai as genai
import streamlit as st
from PIL import Image

# Configure the Gemini API key
API_KEY = "AIzaSyB-7cKMdUpA5kTccpNxd72IT5CjeSgSmkc"
genai.configure(api_key=API_KEY)

# Define the Gemini model
MODEL_NAME = "gemini-1.5-flash"

def generate_description(image_path, prompt):
    """Generate description using Gemini API."""
    model = genai.GenerativeModel(model_name=MODEL_NAME)
    response = model.generate_content([image_path, prompt])
    return response.text

# Define the prompt
PROMPT = '''Describe the image in a way that is accessible to a visually impaired person. Focus on tactile and auditory details, and avoid using visual metaphors.
Additional Tips:
- Use words that evoke tactile sensations (e.g., "smooth," "rough," "soft").
- Use words that evoke auditory sensations (e.g., "loud," "quiet," "rumbling").
- Avoid using phrases like "looks like" or "seems like" as they rely on visual understanding.'''

# Streamlit app layout
st.title("Accessible Image Description App")
st.write("Upload an image to generate a description tailored for visually impaired individuals.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    # Generate description
    if st.button("Generate Description"):
        try:
            # Save the uploaded image locally
            # img.save("temp_image.jpg")
            
            # Call the API
            description = generate_description(img, PROMPT)
            
            # Display the description
            st.subheader("Generated Description")
            st.write(description)
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Please upload an image to proceed.")
