import json
from sys import displayhook
import openai

def show_json(obj):
    print(json.dumps(json.loads(obj.model_dump_json()), indent=4))

def get_json_str(obj):
    return json.dumps(obj, indent=4)

def log(from_where, what):
    # with open("log.json", mode="a") as log_file:
    print(f"[{from_where}] {what}")
