import os
import time
import cv2
import hashlib
import pandas as pd
from pathlib import Path
from flask import Flask, render_template, Response, jsonify
import google.generativeai as genai
import random


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

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
]


# Initialize model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

app = Flask(__name__)
uploaded_files = []
results = []
last_captured_time = 0
frame_interval = 1  


def upload_if_needed(pathname: str) -> list[str]:
    path = Path(pathname)
    hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
    try:
        existing_file = genai.get_file(name=hash_id)
        return [existing_file]
    except:
        uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
        return [uploaded_files[-1]]

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


def gen_frames():
    global last_captured_time
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            current_time = time.time()

            if current_time - last_captured_time >= frame_interval:
                last_captured_time = current_time
                image_path = 'frame.jpg'
                cv2.imwrite(image_path, frame)

                # Single prompt
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
                        results.append([trash_type, classification, instructions])
                    
                    # Overlay "Trash Detected" on the frame
                    frame = cv2.putText(frame, "Trash Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                        1, (0, 0, 255), 2, cv2.LINE_AA)
                else:
                    results.append(["No trash detected", "", ""])

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/results')
def get_results():
    df = pd.DataFrame(results, columns=["Trash Type", "Classification", "Instructions"])
    return df.to_html(index=False)

@app.route('/')
def index():
    return render_template('indexpapu1.html')

if __name__ == "__main__":
    app.run(debug=True)
