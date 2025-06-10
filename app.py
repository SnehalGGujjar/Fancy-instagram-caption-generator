import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import random

# Load model & processor
st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return processor, model, device

processor, model, device = load_model()

# Fancy caption generator
def make_fancy(caption):
    emojis = ["✨", "🌟", "💫", "🔥", "💖", "📸", "🌈", "🌸", "😎", "🧡"]
    starters = [
        "Serving looks 😍 —", "Just vibes ✨", "In my element 💁‍♀️ —",
        "Golden hour magic 🌅", "Aesthetic overload 🎨 —", "Casual slay 🕶️ —"
    ]
    enders = [
        " #mood", " #wanderlust", " #aesthetic", " #vibes", " #instadaily", " #sunsetlover"
    ]
    caption = caption[0].upper() + caption[1:]
    return f"{random.choice(starters)} {caption} {random.choice(emojis)}{random.choice(enders)}"

# UI
st.title("📸 Fancy Instagram Caption Generator")
st.caption("Upload your image and get a trendy caption ready to post!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("✨ Generate Fancy Caption"):
        with st.spinner("Generating..."):
            inputs = processor(images=image, return_tensors="pt").to(device)
            outputs = model.generate(**inputs)
            caption = processor.decode(outputs[0], skip_special_tokens=True)
            fancy_caption = make_fancy(caption)
        st.success("Done!")
        st.markdown(f"**📝 Caption:**\n\n> {fancy_caption}")
