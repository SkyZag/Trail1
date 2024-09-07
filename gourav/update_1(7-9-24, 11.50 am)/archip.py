import os
import time
import cv2
import hashlib
import pandas as pd
from pathlib import Path
import google.generativeai as genai
import random
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def gk():
    # Configure API keys
    api_key1 = 'AIzaSyA59iFa2YEp9-4pqdM1pGOJwfOenil9fCI'
    api_key2 = 'AIzaSyDxFSs2n8X1fDNeS5o3HirUi1Y8_ZgixeQ'
    api_key3 = 'AIzaSyAeCq43oM55R9sKp3ceDLCw3ITjTvgua-0'
    api_key4 = 'AIzaSyDcT8abHhg94xH8twWSdzXC_EqLPuuE6W4'

    api_key = eval(f"api_key{random.randint(1,4)}")
    genai.configure(api_key=api_key)

    # Set up model configuration
    generation_config = {
        "temperature": 0.5,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
    }

    # Initialize model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        #safety_settings=safety_settings
    )

    def upload_if_needed(pathname: str) -> list[str]:
        path = Path(pathname)
        hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
        try:
            existing_file = genai.get_file(name=hash_id)
            return [existing_file]
        except:
            uploaded_files = genai.upload_file(path=path, display_name=hash_id)
            return [uploaded_files]

    def generate_response(image_path: str, prompt: str) -> str:
        prompt_parts = [
            prompt,
            *upload_if_needed(image_path),
            "\n",
        ]
        response = model.generate_content(prompt_parts)

        if response and response.candidates and response.candidates[0].safety_ratings:
            safety_rating = response.candidates[0].safety_ratings[0]
            if safety_rating.category == "HARM_CATEGORY_HARASSMENT" and safety_rating.threshold == "BLOCK_MEDIUM_AND_ABOVE":
                return "Content blocked due to safety settings."

        return response.text.strip() if response else "No valid response generated."

    def classify_image(image_path):
        prompt = ("In the first line only 'yes' if there is any trash and 'no' if no trash found. "
                  "In the second line, tell me what trash it is. "
                  "In the third line, if this trash is recyclable, decomposable, or disposable. "
                  "In the next line, how do I do it (recycle, dispose, or decompose) in around 15 words.")
        response = generate_response(image_path, prompt)
        lines = response.split('\n')

        if lines[0].lower() == "yes":
            if len(lines) >= 4:
                trash_type = lines[1]
                classification = lines[2]
                instructions = lines[3]
                return f"Trash Type: {trash_type}\nClassification: {classification}\nInstructions: {instructions}"
            else:
                return "Trash detected but response incomplete."
        else:
            return "No trash detected."

    def open_file():
        file_path = filedialog.askopenfilename(title="Select an Image File",
                                               filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            result_text.set("Classifying...")
            window.update()
            result = classify_image(file_path)
            result_text.set(result)
            display_image(file_path)

    def capture_image():
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            image_path = "captured_image.jpg"
            cv2.imwrite(image_path, frame)
            result_text.set("Classifying...")
            window.update()
            result = classify_image(image_path)
            result_text.set(result)
            display_image(image_path)
        else:
            messagebox.showerror("Error", "Failed to capture image from camera.")

    def display_image(image_path):
        img = Image.open(image_path)
        img = img.resize((300, 300), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        panel.config(image=img_tk)
        panel.image = img_tk

    # GUI Setup
    window = tk.Tk()
    window.title("Trash Classification")
    window.geometry("400x500")

    result_text = tk.StringVar()
    result_text.set("Upload or capture an image to classify.")

    label = tk.Label(window, text="Trash Classifier", font=("Helvetica", 16))
    label.pack(pady=10)

    panel = tk.Label(window)
    panel.pack()

    result_label = tk.Label(window, textvariable=result_text, wraplength=300, justify="left")
    result_label.pack(pady=10)

    upload_button = tk.Button(window, text="Upload Image", command=open_file)
    upload_button.pack(pady=10)

    capture_button = tk.Button(window, text="Capture Image", command=capture_image)
    capture_button.pack(pady=10)

    window.mainloop()

# You can now import this function in another program and call it.
# Example usage:
# from your_module import initialize_trash_classifier
# initialize_trash_classifier()


gk()