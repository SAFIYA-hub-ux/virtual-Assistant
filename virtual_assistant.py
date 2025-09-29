# -*- coding: utf-8 -*-
"""virtual assistant"""

import pyttsx3  # For text-to-speech
import speech_recognition as sr  # For speech-to-text
import datetime  # For current time
import webbrowser  # To open websites
import pyjokes  # For telling jokes
import wikipedia  # For fetching summaries from Wikipedia
import matplotlib.pyplot as plt  # For plotting accuracy chart
import re  # For regex

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change to voices[1] for female voice

# Function to make the assistant speak
def talk(text):
    print("Chintu:", text)
    engine.say(text)
    engine.runAndWait()

# Function to take voice input
def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.pause_threshold = 1
        audio = listener.listen(source)

    try:
        command = listener.recognize_google(audio)
        print("Heard:", command)
        return command.lower()
    except sr.UnknownValueError:
        talk("Sorry, I didn't catch that.")
    except sr.RequestError:
        talk("Sorry, there was an error with the recognition service.")
    return ""

# Function to get route using Google Maps
def get_route(command):
    match = re.search(r'route from (.*?) to (.*)', command)
    if match:
        source = match.group(1).strip()
        destination = match.group(2).strip()

        talk(f"Getting the route from {source} to {destination}")
        route_url = f"https://www.google.com/maps/dir/{source}/{destination}"
        webbrowser.open(route_url)
        return True
    else:
        talk("Please say the route like 'route from Hyderabad to Chennai'")
        return False

# Mock location (placeholder)
def get_location():
    return "India"

# Performance tracking
total_commands = 0
successful_commands = 0

# Main assistant function
def run_chintu():
    global total_commands, successful_commands
    command = take_command()
    if not command or 'chintu' not in command:
        return True

    total_commands += 1
    success = False
    command = command.replace('chintu', '').strip()

    # Exit condition
    if any(word in command for word in ['bye', 'thank', 'exit', 'quit', 'stop', 'goodbye']):
        talk("You're welcome! Goodbye!")
        successful_commands += 1
        return False

    # Route finder
    elif 'route' in command:
        success = get_route(command)

    # Play song
    elif 'play' in command:
        song = command.replace('play', '').strip()
        talk('Playing ' + song)
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        success = True

    # Current time
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
        success = True

    # Wikipedia search
    elif 'who is' in command or 'what is' in command:
        topic = command.replace('who is', '').replace('what is', '').strip()
        try:
            info = wikipedia.summary(topic, sentences=1)
            talk(info)
            success = True
        except:
            talk("Sorry, I couldn't find any information about that.")

    # Jokes
    elif 'joke' in command:
        talk(pyjokes.get_joke())
        success = True

    # Fun response
    elif 'are you single' in command:
        talk('I am in a relationship with Wi-Fi.')
        success = True

    # Mock location
    elif 'location' in command:
        location = get_location()
        talk(f"You are currently in {location}")
        success = True

    # Travel suggestion / fallback
    else:
        try:
            place = command.strip()
            if len(place.split()) <= 3:
                talk(f"Fetching information about {place}")
                summary = wikipedia.summary(place, sentences=2)
                talk(summary)
                search_url = f"https://www.google.com/search?q=best+time+to+visit+{place}+places+to+visit"
                webbrowser.open(search_url)
                talk(f"I've also opened a page with travel tips and top places to visit in {place}")
                success = True
            else:
                talk("Please say the command again.")
        except:
            talk("Sorry, I couldn't find detailed information about that place.")

    if success:
        successful_commands += 1

    return True

# Show performance bar chart
def show_accuracy_chart():
    if total_commands == 0:
        accuracy = 0
    else:
        accuracy = (successful_commands / total_commands) * 100

    print(f"\nTotal Commands: {total_commands}")
    print(f"Successful Commands: {successful_commands}")

    results = ['Successful', 'Failed']
    counts = [successful_commands, total_commands - successful_commands]
    colors = ['green', 'red']

    plt.bar(results, counts, color=colors)
    plt.title(f'Chintu Accuracy: {accuracy:.2f}%')
    plt.xlabel('Result')
    plt.ylabel('Number of Commands')
    plt.show()

# Main loop
if __name__ == '__main__':
    while run_chintu():
        pass
    show_accuracy_chart()
