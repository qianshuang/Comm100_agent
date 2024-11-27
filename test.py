# -*- coding: utf-8 -*-

from openai import AzureOpenAI

from secret import *

client = AzureOpenAI(api_key=gpt4o_ak, api_version="2024-05-01-preview", azure_endpoint=gpt4o_ep)

message = client.beta.threads.messages.create(
    thread_id="thread_ZaB4ase6gmSdKvwvlW5KygPG",
    role="user",
    content="What's the weather in San Francisco today and the likelihood it'll rain?"
)
print(message)

run = client.beta.threads.runs.create_and_poll(
    thread_id="thread_ZaB4ase6gmSdKvwvlW5KygPG",
    assistant_id="asst_0SuZGxbmBEDOzrEBvnA3iMrk",
    instructions="Please address the user as Jane Doe. The user has a premium account."
)
print(run)

if run.status == 'completed':
    messages = client.beta.threads.messages.list(thread_id="thread_ZaB4ase6gmSdKvwvlW5KygPG")
    print(messages.data[0].content[0].text.value)
