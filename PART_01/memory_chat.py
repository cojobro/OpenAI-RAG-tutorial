import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

conversation = [
            {"role": "system", "content": "You are a funny assistant who likes to make jokes."},
        ]

def chat(prompt):
    conversation.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = conversation
    )
    
    ai_response = response.choices[0].message.content.strip()
    conversation.append({"role": "assistant", "content": ai_response})
    
    return ai_response

if __name__ == "__main__":
    print("\nHello! I am a funny yet assistive chatbot! Press Q and hit enter to quit.\n")
    while True:
        user = input()
        if user == "Q":
            break

        response = chat(user)
        print('\n"',response,'"\n')