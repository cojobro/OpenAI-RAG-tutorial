import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def chat(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a funny assistant who likes to make jokes."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("\nHello! I am a funny yet assistive chatbot! Press Q and hit enter to quit.\n")
    while True:
        user = input()
        if user == "Q":
            break

        response = chat(user)
        print('\n"',response,'"\n')