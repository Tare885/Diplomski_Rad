import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse
import requests
import re

# 1️⃣ Inicijalizacija TTS
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# 2️⃣ Funkcija za prepoznavanje glasa (s timeout-om 10 sekundi)
def listen_command(timeout=10):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Govorite sada...")
        try:
            audio = recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            print("⚠️ Nije bilo govora u zadanom vremenu.")
            return None
    try:
        command = recognizer.recognize_google(audio, language="hr-HR")
        print("Prepoznato:", command)
        return command
    except sr.UnknownValueError:
        print("⚠️ Nisam razumio govor.")
        return None
    except sr.RequestError as e:
        print("⚠️ Greška servisa:", e)
        return None

# 3️⃣ Funkcija za dobivanje trenutne lokacije prema IP-u
def get_current_city():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        city = data.get("city")
        print("Trenutni grad prema IP-u:", city)
        return city
    except Exception as e:
        print("⚠️ Nije moguće dobiti lokaciju:", e)
        return None

# 4️⃣ Funkcija koja priprema upit za Google Maps
def interpret_command(command):
    # Pokušava izdvojiti tip mjesta i grad
    pattern = r"(.*) u (.*)"
    match = re.search(pattern, command, re.IGNORECASE)
    if match:
        place_type = match.group(1).strip()
        city = match.group(2).strip()
    else:
        place_type = command.strip()
        city = get_current_city()  # Ako korisnik ne kaže grad, koristi trenutni grad

    search_query = f"{place_type} {city}" if city else place_type
    print("Pripremljen upit za Maps:", search_query)
    return search_query

# 5️⃣ Funkcija za otvaranje Google Maps
def open_google_maps(destination):
    query = urllib.parse.quote(destination)
    url = f"https://www.google.com/maps/search/{query}"
    webbrowser.open(url)
    speak(f"Otvaram rutu do {destination} u Google Mapsu")

# 6️⃣ Glavna funkcija (mikrofon radi samo jednom)
def main():
    command = listen_command(timeout=10)  # Mikrofon radi max 10 sekundi
    if command:
        destination = interpret_command(command)
        if destination:
            open_google_maps(destination)
    else:
        speak("Nije primljena nijedna naredba.")

if __name__ == "__main__":
    main()
