import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os

# --- API Key Setup ---


# --- Image Generation Function ---
def generate_image_from_prompt(prompt):
    try:
        client = genai.Client(api_key="AIzaSyBWyEsq0clnAfP5HO6idRAvkgD-hODy4DI")

        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        image_path = None
        message_text = None

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                message_text = part.text
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                image_path = "gemini_generated_image.png"
                image.save(image_path)
                return image_path, message_text

        return None, message_text or "No image data returned."

    except Exception as e:
        return None, f"Error: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Gemini Image Generator", page_icon="🐷")

st.title("CREATE AT YOU STYLE")

prompt = st.text_input("Enter your image prompt:", 
                       placeholder="e.g., A pig with wings flying over a sci-fi city")

if st.button("Generate Image"):
    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    else:
        with st.spinner("⏳ Generating image, please wait..."):
            image_file, extra_text = generate_image_from_prompt(prompt)

        if image_file:
            st.success("✅ Image generated successfully!")
            st.image(image_file, use_container_width=True)
            if extra_text:
                st.markdown(f"*Model response:* {extra_text}")
        else:
            st.error(f"❌ Failed to generate image.\n{extra_text}")