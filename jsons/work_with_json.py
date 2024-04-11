import json


with open("jsons/config.json", "r", encoding='utf-8') as file:
    data = json.load(file)
    pas = data["password"]
    TOKEN = data["TOKEN"]

with open("jsons/chats.json", "r", encoding='utf-8') as file:
    chats_id = []
    try:
        chats = json.load(file)
        for chat in chats:
            chats_id.append(chat["chat_id"])
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []
