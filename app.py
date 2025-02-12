from flask import Flask, request, jsonify, send_file
import speech_recognition as sr
import os
from gtts import gTTS
import wolframalpha
from selenium import webdriver

app = Flask(__name__)
num = 1  # Global variable for unique naming of mp3 files

# Function to generate speech response
def assistant_speaks(output):
    global num
    num += 1
    print("Assistant: ", output)

    # Convert text to speech using gTTS
    toSpeak = gTTS(text=output, lang='en', slow=False)
    file = str(num) + ".mp3"
    toSpeak.save(file)

    return file

# Function to process text and handle different commands
def process_text(input):
    try:
        if 'search' in input or 'play' in input:
            search_web(input)
            return
        elif "who are you" in input or "define yourself" in input:
            speak = '''Hello, I am your personal assistant. 
            I am here to help you with various tasks.'''
            return assistant_speaks(speak)
        elif "who made you" in input or "created you" in input:
            speak = "I have been created by your developer."
            return assistant_speaks(speak)
        elif "calculate" in input.lower():
            app_id = "YOUR_WOLFRAMALPHA_APP_ID"  # Use your WolframAlpha app ID here
            client = wolframalpha.Client(app_id)
            indx = input.lower().split().index('calculate')
            query = input.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            return assistant_speaks("The answer is " + answer)
        else:
            return assistant_speaks("I can search the web for you, Do you want to continue?")
    except:
        return assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")

# Function to perform web search
def search_web(input):
    driver = webdriver.Firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()

    if 'youtube' in input.lower():
        speak = "Opening in youtube"
        assistant_speaks(speak)
        indx = input.lower().split().index('youtube')
        query = input.split()[indx + 1:]
        driver.get("http://www.youtube.com/results?search_query=" + '+'.join(query))
    else:
        speak = "Searching on Google"
        assistant_speaks(speak)
        driver.get("https://www.google.com/search?q=" + '+'.join(input.split()))

# Endpoint to handle user speech input
@app.route('/get_audio', methods=['POST'])
def get_audio():
    if 'audio' not in request.files:
        return jsonify({"text": "No audio file found."}), 400

    audio_file = request.files['audio']
    audio_file.save('user_audio.wav')

    # Perform speech recognition on the saved file
    try:
        rObject = sr.Recognizer()
        with sr.AudioFile('user_audio.wav') as source:
            audio = rObject.record(source)  # Read the entire audio file
        text = rObject.recognize_google(audio, language='en-US')
        print("You: ", text)
        return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"text": "Could not understand the audio."}), 400
    except Exception as e:
        print(e)
        return jsonify({"text": "Error processing the audio."}), 500

# Endpoint to process text and get assistant response
@app.route('/process_text', methods=['POST'])
def process_request():
    data = request.get_json()
    user_input = data.get('text', '')

    if not user_input:
        return jsonify({"message": "No input provided"}), 400

    response_file = process_text(user_input)  # process_text should return the file path
    return send_file(response_file, mimetype='audio/mp3')

# Start the Flask application
if __name__ == "__main__":
    app.run(debug=True)
