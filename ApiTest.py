import openai

# Initialize the OpenAI API with your API key
openai.api_key = "Key Here"

user_prompt = input("Enter your prompt: ")

# List of all the prompts from this conversation
messages = [
    {"role": "system", "content": "You are a helper that generates pure python code based on the user's request. Your task is to output only valid python code without any extraneous text or markdown."},
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

# Run the generated code
try:
    exec(cleaned_code)
except Exception as e:
    print(f"An error occurred: {e}")