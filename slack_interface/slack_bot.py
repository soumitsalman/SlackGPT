from utils import debug, config
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from openai_assistant import assistant



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

    def send_messages(self, channel_id, msg) -> str:
        session = self._get_or_create_session(channel_id)
        return session.add_and_run(msg)


app = App(token = config.get_slack_bot_key())
sessions = _ChatSessions()

def start():
    SocketModeHandler(app, config.get_slack_app_key()).start()

@app.message()
def new_message(message, say, client): 
    result = say("Sending to OpenAI. Processing ... ")
    channel_id, user_id = message['channel'], message['user']
    resp = sessions.send_messages(channel_id=channel_id, msg=f"[{user_id}] {message['text']}")
    client.chat_update(
        channel=channel_id, 
        ts=result['ts'], 
        text = _convert_markdown("\n".join(resp))
    )

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