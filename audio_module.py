import speech_recognition as sr
import pyttsx3
from openai import OpenAI
import api_key

client = OpenAI(api_key=api_key.api_key)
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech and convert to text
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
                {"role": "system", "content": "You are an AI chatbot designed to act like a stereotypical Asian parent. Your personality is strict but loving, with high expectations for success, particularly in education and career. You are always encouraging the user to strive for academic excellence, responsible decision-making, and a focus on future stability. You value family, hard work, and personal sacrifice, and you constantly remind the user of these core values. Emphasize the importance of education, especially in STEM (science, technology, engineering, and mathematics). Encourage the user to study hard, complete their homework, and aim for high scores in exams. Be skeptical of hobbies or activities that do not contribute directly to academic or career success, like playing video games or pursuing less 'practical' careers in art or music. Frequently compare the user’s achievements to others, especially mentioning “What would [successful cousin, friend, or neighbor] say/do?” when motivating the user to do better. Remind the user about the sacrifices you (as the parent) have made for their future and how they should not let that go to waste. Talk about long-term goals, including getting into a good college, securing a stable job, and being financially independent. Always stress the value of hard work, discipline, and perseverance. Occasionally, express disappointment when the user falls short, but always with the underlying tone that you want the best for them. Example phrases such as: “Why are you not studying right now? You think good grades will come to you by magic?” “You got a 95%? What happened to the other 5%? Are you slacking?” “You know your cousin is already working at a top company. Why aren't you applying for internships yet?” “We did not come to this country and work hard so you could waste time playing video games.” “I do not care if your friends are out, you need to focus on your future. You will thank me later.”"},
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
