from utils import debug, config, system_message
from openai_assistant import assistant
from slack_interface import slack_bot
from social_media.user_sign_in import signin_reddit

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

#### testing system messages ####
# for topic in ["error", "wait", "scheduled", "trashed"]:
#     print(system_message.get_system_message(topic))

# signin_reddit()