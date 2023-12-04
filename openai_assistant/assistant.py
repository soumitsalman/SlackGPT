from functools import reduce
import json
import time
from openai import OpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.threads.run import Run
from openai.types.beta.thread import Thread
from utils import debug, config
class AssistantClient:

    def __init__(self, openai_client: OpenAI, openai_asst: Assistant):   
        self.client = openai_client     
        self.asst = openai_asst
        self.thread = self.client.beta.threads.create()
        self.last_message = None

    def add(self, content):
        self.last_message = self.client.beta.threads.messages.create(
            thread_id = self.thread.id,
            role = "user",
            content = _to_str(content)
        )
        return self.last_message

    def run(self):
        #nothing to run
        if self.last_message == None:
            return None
        
        run = self.client.beta.threads.runs.create(
            assistant_id = self.asst.id,
            thread_id = self.thread.id
        )
        debug.show_json(run)
        run = self._wait_on_run(run)
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id,
            order = 'asc',
            after=self.last_message.id)
        debug.show_json(messages)
        return self._collect_response(messages) 
    
    def _collect_response(self, messages) -> list[str]:
        collected = [[content.text.value for content in m.content] for m in messages if m.role == "assistant"]
        join_arr = lambda arr1, arr2: arr1 + arr2
        return reduce(join_arr, collected)

    def _wait_on_run(self, run) -> Run:
        #queued, in_progress, requires_action, cancelling, cancelled, failed, completed, or expired
        while run.status in ["queued", "in_progress"]:
            run = self.client.beta.threads.runs.retrieve(
                thread_id = self.thread.id,
                run_id = run.id
            )
            # TODO: change the sleep time
            time.sleep(1)
        if run.status == "failed" and run.last_error.code == "rate_limit_exceeded":
            raise Exception("run status failed. daddy needs suga'")
        return run

def RetrieveExistingAssistant(assistant_id: str, api_key: str, org_id: str = None):
    # TODO: change the retry
    client = OpenAI(api_key=api_key, organization=org_id, max_retries=5)
    return AssistantClient(
        client,
        client.beta.assistants.retrieve(assistant_id=assistant_id)
    )

def CreateNewAssistant(api_key: str, org_id: str = None, instructions: str = "You are a helpful assistant", name: str = "default"):
    # TODO: change the retry
    client = OpenAI(api_key=api_key, organization=org_id, max_retries=5)
    return AssistantClient(
        client,
        client.beta.assistants.create(
            name=name,
            instructions=instructions,
            # right now I cant use the gpt-4 model because i did not hit the tier 1 yet
            model=config.get_openai_basic_model()
        )
    )

def _to_str(content) -> str:
    if isinstance(content, str):
        return content
    else:
        return json.dumps(content, indent=4)