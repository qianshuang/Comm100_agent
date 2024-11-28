# -*- coding: utf-8 -*-

import json


def get_order_detail(order_id):
    order_detail_y = {
        "code": 0,
        "msg": "success",
        "order_detail": {
            "order_id": "789456123",
            "user_id": "12345",
            "order_date": "2024-11-25T10:30:00Z",
            "status": "Processing",
            "item_ids": ["987654", "987655"],
            "total": 162.47,
            "currency": "USD",
            "shipping_address": {
                "recipient_name": "John Doe",
                "street": "123 Main St, Los Angeles, CA, USA",
                "phone": "+1-234-567-8901"
            }
        }
    }
    order_detail_n = {
        "code": -1,
        "msg": "Order does not exist."
    }
    return json.dumps(order_detail_y)


def get_item_detail(item_id):
    item_detail_y = {
        "code": 0,
        "msg": "success",
        "item_detail": {
            "id": "123456",
            "name": "Wireless Bluetooth Headphones",
            "description": "High-quality wireless headphones with noise-cancellation.",
            "category": "Electronics",
            "price": 59.99,
            "currency": "USD",
            "stock_quantity": 120,
            "brand": "TechSound",
            "images": [
                "https://example.com/images/product1.jpg",
                "https://example.com/images/product1_2.jpg"
            ],
            "sku": "TS-BT-H1",
            "availability": "In Stock",
            "created_at": "2024-11-25T08:00:00Z"
        }
    }
    item_detail_n = {
        "code": -1,
        "msg": "Item does not exist."
    }
    return json.dumps(item_detail_y)


def get_recommend_items():
    recommend_items_y = {
        "code": 0,
        "msg": "success",
        "items": [{
            "id": "101",
            "name": "Wireless Bluetooth Noise-Cancelling Headphones",
            "description": "Experience immersive sound with active noise-cancellation and 30-hour battery life.",
            "category": "Electronics",
            "price": 149.99,
            "currency": "USD",
            "stock_quantity": 50,
            "brand": "SoundPro"
        }, {
            "id": "102",
            "name": "Smart Fitness Tracker Watch",
            "description": "Track your health and fitness with heart rate monitoring, sleep analysis, and GPS tracking.",
            "category": "Wearables",
            "price": 79.99,
            "currency": "USD",
            "stock_quantity": 120,
            "brand": "FitSmart"
        }, {
            "id": "103",
            "name": "4K Ultra HD Smart TV",
            "description": "Enjoy cinematic visuals and smart features with this 55-inch 4K UHD TV.",
            "category": "Home Entertainment",
            "price": 499.99,
            "currency": "USD",
            "stock_quantity": 30,
            "brand": "VisionX"
        }]
    }
    return json.dumps(recommend_items_y)


def transfer_to_human():
    transfer_to_human_y = {
        "code": 0,
        "msg": "success",
        "agent_info": {
            "agent_id": "A12345",
            "name": "John Doe",
            "department": "Customer Support",
            "availability": "online"
        },
        "conversation_id": "C987654321"
    }
    transfer_to_human_n = {
        "code": -1,
        "msg": "No available human agents at the moment.",
        "conversation_id": "C987654321"
    }
    return json.dumps(transfer_to_human_y)


def get_rag_res(chat_his):
    rag_res = {
        "code": 0,
        "msg": "success",
        # "answer": "Sorry, the correct answer to this question cannot be found.",
        "answer": "Zhang Ming's height is 1.85 meters."
    }
    return json.dumps(rag_res)
