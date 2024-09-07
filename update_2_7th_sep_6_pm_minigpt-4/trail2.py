from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the processor and model
processor = BlipProcessor.from_pretrained("./gpt4mini_processor")
model = BlipForConditionalGeneration.from_pretrained("./gpt4mini_model")

TF_ENABLE_ONEDNN_OPTS = 0

# Path of the local image
image_path = "./temp.jpg"

# Open the image from the local file system
image = Image.open(image_path)

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
