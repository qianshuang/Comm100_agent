# -*- coding: utf-8 -*-

import time
from openai import AzureOpenAI
from functions import *
from secret import *

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
            instructions="You are a weather bot. Use the provided functions to answer questions.",
            tools=[{"type": "code_interpreter"},
                   {"type": "file_search"},
                   {"type": "function", "function": get_current_temperature},
                   {"type": "function", "function": get_rain_probability}]
        )
        break
    except:
        sleep_time = 0.5
        print("client.beta.assistants.create failed, sleep {} second...".format(sleep_time))
        time.sleep(sleep_time)
print(assistant)

# 2. 创建用户栈
thread = client.beta.threads.create()
print(thread)

# 3. 创建交互
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    # content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
    # content="请画一张饼图的示意图"
    content="What's the weather in San Francisco today and the likelihood it'll rain? And what's the height of Yao Ming?"
)
print(message)

# 4. 调用Agent（异步执行）
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    # instructions="Please address the user as Jane Doe. The user has a premium account."
)
print(run)

# 5. 获取结果
if run.status == 'completed':
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    try:
        print(messages.data[0].content[0].text.value)
    except:
        print(messages.data[0].content[0])
elif run.status == 'requires_action':
    # 函数调用
    tool_outputs = []
    for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "get_current_temperature":
            tool_outputs.append({"tool_call_id": tool.id, "output": "57"})
        elif tool.function.name == "get_rain_probability":
            tool_outputs.append({"tool_call_id": tool.id, "output": "0.06"})

    # 提交函数调用结果给Agent，组装最终输出
    if tool_outputs:
        run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )

    # 输出最终结果
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.data[0].content[0].text.value)
else:
    print(run.status)
