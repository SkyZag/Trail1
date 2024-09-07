import requests
from PIL import Image
from io import BytesIO
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the MiniGPT-4 model (BLIP in this case)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")



# URL of the image
image_url = "https://t3.ftcdn.net/jpg/02/24/57/72/360_F_224577276_kjp2gsqPZoEGb6iD4wQGIiUKfo82kkKK.jpg"

# Download the image
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

custom_prompt = (
    "This image shows trash. Just answer with the type of trash in this image. "
    "Is it e-waste, plastic waste, bio waste, medical waste, or multiple wastes?"
)

# Process the image and generate a classification based on the custom prompt
inputs = processor(images=image, text=custom_prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
response_text = processor.decode(outputs[0], skip_special_tokens=True)

# Extract relevant classification
keywords = ["e-waste", "plastic waste", "bio waste", "medical waste", "multiple wastes"]
classification = next((keyword for keyword in keywords if keyword in response_text.lower()), "Classification not found")

print(f"Trash Classification: {classification}")
