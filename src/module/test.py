import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["WOLFRAM_ALPHA_APPID"] = os.getenv("WOLFRAM_ALPHA_APPID")

from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI, OpenAIChat
from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationSummaryMemory, ConversationSummaryBufferMemory
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.agents import ZeroShotAgent, ConversationalAgent, Tool, AgentExecutor
from langchain import LLMChain, PromptTemplate
from langchain.utilities import GoogleSearchAPIWrapper

llm = OpenAIChat(model_name='gpt-3.5-turbo', temperature=0, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), verbose=True)
tools = load_tools(['google-serper'])
memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history")
agent = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory, verbose=True)

agent.run("You are a linux terminal. You will execute my input and display the output. You will also display an error if the input is wrong. If I'm going to talk to you in English, the input will be in a curly bracket {like this}.")
# agent.run("pwd")
print(memory.load_memory_variables({}))

def get_methods(object, spacing=20):
  methodList = []
  for method_name in dir(object):
    try:
        if callable(getattr(object, method_name)):
            methodList.append(str(method_name))
    except Exception:
        methodList.append(str(method_name))
  processFunc = (lambda s: ' '.join(s.split())) or (lambda s: s)
  for method in methodList:
    try:
        print(str(method.ljust(spacing)) + ' ' +
              processFunc(str(getattr(object, method).__doc__)[0:90]))
    except Exception:
        print(method.ljust(spacing) + ' ' + ' getattr() failed')

# object_methods = get_methods(memory)