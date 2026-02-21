import openai
import speech_recognition as sr
import threading
import time
import sys
from RobotClass import Robot
robot = Robot()

# Initialize the OpenAI API with your API key
openai.api_key = "Key Here"

# Global flags and variables
command_received = False
thread_stop = False
last_activity_time = time.time()

# Function to be executed when inactivity is detected
def idle_state_1():
    global command_received
    while True:
        if not command_received:
            print("Forward")
            robot.forward(0.2)
            time.sleep(2)
            robot.stop()
            if not command_received:
                print("Stop")
                time.sleep(2)
                if not command_received:
                    print("Backward")
                    robot.backward(0.2)
                    time.sleep(2)
                    robot.stop()
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
        if elapsed_time > 30:
            print("30 seconds of inactivity detected.")
            command_received = False
            idle_state_1()

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

# Put the code in a while loop to keep the robot performing actions until the user asks to stop
try:
    while True:
        user_prompt = listen_and_recognize()

        # List of all the prompts from this conversation
        messages = [
            {"role": "system", "content": "You are a helper that generates pure python code based on the user's request. Your task is to output only valid python code without any extraneous text or markdown. The python code is specifically used to control a robot, which uses custom code. This code will be given in a moment."},
            {"role": "user", "content": "Understood. Please make sure that the only output is the python code that works on the robot and do not output anything else as the code will be executed. Start the code immediately and don't add any other text."},
            {"role": "user", "content": """Here is the code for the robot, please use this to create more commands for the robot to execute. Only use the methods in this class, not anything else to control the robot

                RobotClass.py:

                import traitlets
                import time
                from traitlets.config.configurable import SingletonConfigurable
                from drivers import PCA9685, Motor

                class Robot(SingletonConfigurable):
                
                    front_left_motor = traitlets.Instance(Motor)
                    front_right_motor = traitlets.Instance(Motor)
                    back_left_motor = traitlets.Instance(Motor)
                    back_right_motor = traitlets.Instance(Motor)

                    # config
                    front_left_motor_channel = traitlets.Integer(default_value=1).tag(config=True)
                    front_left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
                    front_right_motor_channel = traitlets.Integer(default_value=2).tag(config=True)
                    front_right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
                    back_left_motor_channel = traitlets.Integer(default_value=3).tag(config=True)
                    back_left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
                    back_right_motor_channel = traitlets.Integer(default_value=4).tag(config=True)
                    back_right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
                
                    def __init__(self, *args, **kwargs):
                        super(Robot, self).__init__(*args, **kwargs)
                        self.left_motor_driver = PCA9685(0x41, debug=False)
                        self.right_motor_driver = PCA9685(0x40, debug=False)
                        self.front_left_motor = Motor(self.left_motor_driver, channel=self.front_left_motor_channel, alpha=self.front_left_motor_alpha)
                        self.front_right_motor = Motor(self.right_motor_driver, channel=self.front_right_motor_channel, alpha=self.front_right_motor_alpha)
                        self.back_left_motor = Motor(self.left_motor_driver, channel=self.back_left_motor_channel, alpha=self.back_left_motor_alpha)
                        self.back_right_motor = Motor(self.right_motor_driver, channel=self.back_right_motor_channel, alpha=self.back_right_motor_alpha)
                    
                    def set_motors(self, front_left_speed, front_right_speed, back_left_speed, back_right_speed):
                        self.front_left_motor.value = front_left_speed
                        self.front_right_motor.value = front_right_speed
                        self.back_left_motor.value = back_left_speed
                        self.back_right_motor.value = back_right_speed
                    
                    def forward(self, speed=1.0):
                        self.front_left_motor.value = speed
                        self.front_right_motor.value = speed
                        self.back_left_motor.value = speed
                        self.back_right_motor.value = speed

                    def backward(self, speed=1.0):
                        self.front_left_motor.value = -speed
                        self.front_right_motor.value = -speed
                        self.back_left_motor.value = -speed
                        self.back_right_motor.value = -speed

                    def left(self, speed=1.0):
                        self.front_left_motor.value = -speed
                        self.front_right_motor.value = speed
                        self.back_left_motor.value = -speed
                        self.back_right_motor.value = speed

                    def right(self, speed=1.0):
                        self.front_left_motor.value = speed
                        self.front_right_motor.value = -speed
                        self.back_left_motor.value = speed
                        self.back_right_motor.value = -speed

                    def stop(self):
                        self.front_left_motor.value = 0
                        self.front_right_motor.value = 0
                        self.back_left_motor.value = 0
                        self.back_right_motor.value = 0
                
                    def forward_left(self, speed=1.0):
                        self.front_left_motor.value = speed / 3
                        self.front_right_motor.value = speed
                        self.back_left_motor.value = speed / 3
                        self.back_right_motor.value = speed
                        
                    def forward_right(self, speed=1.0):
                        self.front_left_motor.value = speed
                        self.front_right_motor.value = speed / 3
                        self.back_left_motor.value = speed
                        self.back_right_motor.value = speed / 3

                    def backward_left(self, speed=1.0):
                        self.front_left_motor.value = -speed / 3
                        self.front_right_motor.value = -speed
                        self.back_left_motor.value = -speed / 3
                        self.back_right_motor.value = -speed
                        
                    def backward_right(self, speed=1.0):
                        self.front_left_motor.value = -speed
                        self.front_right_motor.value = -speed / 3
                        self.back_left_motor.value = -speed
                        self.back_right_motor.value = -speed / 3"""},
            {"role": "user", "content": "This output will be executed in a part of the code that is in a never ending while loop. If a future prompt is to stop the program then output 'break' to break the loop and if the future prompt is related to stopping the robot then use the robot.stop() method"},
            {"role": "user", "content": "If the future prompts do not ask to stop the program, then end the code with 'last_activity_time = time.time()'"},
            {"role": "user", "content": "All libraries are already imported, so you will not need to do that"},
            {"role": "user", "content": "Make the robot move slowly by default, only increase speed if specifically asked"},
            {"role": "user", "content": "Make sure that the code generated always stops unless asked otherwise"},
            {"role": "user", "content": "Make sure that all code that you generate is executable and does not have any placeholders"},
            {"role": "user", "content": "You should not explain anything you have generated"},
            {"role": "user", "content": "Please generate nothing but python code as non code related output will bug out the execution of the code due to the output being executed in the exec function in python"},
            {"role": "user", "content": f"The user prompt is: '{user_prompt}'."}
        ]

        # Get the response from GPT-4 using the chat model
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",  # Edit based on what model you want to use
            messages = messages
        )

        generated_code = response.choices[0].message['content'].strip()
        print(generated_code)

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

        # Print the generated code
        print(cleaned_code)

        # Run the generated code
        try:
            exec(cleaned_code)
        except Exception as e:
            print(f"An error occurred: {e}")

except KeyboardInterrupt:
    print("Exiting...")
