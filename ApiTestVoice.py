import openai
import speech_recognition as sr

def listen_and_recognize():
    ### The function to pick up voice commands using the Speech Regonision library
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening for a command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for the first phrase and extract it into audio data

    try:
        # Recognize speech using Google Web Speech API
        command = recognizer.recognize_google(audio)
        print("You said: " + command)
        return command
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Initialize the OpenAI API with your API key
openai.api_key = "Key Here"

# Put the code in a while loop to keep the robot performing actions until the user asks to stop
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
        break

    # Run the generated code
    try:
        exec(cleaned_code)
    except Exception as e:
        print(f"An error occurred: {e}")