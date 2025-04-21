# 🗣️ Voice Assistant using Python

A Python-based voice assistant that can understand voice commands, respond with speech, provide weather updates, tell random facts and math trivia, perform web searches, fetch information from Wikipedia, set alarms/reminders, and more.

## 🚀 Features

- 🎙️ Voice recognition via Google Speech API  
- 🗣️ Text-to-speech using `pyttsx3`  
- 📚 Knowledge lookup using Wikipedia  
- ☁️ Real-time weather updates via OpenWeatherMap API  
- 🔔 Set alarms and reminders  
- 🤖 Basic chit-chat and joke capabilities  
- 🔍 Google and Wikipedia search  
- 📅 Tells the current date and time  
- 🔢 Random facts and math trivia  
- 🌐 Open websites using voice command  
- 🌱 Built-in Flask server for future web integrations

## 🧰 Tech Stack

- Python 3.x  
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)  
- [pyttsx3](https://pypi.org/project/pyttsx3/)  
- [spaCy](https://spacy.io/) (`en_core_web_sm` model)  
- [Wikipedia-API](https://pypi.org/project/Wikipedia-API/)  
- [Flask](https://pypi.org/project/Flask/)  
- [Requests](https://pypi.org/project/requests/)  
- [OpenWeatherMap API](https://openweathermap.org/api)  

## 🔧 Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/voice-assistant-python.git
   cd voice-assistant-python
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Set up environment variable for weather API**
   - Get an API key from [OpenWeatherMap](https://openweathermap.org/)
   - Create a `.env` file or set the environment variable:
     ```bash
     export WEATHER_API=your_api_key_here
     ```

5. **Run the assistant**
   ```bash
   python your_script_name.py
   ```

## 🎤 How It Works

The assistant listens for your voice input, processes it using natural language processing (NLP) with spaCy, and triggers the appropriate functionality. It can respond back using speech synthesis and also interact with web services like Wikipedia and OpenWeatherMap.

### Example Voice Commands:

- “Tell me a random fact”  
- “Give me a math fact”  
- “Weather in London”  
- “Tell me about climate change”  
- “Set a reminder”  
- “Set an alarm”  
- “What’s the time?”  
- “Open YouTube”  
- “Search Python programming”  

## 🔒 Permissions

To function properly, the app requires access to your microphone and internet connection.

## 📝 TODOs

- Integrate Spotify API
- Add support for more chit-chat
- Enhance NLP parsing with intent recognition
- Add GUI interface (Tkinter or Web)

## 🤝 Contributions

Pull requests and suggestions are welcome! If you’d like to contribute, please fork the repo and submit a PR.

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

Let me know if you’d like a `requirements.txt` file or a `.env.example` as well!
