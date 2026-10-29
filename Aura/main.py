from listen import take_command
from speak import speak
from brain import ask_llm
from router import handle


def aura_response(command):
    reply = handle(command)
    if reply is not None:
        return reply
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