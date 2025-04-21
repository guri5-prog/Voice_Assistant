import os
import requests
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import time
import threading
from flask import Flask
import spacy
import wikipediaapi  # Import the Wikipedia API library

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Flask app for handling Spotify authorization
app = Flask(__name__)

# Variable to hold the access token
access_token = None

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the microphone as the source for input
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)  # Adjust for background noise
        try:
            # Listen for user input with a timeout
            audio = recognizer.listen(source, timeout=5)
            print("Recognizing...")  # Debugging print
            query = recognizer.recognize_google(audio)  # Recognize speech using Google Web Speech API

            # Normalize and clean up the input
            query = query.lower().strip()
            return query

        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")  # Handle timeout
            return None
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")  # Handle unrecognized speech
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")  # Handle request errors
            return None

def get_random_fact():
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        if response.status_code == 200:
            fact = response.json()["text"]
            return fact
        else:
            return "Sorry, I couldn't retrieve a fact at this moment."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def get_random_math_fact():
    try:
        response = requests.get("http://numbersapi.com/random/math?json")
        data = response.json()
        return data['text']
    except Exception as e:
        return "Sorry, I couldn't retrieve a math fact at the moment."



def chit_chat_response(user_input):
    responses = {
        "how are you": "I'm just a program, but thanks for asking! How can I assist you today?",
        "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
        "what's your name": "I'm your friendly voice assistant!",
        "hi": "Hello! How can I help you today?",
        "bye": "Goodbye! Have a great day!",
    }

    user_input = user_input.lower()  # Convert input to lowercase for matching
    return responses.get(user_input, None)  # Return None if no match is found

def tell_about_topic(topic):
    # Add more detailed information about various topics
    topics_info = {
        "climate change": "Climate change refers to long-term changes in temperatures and weather patterns. Primarily driven by human activities such as burning fossil fuels, deforestation, and industrial processes, it poses significant threats to ecosystems and human societies.",
        "artificial intelligence": "Artificial intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. AI includes learning, reasoning, and self-correction.",
        # Add more topics as needed
    }

    response = topics_info.get(topic.lower(), "I'm sorry, I don't have information on that topic.")
    say(response)

def fetch_wikipedia_summary(query):
    # Create a Wikipedia object with a user agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='MyVoiceAssistant/1.0 (https://example.com; info@example.com)'  # Custom user agent
    )

    page = wiki_wiki.page(query)

    if page.exists():
        summary = page.summary
        say(summary)
    else:
        say("Sorry, I couldn't find any information on that topic.")

def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    say(f"The current time is {current_time}.")

def tell_date():
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    say(f"The current date is {current_date}.")

# Updated Weather function with error handling
def get_weather(city):
    api_key = os.getenv("WEATHER_API")
    if not api_key:
        say("Weather API key is not set.")
        return

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={city}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if data.get("cod") == 200:
        main = data["main"]
        temperature = main["temp"]
        weather_description = data["weather"][0]["description"]
        say(f"The temperature in {city} is {temperature} degrees Celsius with {weather_description}.")
    else:
        error_message = data.get("message", "Unable to retrieve weather information.")
        say(f"Error: {error_message}. Please check the city name or try again later.")

# Lists to store reminders and alarms
reminders = []
alarms = []

# Function to check reminders
def check_reminders():
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        for reminder in reminders:
            if reminder["time"] == current_time:
                say(reminder["message"])
                reminders.remove(reminder)
        time.sleep(60)

# Function to check alarms
def check_alarms():
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        for alarm in alarms:
            if alarm == current_time:
                say("Alarm ringing!")
                alarms.remove(alarm)
        time.sleep(60)

# Function to set a reminder
def set_reminder():
    say("What time do you want to set the reminder? Please use the format HH:MM.")
    reminder_time = takeCommand()
    if reminder_time:
        say("What message do you want to remember?")
        reminder_message = takeCommand()
        if reminder_message:
            reminders.append({"time": reminder_time, "message": reminder_message})
            say(f"Reminder set for {reminder_time} with message: {reminder_message}")

# Function to set an alarm
def set_alarm():
    say("What time do you want to set the alarm? Please use the format HH:MM.")
    alarm_time = takeCommand()
    if alarm_time:
        alarms.append(alarm_time)
        say(f"Alarm set for {alarm_time}.")

def run_flask():
    app.run(port=8889, debug=False)  # Disable debug mode to avoid reloader issue

# Main loop for processing voice commands
if __name__ == '__main__':
    threading.Thread(target=check_reminders, daemon=True).start()
    threading.Thread(target=check_alarms, daemon=True).start()

    print("Starting Flask app...")
    threading.Thread(target=run_flask, daemon=True).start()  # Start Flask in a separate thread

    print("PyCharm")
    say("Hello, I am here to assist you.")

    while True:
        print("Listening...")
        query = takeCommand()

        # Check if a command was recognized
        if query:
            print(f"Recognized command: {query}")  # Debugging print
            processed_input = nlp(query)  # Processed input using spaCy

            # Print processed input for debugging
            print(f"Processed input: {processed_input}")  # Debugging print

            # Check for chit-chat responses
            chit_chat = chit_chat_response(query)
            if chit_chat:
                say(chit_chat)
                continue  # Skip to the next loop iteration

            if "give me a random fact" in query.lower() or "tell me a fact" in query.lower():
                fact = get_random_fact()
                say(fact)
                continue  # Skip to the next loop iteration

            if "give me a math fact" in query.lower() or "tell me a math fact" in query.lower():
                fact = get_random_math_fact()
                say(fact)
                continue  # Skip to the next loop iteration

            # Check for specific commands
            if "tell me about" in query.lower():
                topic = query.lower().replace("tell me about", "").strip()
                tell_about_topic(topic)

            elif "who was the first president of" in query.lower() or "who is considered as the best footballer" in query.lower():
                # Directly handle specific cases if needed
                if "who was the first president of" in query.lower():
                    fetch_wikipedia_summary("President of India")
                elif "who is considered as the best footballer" in query.lower():
                    fetch_wikipedia_summary("FIFA Ballon d'Or")

            elif "weather in" in query.lower():
                city = query.lower().replace("weather in", "").strip()
                get_weather(city)

            elif "search" in query.lower():
                search_query = query.replace("search", "").strip()
                say(f"Searching for {search_query} on Google")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")

            elif "wikipedia" in query.lower():
                search_query = query.replace("wikipedia", "").strip()
                say(f"Searching for {search_query} on Wikipedia")
                webbrowser.open(f"https://en.wikipedia.org/wiki/{search_query.replace(' ', '_')}")

            elif "time" in query.lower():
                tell_time()
            elif "date" in query.lower():
                tell_date()

            elif "set a reminder" in query.lower():
                set_reminder()

            elif "set an alarm" in query.lower():
                set_alarm()

            elif "open" in query.lower():
                website = query.lower().replace("open", "").strip()
                if not website.startswith("http://") and not website.startswith("https://"):
                    if '.' not in website:
                        website += ".com"
                say(f"Opening {website}")
                webbrowser.open(f"http://{website}")

            else:
                # Treat any other input as a general Wikipedia query
                fetch_wikipedia_summary(query)