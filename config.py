# -*- coding: utf-8 -*-

import time
from openai import AzureOpenAI
from secret import *
from functions import *
from utils import *

client = AzureOpenAI(api_key=gpt4o_ak, api_version="2024-05-01-preview", azure_endpoint=gpt4o_ep)

# 1. 创建Agent
assistant = None
num_retries = 3
for _ in range(num_retries):
    try:
        assistant = client.beta.assistants.create(
            model="GPT4oChat",
            temperature=0,
            name="Weather Bot",
            instructions="You are a e-commerce bot. Use the provided functions to answer questions.",
            tools=[{"type": "function", "function": get_order},
                   {"type": "function", "function": get_item},
                   {"type": "function", "function": recommend_items},
                   {"type": "function", "function": transfer_to_human},
                   {"type": "function", "function": retrieve_KB}]
        )
        break
    except:
        sleep_time = 0.5
        print("client.beta.assistants.create failed, sleep {} second...".format(sleep_time))
        time.sleep(sleep_time)
print(show_json(assistant))
