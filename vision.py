from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API key for Google Gemini
os.environ["GOOGLE_API_KEY"] = "AIzaSyADEqsYKbgEv6k2wWaZSOSTGtcP_oyZOHI"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# Define the financial extractor function
def extract_financial_data(input_text, image_data=None):
    # Specify the Gemini model to use
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Prepare input
    inputs = [input_text]
    if image_data:
        inputs.append(image_data)
    
    # Generate a response from the model
    response = model.generate_content(inputs)
    return response.text

# Process uploaded image file
def process_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        # Convert uploaded file to bytes
        bytes_data = uploaded_file.getvalue()
        return {
            "mime_type": uploaded_file.type,  # e.g., image/png
            "data": bytes_data
        }
    else:
        return None

# Initialize Streamlit app
st.set_page_config(page_title="Financial Data Extractor", layout="wide")
st.title("Financial Data Extractor")
st.write("Extract financial data from a prompt, a file, or both!")

# Toggle input method
st.subheader("Choose Input Method:")
input_method = st.radio("Select an option:", ["Prompt Only", "Upload File", "Both"])

# Input prompt
input_prompt = st.text_area(
    "Enter a financial data extraction prompt:",
    value="""
    You are a financial data extraction expert. Analyze the input to extract:
    - Invoice number
    - Date
    - Vendor name
    - Subtotal
    - Tax amount
    - Total amount
    """,
    height=150
)

# File upload (if applicable)
uploaded_file = None
if input_method in ["Upload File", "Both"]:
    uploaded_file = st.file_uploader("Upload a financial document (JPG, PNG):", type=["jpg", "jpeg", "png"])

# Display uploaded image (if applicable)
if input_method in ["Upload File", "Both"] and uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Document", use_column_width=True)
    except Exception as e:
        st.error(f"Error loading file: {e}")

# Submit button
if st.button("Extract Financial Data"):
    try:
        # Process uploaded image if available
        image_data = None
        if input_method in ["Upload File", "Both"] and uploaded_file:
            image_data = process_uploaded_image(uploaded_file)

        # Extract financial data
        extracted_data = extract_financial_data(input_prompt, image_data)

        # Display the extracted data
        st.subheader("Extracted Financial Data:")
        st.write(extracted_data)
    except Exception as e:
        st.error(f"Error during extraction: {e}")