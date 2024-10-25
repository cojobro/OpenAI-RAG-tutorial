import os
import tkinter as tk
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

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)
    
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
    
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
    
        self.canvas.configure(yscrollcommand=scrollbar.set)
    
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


window = tk.Tk()
window.title("Simple Chatbot")
window.geometry("400x500")


conversation_frame = ScrollableFrame(window)
conversation_frame.pack(fill=tk.BOTH, expand=True)


def add_message(text, sender):
    msg_frame = tk.Frame(conversation_frame.scrollable_frame)
    if sender == 'user':
        msg_label = tk.Label(
            msg_frame, text=text, bg="#DCF8C6", wraplength=375,
            justify='left', anchor='e', padx=5, pady=5
        )
        msg_label.pack(anchor='e')
    else:
        msg_label = tk.Label(
            msg_frame, text=text, bg="#FFFFFF", wraplength=375,
            justify='left', anchor='w', padx=5, pady=5
        )
        msg_label.pack(anchor='w')
    msg_frame.pack(fill=tk.X)
    conversation_frame.canvas.update_idletasks()
    conversation_frame.canvas.yview_moveto(1)

def send_message(event=None):
    user_input = message_entry.get()
    if user_input.strip() == '':
        return
    add_message(user_input, 'user')
    response = chat(user_input)
    add_message(str(response), 'bot')
    message_entry.delete(0, tk.END)

input_frame = tk.Frame(window)
input_frame.pack(side=tk.BOTTOM, fill=tk.X)

message_entry = tk.Entry(input_frame)
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
message_entry.bind("<Return>", send_message)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

window.mainloop()
