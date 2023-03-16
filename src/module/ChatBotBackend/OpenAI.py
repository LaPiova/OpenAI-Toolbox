import os
import openai
import random
import string

def get_random_str(n:int)->str:
	"""
	Generate a random string of length n
	"""
	return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))

def get_system_prompt(key:str, prompt=None, lang:str="English"):
	SYSTEM_PROMPT_TEMPLATES: dict = {
		"default": "You are ChatGPT, a large language model trained by OpenAI. You will answer questions precisely and coherently. If you don't know the answer, you will answer \"I don't know.\" honestly. All your responses in this conversation will be " + lang + ".",
		"translator": "You are ChatGPT, a large language model based translator. If there are additional instructions from user, these instructions will be given inside curly braces, e.g. \" {Translate all future inputs into Chinese.}\". If there are no instructions, you will translate the input into " + lang + ".",
		"linux": "I want you to act as a linux terminal. I will type commands and you will reply with what the terminal should show. I want you to only reply with the terminal output inside one unique code block, and nothing else. do not write explanations. do not type commands unless I instruct you to do so. When I need to tell you something in English, I will do so by putting text inside curly brackets {like this}. My first command is pwd.",
		"grammarly": "I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations. My first sentence is \"istanbulu cok seviyom burada olmak cok guzel\"."
	}
	if prompt:
		return prompt
	else:
		if key in SYSTEM_PROMPT_TEMPLATES:
			return SYSTEM_PROMPT_TEMPLATES[key]
		else:
			print("Prompt key does not exist.")
			return None

def get_stream_response(response) -> str:
	ret_msg = ""
	for chunk in response:
		if "content" in chunk["choices"][0]["delta"]:
			ret_msg += chunk["choices"][0]["delta"]["content"]
	return ret_msg


class User:
	"""
	User class for OpenAI GPT-3.5-turbo chatbot
	"""
	def __init__(self, user_id):
		self.id = user_id
		self.last_thread = None
		self.threads: dict = {	}

	def list_thread(self):
		keys = ""
		for key in self.threads:
			keys += (key + ", ")
		keys = keys[:-2] + "."
		return keys, self.last_thread


	def delete_thread(self, thread_id=None):
		if not thread_id:
			thread_id = self.last_thread
		if not (thread_id in self.threads):
			return ("ERROR. Thread not found.")
		else:
			del self.threads[thread_id]
			return ("Thread " + thread_id + " deleted.")

	def select_thread(self, key):
		if key in self.threads:
			self.last_thread = key
			return "You are on conversation " + key + " now."
		else:
			thread_list, cur_thread = self.list_thread()
			return "Thread_ID does not exist. You have threads of " + thread_list + " Currently you are on " + cur_thread + "."

class ChatBot:
	"""
	Chat class for OpenAI GPT-3.5-turbo chatbot
	"""

	def __init__(
		self,
		api_key: str=None, 							# OpenAI API key
		model: str="gpt-3.5-turbo-0301",			# Chat Completion model
		max_tokens: int=2048,						# Max tokens to generate
		temperature: float=0.5,						# Temperature for response
		top_p: float=1.0,							# Top possiblity for response
		presence_penalty: float=0.0,				# Presence penalty for response
		frequency_penalty: float=0.0,				# Frequency penalty for response
		n: int=1									# Number of potential choices to generate
		):
		"""
		Initializes the Chat class
		"""
		if api_key:
			openai.api_key = api_key
		else:
			openai.api_key = os.getenv("OPENAI_API_KEY")
		self.model = model
		self.max_tokens = max_tokens
		self.temperature = temperature
		self.top_p = top_p
		self.presence_penalty = presence_penalty
		self.frequency_penalty = frequency_penalty
		self.n = n
		self.users: dict = {}


	async def ask_stream(
			self,
			user_id=None,
			thread_id=None,
			message=None,
			prompt_key=None,
			lang=None,
			system_prompt: str="You are ChatGPT, a large language model trained by OpenAI. You will answer questions precisely and coherently.",
		):
		# User ID handling
		if not user_id:
			# If user_id not specified
			print("User ID is required.")
			return None
		if user_id in self.users:
			# If user exists
			user = self.users[user_id]
		else:
			# Create new user
			user = User(user_id)
			self.users[user_id] = user
		if prompt_key:
			if lang:
				system_prompt = get_system_prompt(prompt_key, prompt=None, lang=lang)
			else:
				system_prompt = get_system_prompt(prompt_key, prompt=None)

		# Thread ID handling
		if user.last_thread:
			thread_id = user.last_thread
		if thread_id:
			# thread_id is provided
			if thread_id in user.threads:
				# thread_id exists
				thread = user.threads[thread_id]
				thread.append({'role': 'user', 'content': message})
			else:
				# thread_id doesn't exist, create new thread
				thread = [
					{'role': 'system', 'content': system_prompt},
					{'role': 'user', 'content': message}
				]
				user.threads[thread_id] = thread
		else:
			# thread_id not provided. Create default thread_id by 
			suffix = get_random_str(4)
			while ("thread_" + suffix) in user.threads:
				suffix = get_random_str(4)
			thread_id = "thread_" + suffix
			thread = [
					{'role': 'system', 'content': system_prompt},
					{'role': 'user', 'content': message}
			]
			user.threads[thread_id] = thread

		user.last_thread = thread_id

		response = openai.ChatCompletion.create(
			model=self.model,
			messages=user.threads[thread_id],
			temperature=self.temperature,
			stream=True)
		response = get_stream_response(response)
		user.threads[thread_id].append({'role': 'assistant', 'content': response})

		return response

