import json
from utils import debug, config, system_message
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai_assistant import assistant
from social_media.user_sign_in import signin_reddit

class _ChatSessions:
    def __init__(self):
        self.sessions = {}

    def _get_or_create_session(self, channel_id) -> assistant.AssistantClient:
        if channel_id not in self.sessions:
            self.sessions[channel_id] = assistant.RetrieveExistingAssistant(
                api_key=config.get_openai_api_key(), 
                org_id=config.get_openai_org_id(),
                assistant_id=config.get_group_chat_assistant()
            )
        return self.sessions[channel_id]

    def add_message(self, channel_id, user_id, content):
        session = self._get_or_create_session(channel_id)
        session.add(f"[{user_id}] {content}")
        return session

    def get_response(self, channel_id):
        return self._get_or_create_session(channel_id).run()
        

app = App(token = config.get_slack_bot_key())
sessions = _ChatSessions()

def start():
    SocketModeHandler(app, config.get_slack_app_key()).start()

@app.event("app_home_opened")
def update_home_tab(client, event):
    
    client.views_publish(
        user_id = event['user'],
        view = {
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Learn how home tabs can be more useful and interactive <https://api.slack.com/surfaces/tabs/using|*in the documentation*>."
                    }
                }
            ]
        }
    )


@app.message()
def new_message(message, say, client):     
    channel_id, channel_type, user_id, text = message['channel'], message['channel_type'], message['user'], message['text']    
    debug.log("slack_bot.py", f"channel_type={channel_type} | text={text}")
    # queue message no matter what
    sessions.add_message(channel_id=channel_id, user_id=user_id, content=text)

    # either IM or got mentoned
    if (channel_type == "im") or (f"<@{config.get_slack_poster_user_id()}>" in text):
        # else its action is triggered and will send it to openai
        debug.log("slack_bot.py", "either 1:1 convo or received mention in group or channel convo")
        wait_msg = say(system_message.get_system_message("wait"))
        client.chat_update(
            channel=channel_id, 
            ts=wait_msg['ts'], 
            blocks=[_create_markdown_block(resp) for resp in sessions.get_response(channel_id=channel_id)]
        )

# create a markdown text block
def _create_markdown_block(text: str):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": _convert_markdown(text)
        }
    }

# coverts openai markdown to slack markdown
def _convert_markdown(text: str) -> str:
    conversions = {
        '**': '*',        # Bold
        '__': '_',        # Italic
        '~~': '~',        # Strikethrough
        '```': '```',     # Code block (same in Slack)
        '`': '`',         # Inline code (same in Slack)
        # Hyperlinks are left as they are because Slack automatically detects URLs and formats them.
    }
    
    # Replace based on the conversion dictionary
    for md, slack_md in conversions.items():
        text = text.replace(md, slack_md)
    
    return text