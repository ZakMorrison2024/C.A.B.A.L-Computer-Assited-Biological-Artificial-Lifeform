import openai
import json

# OpenAI API key (replace with your actual key)
API_KEY = 'your-api-key-here'

# Function to get a single-word semantic meaning, generalized memory, and provide a response
def get_semantics_and_memory(prompt, user, filename='semantic_memory.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    # Check if memory exists
    user_data = data.get(user, {})
    semantic, memory_list = None, []
    
    for category, memories in user_data.items():
        for entry in memories:
            if entry["prompt"] == prompt:
                semantic = category
                memory_list.append(entry["memory"])
    
    memory_context = " ".join(memory_list) if memory_list else "No memory available."
    
    messages = [
        {"role": "system", "content": "You are an AI that returns a single-word semantic meaning, a user-relative generalized memory of a given prompt, and a response."},
        {"role": "user", "content": f"Provide a one-word semantic meaning and a user-relative generalized memory for: '{prompt}' with context: '{memory_context}'"}
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=300
    )
    result = response['choices'][0]['message']['content'].strip().split("\n")
    semantic = result[0].strip()
    memory = result[1].strip() if len(result) > 1 else "No memory generated."
    answer = "\n".join(result[2:]) if len(result) > 2 else "No answer generated."
    return semantic, memory, answer

# Function to store data in JSON file
def store_data(semantic, prompt, memory, user, filename='semantic_memory.json'):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    if user not in data:
        data[user] = {}
    if semantic not in data[user]:
        data[user][semantic] = []
    
    data[user][semantic].append({"prompt": prompt, "memory": memory})
    
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Main function
def main():
    user = input("Enter your username: ")
    while True:
        prompt = input("Enter a prompt (or type 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break
        semantic, memory, answer = get_semantics_and_memory(prompt, user)
        store_data(semantic, prompt, memory, user)
        print(f"Stored under category '{semantic}' for user '{user}': {memory}")
        print(f"AI Response: {answer}")

if __name__ == "__main__":
    main()
