import openai
import time
#from RobotClass import Robot
#robot = Robot()

#THIS IS THE FIRST ITERATION WITH JUST THE INITIAL FEATURES#

# Initialize the OpenAI API with your API key
openai.api_key = "Key Here"

# Put the code in a while loop to keep the robot performing actions until the user asks to stop
while True:

    user_prompt = input("Enter your prompt: ")

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
        break

    # Print the generated code
    print(cleaned_code)

    # Run the generated code
    #try:
    #    exec(cleaned_code)
    #except Exception as e:
    #    print(f"An error occurred: {e}")