# -*- coding: utf-8 -*-

get_order = {
    "name": "get_order",
    "description": "Get the order details for a specific order",
    "parameters": {
        "type": "object",
        "properties": {
            "order_id": {
                "type": "string",
                "description": "The order id"
            }
        },
        "required": ["order_id"],
        "additionalProperties": False  # 不要添加其他参数
    },
    "strict": True  # 严格按照schema生成函数调用
}

get_item = {
    "name": "get_item",
    "description": "Get the item details or check availability for a specific item",
    "parameters": {
        "type": "object",
        "properties": {
            "item_id": {
                "type": "string",
                "description": "The item id"
            }
        },
        "required": ["item_id"],
        "additionalProperties": False  # 不要添加其他参数
    },
    "strict": True  # 严格按照schema生成函数调用
}

recommend_items = {
    "name": "recommend_items",
    "description": "When users inquire about the existence of specific models or styles of products, recommend up to 3 items to them",
    "parameters": {
        "type": "object",
        "properties": {
        },
        "additionalProperties": False  # 不要添加其他参数
    },
    "strict": True  # 严格按照schema生成函数调用
}

transfer_to_human = {
    "name": "transfer_to_human",
    "description": "When the user expresses the intention to switch to a human agent, transfer the conversation to a customer service representative.",
    "parameters": {
        "type": "object",
        "properties": {
        },
        "additionalProperties": False  # 不要添加其他参数
    },
    "strict": True  # 严格按照schema生成函数调用
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
