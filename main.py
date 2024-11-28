# -*- coding: utf-8 -*-

import os
from fastapi import FastAPI
from openai import AzureOpenAI
from pydantic import BaseModel
from actions import *
from utils import *
from secret import *

app = FastAPI()

client = AzureOpenAI(api_key=gpt4o_ak, api_version="2024-05-01-preview", azure_endpoint=gpt4o_ep)

user2thread_file = "data/user2thread.json"
user2thread = load_json_file(user2thread_file) if os.path.exists(user2thread_file) else {}


class QueryBody(BaseModel):
    assistant_id: str
    user_id: str
    query: str


@app.get("/")
def welcome():
    return "Welcome to Comm100 Agent."


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
        content=qb.query
    )
    print(show_json(message))

    # 4. 调用Agent（异步执行）
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=qb.assistant_id,
        instructions="For recommend_items function, please provide the user with recommendation reasons to promote to them."
    )
    print(show_json(run))

    # 5. 获取结果
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return {'code': 0, 'msg': 'LLM directly replied', 'data': messages.data[0].content[0].text.value}
    elif run.status == 'requires_action':
        # 函数调用
        tool_outputs = []
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "get_order":
                tool_outputs.append({"tool_call_id": tool.id, "output": get_order_detail(json.loads(tool.function.arguments)["order_id"])})
            elif tool.function.name == "get_item":
                tool_outputs.append({"tool_call_id": tool.id, "output": get_item_detail(json.loads(tool.function.arguments)["item_id"])})
            elif tool.function.name == "recommend_items":
                tool_outputs.append({"tool_call_id": tool.id, "output": get_recommend_items()})
            elif tool.function.name == "transfer_to_human":
                tool_outputs.append({"tool_call_id": tool.id, "output": transfer_to_human()})
            elif tool.function.name == "retrieve_KB":
                messages = client.beta.threads.messages.list(thread_id=thread_id, order="asc")
                chat_history = [mess.content[0].text.value for mess in messages.data]
                tool_outputs.append({"tool_call_id": tool.id, "output": get_rag_res(chat_history)})

        # 提交函数调用结果给Agent，组装最终输出
        if tool_outputs:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        # 输出最终结果
        run = wait_on_run(client, run, thread_id)
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        # print(show_json(messages))
        print(show_json(run))
        return {'code': 0, 'msg': 'Function Called', 'data': messages.data[0].content[0].text.value}
    else:
        return {'code': 0, 'msg': 'Others', 'data': run.status}
