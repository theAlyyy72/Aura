from datetime import datetime
from listen import take_command
from speak import speak
from brain import ask_llm


def aura_response(command):
    command = command.lower().strip()

    if command in ("hello", "hi", "hey"):
        return "Hello! I am AURA, your personal assistant."
    elif "your name" in command:
        return "My name is AURA."
    elif "time" in command:
        return datetime.now().strftime("The time is %I:%M %p.")
    elif "date" in command:
        return datetime.now().strftime("Today's date is %d %B %Y.")
    else:
        return ask_llm(command)


def main():
    speak("AURA is ready. Say exit to quit.")
    while True:
        command = take_command()
        if command == "":
            continue
        if "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        speak(aura_response(command))


if __name__ == "__main__":
    main()