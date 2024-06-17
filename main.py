import speech_recognition as sr
import webbrowser as wb
import pyttsx3 as pyt
import asyncio
import pyjokes
import re as regex

# Initialize the recognizer and the text-to-speech engine
r = sr.Recognizer()
engine = pyt.init()

# Function to make the assistant speak
def speak(text: str):
    rate = engine.getProperty("rate")
    engine.setProperty("rate", 130)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.say(text)
    engine.runAndWait()

# Function to handle the play command
def play(command: str):
    data = command.split(" ")
    
    # Check if the command starts with "play" or "open"
    if data[0] in ["play", "open"]:
        if data[1].lower() == "youtube" or (len(data) > 2 and data[2].lower() == "youtube"):
            wb.open("https://www.youtube.com/")
        elif data[1].lower() == "google" or (len(data) > 2 and data[2].lower() == "google"):
            wb.open("https://www.google.com")
        elif data[1].lower() == "linkedin" or (len(data) > 2 and data[2].lower() == "linkedin"):
            wb.open("https://www.linkedin.com")
        else:
            wb.open("https://youtu.be/_Heu9GAYLUI?si=UfKb7tXeyNqr6MiR")
    
    # Check if the command contains the word "joke"
    elif "joke" or "jokes" in data:
        joke = pyjokes.get_joke()
        speak(joke)
    
    # Check if the command contains the word "news"
    elif "news" in data:
        speak("Currently I have no access to news portal. In future I can.")

# Asynchronous function to listen for commands
async def listen_for_command():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=5)
            
            print("Recognizing...")
            command = r.recognize_google(audio)
            print(command)
            
            # Check if the wake word "Alexa" is spoken
            if command.lower() == "alexa":
                speak("Yes, I am here to assist you.")
                with sr.Microphone() as source:
                    print("Active...")
                    data = r.listen(source, timeout=3, phrase_time_limit=5)
                    print("Collecting...")
                
                com = r.recognize_google(data)
                com_lower = com.lower()
                
                # Use regex to match root words in the command
                pattern = r"(play|open|tell|start|begin|launch|show|display|execute|run|activate|initiate)"
                match = regex.search(pattern, com_lower)
                
                if match:
                    play(com)
                elif regex.search(r"(wait|stop|close|keep quiet|shutdown yourself|mute|shutdown)", com_lower):
                    speak("I am going to close myself. Nice talking with you, sir.")
                    break
            
            # Check for stop commands
            elif regex.search(r"(wait|stop|close|keep quiet|shutdown yourself|mute|shutdown)", command.lower()):
                speak("I am going to close myself. Nice talking with you, sir.")
                break
        
        # Handle exceptions
        except sr.UnknownValueError:
            print("Error: Could not understand the audio.")
            speak("Could not understand the audio. Please help to understand me. Tell me once again.")
        except sr.RequestError as e:
            print(f"Request error: {e}")
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected.")
            continue
        except Exception as ex:
            print(f"Unexpected error: {ex}")

# Entry point of the script
if __name__ == "__main__":
    speak("Hello, Prabhas. I am Alexa. How can I help you?")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen_for_command())
