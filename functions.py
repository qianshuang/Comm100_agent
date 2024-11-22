# -*- coding: utf-8 -*-

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
        "required": ["location", "unit"],
        "additionalProperties": False  # 不要添加其他参数
    },
    "strict": True  # 严格按照schema生成函数调用
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
        "required": ["location"],
        "additionalProperties": False
    },
    "strict": True
}

retrieve_KB = {
    "name": "retrieve_KB",
    "description": "If other tools are insufficient to answer the user's question, retrieve the knowledge base to obtain the answer",
    "parameters": {  # 无参数情况
        "type": "object",
        "properties": {
        },
        "additionalProperties": False
    },
    "strict": True
}
