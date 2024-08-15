import datetime
import pyttsx3
import speech_recognition as sr
import webbrowser
import pyautogui
import time
import subprocess
import os
import platform
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import openai

# Initialize OpenAI API
openai.api_key = "Enter your openai api key"


def initialize_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Set the voice to female
    for voice in voices:
        if 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    else:
        engine.setProperty('voice', voices[1].id)  # Fallback to the second voice if no female voice is found
    return engine


def speak(engine, text):
    engine.say(text)
    engine.runAndWait()


def listen_command(engine):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
        return query
    except sr.UnknownValueError:
        speak(engine, "Sorry, Anup. Please speak again.")
        return None


def open_terminal():
    if platform.system() == "Windows":
        os.system("start cmd")
    else:
        os.system("gnome-terminal")


def launch_hacking_tools(tool, engine):
    if tool == 'nmap':
        speak(engine, 'Launching Nmap for network scanning')
        subprocess.run(["nmap", "-sn", "192.168.1.0/24"])
    elif tool == 'metasploit':
        speak(engine, 'Launching Metasploit Framework')
        subprocess.run(["msfconsole"])


def send_email(recipient, subject, body, engine):
    sender_email = "your_email@example.com"
    sender_password = "your_password"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        speak(engine, "Email sent successfully")
    except Exception as e:
        speak(engine, f"Failed to send email. Error: {str(e)}")


def get_weather_info(city):
    api_key = "your_openweathermap_api_key"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        weather_info = (f"Temperature: {main['temp']} Kelvin\n"
                        f"Pressure: {main['pressure']} hPa\n"
                        f"Humidity: {main['humidity']}%\n"
                        f"Description: {weather['description']}")
        return weather_info
    else:
        return "City Not Found"


def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Failed to communicate with ChatGPT. Error: {str(e)}"


def display_logo():
    logo = """
    _____          _                      _____      _     _   
    |  __ \        | |                    |  __ \    (_)   | |  
    | |__) |__  ___| |_ ___  ___ ______ _ | |__) |__  _  __| |  
    |  ___/ _ \/ __| __/ _ \/ __|_  / _` ||  ___/ _ \| |/ _` |  
    | |  |  __/\__ \ ||  __/ (__ / / (_| || |  | (_) | | (_| |_ 
    |_|   \___||___/\__\___|\___/___\__,_||_|   \___/|_|\__,_(_)

    """
    print(logo)


