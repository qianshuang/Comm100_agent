# -*- coding: utf-8 -*-

import os
from fastapi import FastAPI
from pydantic import BaseModel
from config import *

app = FastAPI()
user2thread_file = "data/user2thread.json"
user2thread = load_json_file(user2thread_file) if os.path.exists(user2thread_file) else {}


class QueryBody(BaseModel):
    user_id: str
    query: str


@app.get("/")
def welcome():
    return "Hello, my friend. Welcome to Comm100 Agent"


@app.post("/call_agent")
def call_agent(qb: QueryBody):
    if qb.user_id in user2thread:
        thread_id = user2thread[qb.user_id]
    else:
        # 2. 创建用户栈
        thread = client.beta.threads.create()
        thread_id = thread.id
        user2thread[qb.user_id] = thread_id
        write_json_file(user2thread, user2thread_file)
        print(show_json(thread))

    # 3. 创建交互
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        # content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
        # content="请画一张饼图的示意图"
        content=qb.query
    )
    print(show_json(message))

    # 4. 调用Agent（异步执行）
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant.id,
        # instructions="Please address the user as Jane Doe. The user has a premium account."
    )
    print(show_json(run))

    # 5. 获取结果
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        try:
            print(messages.data[0].content[0].text.value)
        except:
            print(show_json(messages.data[0].content[0]))
    elif run.status == 'requires_action':
        # 函数调用
        tool_outputs = []
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_current_temperature":
                tool_outputs.append({"tool_call_id": tool.id, "output": "57"})
            elif tool.function.name == "get_rain_probability":
                tool_outputs.append({"tool_call_id": tool.id, "output": "0.06"})
            elif tool.function.name == "retrieve_KB":
                # 获取多轮对话
                messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc")
                chat_history = [mess.content[0].text.value for mess in messages.data]
                # rag_res = get_rag_res(chat_history)
                # tool_outputs.append({"tool_call_id": tool.id, "output": rag_res})
                pass

        # 提交函数调用结果给Agent，组装最终输出
        if tool_outputs:
            client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        # 输出最终结果
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        print(messages.data[0].content[0].text.value)
    else:
        print(run.status)
