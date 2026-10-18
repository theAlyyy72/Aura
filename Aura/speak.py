import subprocess


def speak(text):
    print("AURA:", text)
    subprocess.run(["say", "-v", "Samantha", text])