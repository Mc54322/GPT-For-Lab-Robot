import openai
import speech_recognition as sr
import threading
import time
import sys

# Initialize the OpenAI API with your API key
openai.api_key = "Key Here"

# Global flags and variables
command_received = False
thread_stop = False
last_activity_time = time.time()

# Function to be executed when inactivity is detected
def on_inactivity():
    global command_received
    while True:
        if not command_received:
            print("Forward")
            time.sleep(2)
            if not command_received:
                print("Stop")
                time.sleep(2)
                if not command_received:
                    print("Backward")
                    time.sleep(2)
                    if not command_received:
                        print("Stop")
                        time.sleep(2)
                    else:
                        command_received = True  # Reset the flag
                        break
                else:
                    command_received = True  # Reset the flag
                    break
            else:
                command_received = True  # Reset the flag
                break
        else:
            command_received = True  # Reset the flag
            break

# Function to continuously check for inactivity
def inactivity_monitor():
    global last_activity_time, command_received, thread_stop
    while True:
        if thread_stop == True:
            break
        time.sleep(0.25)  # Check every quarter second
        elapsed_time = time.time() - last_activity_time
        if elapsed_time > 15:
            print("15 seconds of inactivity detected.")
            command_received = False
            on_inactivity()

def listen_and_recognize():
    ### The function to pick up voice commands using the Speech Regonision library
    global command_received, last_activity_time

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    while True:  # Keep listening until a valid command is received
        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)  # Listen for the first phrase and extract it into audio data

        try:
            # Recognize speech using Google Web Speech API
            command = recognizer.recognize_google(audio)
            print("You said: " + command)
            command_received = True
            last_activity_time = time.time()  # Reset the timer after action
            return command
        except sr.UnknownValueError:
           # print("Google Speech Recognition could not understand audio")
           error = True
        except sr.RequestError as e:
            #print(f"Could not request results from Google Speech Recognition service; {e}")
            error = True

# Start the inactivity check in a separate thread
inactivity_thread = threading.Thread(target=inactivity_monitor)
inactivity_thread.start()

try:
    while True:
        user_prompt = listen_and_recognize()

        # List of all the prompts from this conversation
        messages = [
            {"role": "system", "content": "You are a helper that generates pure python code based on the user's request. Your task is to output only valid python code without any extraneous text or markdown."},
            {"role": "user", "content": "This output will be executed in a part of the code that is in a never ending while loop. If a future prompt is to stop the program then output 'break' to break the loop"},
            {"role": "user", "content": "Understood. Please make sure that the only output is the python code and do not output anything else as the code will be executed. Start the code immediately and don't add any other text."},
            {"role": "user", "content": user_prompt}
        ]

        # Get the response from GPT-4 using the chat model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Edit based on what model you want to use
            messages=messages
        )

        generated_code = response.choices[0].message['content'].strip()

        # Only keep lines that don't contain markdown syntax or extraneous text.
        code_lines = [line for line in generated_code.split('\n') if not line.startswith('```')]

        # Join the lines to form the final code
        cleaned_code = '\n'.join(code_lines)

        # If the generated code is 'break', then break the loop
        if cleaned_code == 'break':
            print("Exiting...")
            thread_stop = True
            time.sleep(1)
            sys.exit()  # Exit the program

        # Run the generated code
        try:
            exec(cleaned_code)
        except Exception as e:
            print(f"An error occurred: {e}")

except KeyboardInterrupt:
    print("Exiting...")
