import toml
import os

# change this path later
_config = toml.load("/home/soumitsr/Codes/openai-connector/config.toml")

def load(from_file="config.toml"):
    if os.path.exists(from_file):
        global _config
        _config = toml.load(from_file)
    # else stay with default or throw some error

def get_openai_api_key() -> str:
    return _config["openai"]["COCOSLACK_API_KEY"]

def get_openai_org_id() -> str:
    return _config["openai"]["OPENAI_ORG_ID"]

def get_openai_assistant_model() -> str:
    return _config["openai"]["ASSISTANT_MODEL"]

def get_openai_basic_model() -> str:
    return _config["openai"]["BASIC_MODEL"]

def get_group_chat_assistant() -> str:
    return _config['openai']['GROUP_CHAT_ASSISTANT_ID']

def get_slack_bot_key() -> str:
    return _config['slack']['poster']['POSTER_BOT_TOKEN']

def get_slack_app_key() -> str:
    return _config['slack']['poster']['POSTER_APP_TOKEN']

def get_slack_poster_user_id() -> str:
    return _config['slack']['poster']['POSTER_USER_ID']

def get_redditor_app_id() -> str:
    return _config['reddit']['REDDITOR_APP_ID']

def get_redditor_app_secret() -> str:
    return _config['reddit']['REDDITOR_APP_SECRET']

def get_redditor_app_name() -> str:
    return _config['reddit']['REDDITOR_APP_NAME']


