import os
from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI, OpenAIChat
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def extract_last_AI_response(message):
	"""
	Extract last response from OpenAI GPT-3.5-turbo chatbot
	"""
	ptr2 = len(message)
	ptr1 = ptr2 - 3
	while (ptr1 >= 0):
		if message[ptr1:ptr2] == "AI:":
			return message[ptr2 + 1:]
		ptr1 -= 1
		ptr2 -= 1
	return "Error. Response not found."

class User:
	"""
	User class for OpenAI GPT-3.5-turbo chatbot
	"""
	def __init__(self, user_id):
		self.user_id = user_id
		self.threads = {}
		self.last_thread: str = None

	def create_thread(self, llm, thread_id):
		memory = ConversationSummaryBufferMemory(llm=llm, memory_key="chat_history")
		agent = initialize_agent(
			tools=load_tools(['google-serper']), 
			llm=llm,
			agent="conversational-react-description", 
			memory=memory, 
			verbose=True
			)
		self.threads[thread_id] = {"agent": agent, "memory": memory}

	def message_IO(self, thread_id, message):
		agent = self.threads[thread_id]["agent"]
		memory = self.threads[thread_id]["memory"]
		agent.run(message)
		return extract_last_AI_response((memory.load_memory_variables({}))['chat_history'])


class Langchain_Bot:
	"""
	Langchain_Bot class for OpenAI GPT-3.5-turbo chatbot
	"""
	def __init__(self, temperature=0):
		self.llm = OpenAIChat(model_name='gpt-3.5-turbo', temperature=0, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]), verbose=True)
		self.users = {}


	def chat(self, user_id, message, thread_id=None):
		if not (user_id in self.users):
			# User first time send messages.
			if not thread_id:
				return ("ERROR. No previous thread. Please specify the thread name.")
			else:
				user = User(user_id)
				self.users[user_id] = user
				user.create_thread(self.llm, thread_id)
				return user.message_IO(thread_id, message)
		else:
			user = self.users[user_id]
			if not thread_id:
				# User sends messages to the last thread
				if not users.last_thread:
					# User has no threads left
					return ("ERROR. No previous thread. Please specify the thread name.")
				else:
					return user.message_IO(user.last_thread, message)
			else:
				if thread_id in user.threads:
					return user.message_IO(thread_id, message)
				else:
					# Create a new thread
					user.create_thread(self.llm, thread_id)
					return user.message_IO(thread_id, message)

