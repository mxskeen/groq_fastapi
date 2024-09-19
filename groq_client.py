# install (pip install fastapi pydantic groq)
from fastapi import FastAPI
from pydantic import BaseModel
import os
from groq import Groq

app = FastAPI()

client = Groq(api_key="your_grok_api_key")

# Store conversation history
conversation_history = []

class Message(BaseModel):
    content: str


@app.post("/process")
async def process_message(message: Message):
    global conversation_history

    # Append the new user message to the conversation history
    conversation_history.append({"role": "user", "content": message.content})

    # Create the Groq API request with the conversation history
    chat_completion = client.chat.completions.create(
        messages=conversation_history,
        model="llama3-8b-8192",
    )

    # Get the response from Groq
    response = chat_completion.choices[0].message.content

    # Append the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": response})

    return {"response": response}