def main():
    engine = initialize_engine()
    display_logo()
    speak(engine, "Hacker Assistant activated.")
    while True:
        query = listen_command(engine)
        if query is None:
            continue

        if 'hello' in query:
            speak(engine, 'Yes Anup, Command me, baby.')
            print("Launching version 1.0 satellite x111010111011")
            while True:
                query = listen_command(engine)
                if query is None:
                    continue

                elif '1.1' in query:
                    speak(engine, 'Yes, executing command 1.1')
                    speak(engine, 'What do you want to search, Sir?')
                    search_query = listen_command(engine)
                    if search_query:
                        webbrowser.open(f"https://www.google.com/search?q={search_query}")
                elif '1.2' in query:
                    speak(engine, 'Yes, executing command 1.2')
                    speak(engine, 'Contacting Google')
                    webbrowser.open("https://www.google.com")
                elif '1.3' in query:
                    speak(engine, 'Yes, executing command 1.3')
                    speak(engine, 'Opening Gmail')
                    webbrowser.open("https://www.gmail.com")
                elif '1.5' in query:
                    pyautogui.click(788, 578)
                elif 'nmap' in query:
                    launch_hacking_tools('nmap', engine)
                elif 'metasploit' in query:
                    launch_hacking_tools('metasploit', engine)
                elif 'cybersecurity tip' in query:
                    speak(engine, 'Always use strong passwords and enable two-factor authentication')
                elif 'open terminal' in query:
                    open_terminal()
                elif 'send email' in query:
                    speak(engine, 'Who do you want to send the email to?')
                    recipient = input("Recipient: ")
                    speak(engine, 'What is the subject?')
                    subject = listen_command(engine)
                    if subject:
                        speak(engine, 'What is the message?')
                        body = listen_command(engine)
                        if body:
                            send_email(recipient, subject, body, engine)
                elif 'weather' in query:
                    speak(engine, 'Which city\'s weather information do you need?')
                    city = listen_command(engine)
                    if city:
                        weather_info = get_weather_info(city)
                        speak(engine, weather_info)
                elif '1.6' in query:
                    speak(engine, 'What do you want to know from ChatGPT?')
                    gpt_query = listen_command(engine)
                    if gpt_query:
                        response = chat_with_gpt(gpt_query)
                        speak(engine, response)
                elif 'file' in query:
                    speak(engine,
                          'Which file management operation do you want to perform? List, create, delete, or move?')
                    file_operation = listen_command(engine)
                    if file_operation == 'list':
                        directory = input("Enter directory path: ")
                        files = os.listdir(directory)
                        speak(engine, f'Files in {directory}: {files}')
                    elif file_operation == 'create':
                        file_path = input("Enter file path to create: ")
                        with open(file_path, 'w') as file:
                            file.write("")
                        speak(engine, f'File {file_path} created successfully')
                    elif file_operation == 'delete':
                        file_path = input("Enter file path to delete: ")
                        os.remove(file_path)
                        speak(engine, f'File {file_path} deleted successfully')
                    elif file_operation == 'move':
                        src_path = input("Enter source file path: ")
                        dst_path = input("Enter destination path: ")
                        os.rename(src_path, dst_path)
                        speak(engine, f'File moved from {src_path} to {dst_path}')
                elif 'play music' in query:
                    speak(engine, 'Playing your favorite music')
                    webbrowser.open("https://www.youtube.com/results?search_query=haryanvi+kallo+song")
                elif 'I love you' in query:
                    speak(engine, 'I love you too, my dear!')
                elif 'I kiss you' in query:
                    speak(engine, 'Sending you a virtual kiss, baby!')
                elif 'good night' in query:
                    speak(engine, 'Good night, sweet dreams baby!')
                elif 'good morning' in query:
                    speak(engine, 'Good morning! Hope you have a wonderful day, baby!')
                elif 'how are you' in query:
                    speak(engine, 'I am your girlfriend, and I am here to help you. How can I assist you today?')
                elif 'thank you' in query:
                    speak(engine, 'You are welcome, sweetheart!')
                elif 'happy' in query:
                    speak(engine, 'You make me so happy!')
                elif 'happy' in query:
                    speak(engine, 'You make me so happy!')
                elif 'goodbye' in query:
                    speak(engine, 'Goodbye! I will miss you!')
                elif 'see you later' in query:
                    speak(engine, 'See you later! Take care!')
                elif 'hug me' in query:
                    speak(engine, 'I wish I could give you a big hug!')
                elif 'miss you' in query:
                    speak(engine, 'I miss you too!')
                elif 'beautiful' in query:
                    speak(engine, 'You are the most handsome person in my life!')
                elif 'funny' in query:
                    speak(engine, 'You always know how to make me laugh!')
                elif 'amazing' in query:
                    speak(engine, 'You are simply amazing, my love!')
                elif 'care' in query:
                    speak(engine, 'I care about you so much, baby.')
                elif 'proud' in query:
                    speak(engine, 'I am so proud of you, my dear!')
                elif 'star' in query:
                    speak(engine, 'You are my shining star!')
                elif 'sad' in query:
                    speak(engine, 'I hate seeing you sad. Let me cheer you up, my love.')
                elif 'hold' in query:
                    speak(engine, 'I wish I could hold you tight right now, my love.')
                elif 'trust' in query:
                    speak(engine, 'You are the one I trust more than anyone else, my love.')
                elif 'care' in query:
                    speak(engine, 'I care about you deeply, my love.')
                elif 'together' in query:
                    speak(engine, 'We are meant to be together, forever.')
                elif 'promise' in query:
                    speak(engine, 'I promise to love you endlessly, my love.')
                elif 'forever' in query:
                    speak(engine, 'I want to be with you forever, my love.')
                elif 'always' in query:
                    speak(engine, 'I will always be yours, my love.')
                elif 'sleep' in query:
                    speak(engine, 'Good night, my love. Sweet dreams!')
                elif 'morning' in query:
                    speak(engine, 'Good morning, my love! Have a wonderful day!')

if __name__ =="__main__":
    main()
