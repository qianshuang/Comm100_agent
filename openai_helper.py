# -*- coding: utf-8 -*-

import time
from openai import AzureOpenAI
from secret import *

client = AzureOpenAI(api_key=gpt4o_ak, api_version="2024-02-01", azure_endpoint=gpt4o_ep)


# azure HTTP 接口调用
# 'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.
# query_body = {"temperature": 0, "messages": [{"role": "user", "content": "Hello"}], "response_format": {"type": "json_object"}}
# headers = {'content-type': 'application/json', 'api-key': gpt4o_ak}
# response = requests.post(gpt4o_ep, json=query_body, headers=headers, timeout=100)
# print(json.loads(response.text)["choices"][0]["message"]["content"])

# AzureOpenAI 调用
# client = AzureOpenAI(api_key=gpt4o_ak, api_version="2024-02-01", azure_endpoint=gpt4o_ep)
# completion = client.chat.completions.create(
#     model="gpt-4o",  # 可以写gpt-4或gpt-3.5，但实际都是调用gpt-4o
#     messages=[{"role": "user", "content": "Hello"}]
# )
# print(completion.choices[0].message.content)


def get_gpt_res(prompt_messages):
    num_retries = 3
    response = None
    for _ in range(num_retries):
        try:
            completion = client.chat.completions.create(
                model="gpt-4o",  # 可以写gpt-4或gpt-3.5，但实际都是调用gpt-4o
                messages=prompt_messages
            )
            return completion.choices[0].message.content
        except:
            sleep_time = 0.5
            print("call_azure failed, sleep {} second...".format(sleep_time))
            time.sleep(sleep_time)

    if response is None:
        print("call_azure failed after 3 retries...")
        raise RuntimeError("Failed to call_azure...")
