import random
import json

def load(filepath):
    with open(filepath, 'r') as f:
        msgs = json.load(f)
    return msgs

def get_system_message(topic: str) -> str:
    if topic in _messages:
        return _messages[topic][random.randint(0, len(_messages[topic])-1)]

_messages = load("./utils/_system_messages.json")