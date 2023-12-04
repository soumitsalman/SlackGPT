from utils import debug, config
from openai_assistant import assistant
from slack_interface import slack_bot

#### testing assistant ####
# asst = assistant.RetrieveExistingAssistant(
#     api_key=config.get_openai_api_key(), 
#     org_id=config.get_openai_org_id(),
#     assistant_id=config.get_group_chat_assistant())

# asst.add("is the following a correct json blob")
# resp = asst.add_and_run({"a": "b", "c": "d", "e": {"a": "b"}})
# debug.log("main.py", resp)

#### testing slack bot ####
slack_bot.start()