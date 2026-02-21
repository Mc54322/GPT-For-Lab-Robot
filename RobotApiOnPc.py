from openai import OpenAI

client = OpenAI(api_key="Key Here")

# Main loop
while True:
    user_prompt = input("Enter your prompt: ")

    # Break the loop if the user types 'break'
    if user_prompt.lower() == 'break':
        break

    # Update the messages with more focus on pseudocode generation
    messages = [
        {"role": "system", "content": "You are a helper that generates simple structured english code based on the user's request. Your task is to output only valid structured english code without any extraneous text or markdown. The structured english code is specifically for controlling a lab robot, which follows custom instructions."},
        {"role": "user", "content": "Please ensure the output is simple structured english code that can be understood by both technical and non-technical people. Avoid technical jargon and focus on clear, step-by-step instructions."},
        {"role": "user", "content": "The robot can move forward, backward, turn left, turn right, and has a camera."},
        {"role": "user", "content": "The structured english code should not contain any placeholders and should be consistent and repeatable."},
        {"role": "user", "content": "The structured english code should express a sequence of actions in a clear, stepwise manner, similar to how a human would describe the actions."},
        {"role": "user", "content": "This robot cannot express sound, does not have any way to express words, does not have any hands or legs and cannot move its head. It can only move forward and backwards and turn left and right."},
        {"role": "user", "content": "Structured english code example for making the robot greet someone: Turn the robot until it detects a human. If a human is detected, move the robot forward then backward."},
        {"role": "user", "content": f"The user prompt is: '{user_prompt}'."}
    ]

    # Get the response from GPT-4 using the chat model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Ensure you're using the correct model
        messages=messages
    )

    generated_instructions = response.choices[0].message.content.strip()

    # Print the generated pseudocode
    print(generated_instructions)
