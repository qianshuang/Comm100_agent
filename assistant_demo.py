# -*- coding: utf-8 -*-

from openai import AzureOpenAI
from secret import *
from utils import *

client = AzureOpenAI(api_key=gpt4o_ak, api_version="2024-05-01-preview", azure_endpoint=gpt4o_ep)

get_current_temperature = {
    "name": "get_current_temperature",
    "description": "Get the current temperature for a specific location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g., San Francisco, CA"
            },
            "unit": {
                "type": "string",
                "enum": ["Celsius", "Fahrenheit"],
                "description": "The temperature unit to use. Infer this from the user's location."
            }
        },
        "required": ["location", "unit"]
    }
}

get_rain_probability = {
    "name": "get_rain_probability",
    "description": "Get the probability of rain for a specific location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The city and state, e.g., San Francisco, CA"
            }
        },
        "required": ["location"]
    }
}

# 1. 创建Agent
assistant = client.beta.assistants.create(
    model="GPT4oChat",
    temperature=0,
    name="Weather Bot",
    instructions="You are a weather bot. Use the provided functions to answer questions.",
    # code_interpreter: After the "Create Thread" is called every session is killed when either: 1. There is no activity on it (no run) for 30 minutes (idle timeout) 2. 60 minutes have passed since the time "Create Thread" was called.
    tools=[{"type": "code_interpreter"},
           {"type": "file_search"},
           {"type": "function", "function": get_current_temperature},
           {"type": "function", "function": get_rain_probability}]
)
print(show_json(assistant))

# 2. 创建用户栈
thread = client.beta.threads.create()

# 3. 创建交互
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What's the weather in San Francisco today and the likelihood it'll rain?"
)

# 4. 调用Agent（异步执行）
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account."
)

# 5. 获取结果
if run.status == 'completed':
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.data[0].content[0].text.value)
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
    run = wait_on_run(client, run, thread.id)
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print(messages.data[0].content[0].text.value)
    else:
        print(show_json(run))
else:
    print(run.status)

# Run Steps
run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id, order="asc")
print([show_json(step.step_details) for step in run_steps.data])
