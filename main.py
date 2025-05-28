import speech_recognition as sr
import webbrowser
import requests
from gtts import gTTS
import pygame
import os
import google.generativeai as genai

# Coco - A simple AI assistant
newsapi = "<your key>"            # Your NewsAPI key
googleapi="<your key>"      # Your Google Generative AI API key

def songlink(song):
    if("wolf" in song.lower()):
        return "https://www.youtube.com/watch?v=ThCH0U6aJpU&list=PLnrGi_-oOR6wm0Vi-1OsiLiV5ePSPs9oF&index=21"
    elif ("Faded" in song.lower()):
        return "https://www.youtube.com/watch?v=60ItHLz5WEA&pp=ygUHZmFkZWQgbGF0b24%3D"
    elif ("skyfall" in song.lower()):
        return "https://www.youtube.com/watch?v=DeumyOzKqgI&pp=ygUHc2t5ZmFsbA%3D%3D"
    elif ("stealth" in song.lower()):
        return "https://www.youtube.com/watch?v=U47Tr9BB_wE"
    elif ("march" in song.lower()):
        return "https://www.youtube.com/watch?v=Xqeq4b5u_Xw"
    


def speak(text): #Function to convert text to speech and play it
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 


def aiProcess(command):

    genai.configure(api_key=googleapi)  # Configure the API with your specific key

    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

    response = model.generate_content(command) # Use the model to generate content based on the command

    return response.text


def processCommand(c):
    if "open google" in c.lower():      # Opens Google
        print("Opening Google...")
        webbrowser.open("https://google.com")
    elif "open instagram" in c.lower():  # Opens Instagram
        print("Opening Instagram...")
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():  # Opens LinkedIn
        print("Opening LinkedIn...")
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():   # Opens YouTube
        print("Opening YouTube...")
        webbrowser.open("https://youtube.com")
    elif "open leetcode" in c.lower():  # Opens LeetCode
        print("Opening LeetCode...")
        webbrowser.open("https://leetcode.com")
    elif "open github" in c.lower():    # Opens GitHub
        print("Opening GitHub...")
        webbrowser.open("https://github.com")
    elif c.lower().startswith("play"):
        print("Playing music...")
        song = c.lower().split(" ")[1] #command=play {song name}
        webbrowser.open(songlink(song)) # Opens the song link 

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}") # Fetch top headlines from NewsAPI
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # speaks the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let Gemini handle the request
        output = aiProcess(c)
        speak(output) 


if __name__ == "__main__":
    
    speak("Initializing Coco...")
    while True:
        # Listen for the wake word "Coco"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "coco"):   # If the wake word is recognized
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Coco Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print("Command received: {0}".format(command))
                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))


