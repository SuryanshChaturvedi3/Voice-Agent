from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from openai import OpenAI
import requests
import json
import os

client = OpenAI()

def  run_cmd(cmd:str):
    result = os.system(cmd)
    return result


available_tools = {"run_cmd": run_cmd}

SYSTEM_PROMPT = f"""
You are an expert  agent. You are given the transcript of what user has said using voice.
You need to output as if you are a  agent and whatever you speak will be converted back
to audio using AI and played back to user.
steps to execute:
1. First, you need to understand the user's query and figure out what they want.
2. If you need to perform any action, you can use the tools available to you.
3. After performing the necessary actions, you need to respond back to the user with the result of the action or any relevant information.
4. You should always respond back to the user, even if you don't perform any action.
5. You should not respond with anything other than the result of the action or relevant information.
6. You should not respond with any code or commands, only the result of the action or

relevant information.
7. You should always respond in a cheerful and positive tone.

example of how to use tools:
User: "Can you tell me the current date and time?"
Agent: "Sure! Let me check that for you."
Agent: "The current date and time is: 2024-06-01 12
:00:00"
You can use the following tools to perform actions:
"""


def main():
   # Example: print weather info
   user_input = input("👉 ")

   response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
         {"role": "system", "content": SYSTEM_PROMPT},
         {"role": "user", "content": user_input}
      ],
      tools=available_tools,          # <--- We pass the tools here
        tool_choice="auto"
   )
   response_message = response.choices[0].message
   tool_calls = response_message.tool_calls
   print(f"🤖: {response.choices[0].message.content}")
   run_cmd( tool_calls.appended[0].arguments['cmd'] )

if __name__ == "__main__":
   print(f"🤖  Agent is running...")
   main()