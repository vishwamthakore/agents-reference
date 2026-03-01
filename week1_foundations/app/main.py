import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from tools import tools, handle_tool_calls
from prompts import get_system_prompt

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)



def chat(message, history=[]):
    system_prompt = get_system_prompt()
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    done = False
    while not done:
        # We can add a for loop here to limit number of llm calls
        # This is the call to the LLM - see that we pass in the tools json

        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)

        finish_reason = response.choices[0].finish_reason
        
        # If the LLM wants to call a tool, we do that!
         
        if finish_reason=="tool_calls":
            message = response.choices[0].message
            tool_calls = message.tool_calls
            results = handle_tool_calls(tool_calls)
            messages.append(message)
            messages.extend(results)
        else:
            done = True
    return response.choices[0].message.content


gr.ChatInterface(chat).launch()
