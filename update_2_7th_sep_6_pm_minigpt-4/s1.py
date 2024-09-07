import requests
from PIL import Image
from io import BytesIO
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the MiniGPT-4 model (BLIP in this case)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


processor.save_pretrained("./gpt4mini_processor")
model.save_pretrained("./gpt4mini_model")