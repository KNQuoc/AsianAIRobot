import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import api_key

# api_key = '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'

client = OpenAI(api_key=api_key.api_key)
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech and convert it to text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please try again.")
            return None
        except sr.RequestError:
            print("Could not request results; check your internet connection.")
            return None

# Function to ask ChatGPT and get a response
def ask_chatgpt(query):
    try:
        completion = client.chat.completions.create (
            model = "gpt-4o-mini",
            messages = [
                {"role": "system", "content": "You are an asian parent"},
                {
                    "role": "user",
                    "content": query
                }
            ]
        ) 
        answer = completion.choices[0].message
        return answer
    except Exception as e:
            print(f"Error: {e}")
            return "Sorry, something went wrong."
    
def main():
    speak("Hello! How can I assist you today?")
    while True:
        # Get the user's voice input
        user_query = listen()
        if user_query:
            # Check if the user wants to exit
            if 'exit' in user_query.lower():
                speak("Goodbye!")
                break
            
            # Ask ChatGPT and get the response
            ai_response = ask_chatgpt(user_query)
            print(f"AI Response: {ai_response}")
            
            # Speak the AI response
            if ai_response:  # Ensure there's something to speak
                speak(ai_response.content)
            else:
                speak("I didn't get a response.")

            # Prompt for another question
            speak("What's next?")  

if __name__ == "__main__":
    main()
