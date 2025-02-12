# Voice Assistant with Flask

This project is a simple voice assistant web application built with **Flask**. It takes voice input from the user, processes it, and responds either with text-to-speech or web search results.

## Features

- **Speech Recognition**: Uses Google Speech API to recognize the user's voice.
- **Text-to-Speech**: Uses Google Text-to-Speech (gTTS) to convert responses into speech.
- **Web Search**: Opens Google or YouTube based on the user's request.
- **Calculation**: Uses WolframAlpha API for simple calculations.
- **Microphone Input**: Accepts audio from the user via the web interface.

## Prerequisites

Before you start, ensure you have the following installed:

- Python 3.x
- Flask
- gTTS
- SpeechRecognition
- WolframAlpha
- Selenium
- WebDriver (e.g., for Firefox or Chrome)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/EclipseDev2/voice-assistant-flask.git
    cd voice-assistant-flask
    ```

2. Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Flask Application

1. Start the Flask server by running the following command:

    ```bash
    python app.py
    ```

2. Open your browser and navigate to `http://127.0.0.1:5000/`.


### Frontend

The project comes with a simple HTML/JS interface to interact with the assistant. You can open `index.html` in a browser and use the input form to speak or type queries.

#### HTML:
- Allows the user to speak or type commands.
- Interacts with the Flask backend via JavaScript and AJAX to get responses.

#### JavaScript:
- Sends the voice/audio input to the backend.
- Handles responses and plays back the audio.
``
