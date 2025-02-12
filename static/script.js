document.getElementById("submit-text").addEventListener("click", function () {
    let userInput = document.getElementById("user-input").value;
    if (userInput) {
        sendTextToFlask(userInput);
    } else {
        alert("Please enter a question.");
    }
});

document.getElementById("record-audio").addEventListener("click", function () {
    recordAudioAndSendToFlask();
});

function sendTextToFlask(text) {
    fetch('http://127.0.0.1:5000/process_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.blob())
    .then(blob => {
        const audioUrl = URL.createObjectURL(blob);
        const audioElement = new Audio(audioUrl);
        audioElement.play();
    })
    .catch(error => {
        console.log('Error:', error);
        document.getElementById("assistant-response").innerText = "Something went wrong.";
    });
}

function recordAudioAndSendToFlask() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(function (stream) {
                const recorder = new MediaRecorder(stream);
                recorder.start();

                recorder.ondataavailable = function (event) {
                    const audioBlob = event.data;
                    const formData = new FormData();
                    formData.append("audio", audioBlob, "user_audio.wav");

                    fetch('http://127.0.0.1:5000/get_audio', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById("assistant-response").innerText = "Assistant: " + data.text;
                    })
                    .catch(error => {
                        console.log('Error:', error);
                        document.getElementById("assistant-response").innerText = "Error processing your audio.";
                    });
                };

                recorder.onstop = function () {
                    stream.getTracks().forEach(track => track.stop());
                };

                setTimeout(() => {
                    recorder.stop();
                }, 5000); // Stop recording after 5 seconds
            })
            .catch(function (error) {
                console.log("Error accessing microphone: ", error);
            });
    } else {
        alert("Audio recording is not supported by your browser.");
    }
}
