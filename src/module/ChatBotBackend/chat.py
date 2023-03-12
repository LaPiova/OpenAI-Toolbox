import os
import openai

# Deprecated version of ChatBot backend.

class User:
	"""
	User class for OpenAI GPT-3.5-turbo chatbot
	"""
	def __init__(self, user_id):
		self.id = user_id
		self.thread: dict = {}

class ChatBot:
	"""
	Chat class for OpenAI GPT-3.5-turbo chatbot
	"""

	def __init__(
		self,
		api_key: str=None, 								# OpenAI API key
		model: str="gpt-3.5-turbo-0301",			# Chat Completion model
		max_tokens: int=3000,						# Max tokens to generate
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


	def ask_stream(
			self,
			user_id=None,
			message=None,
			system_prompt: str="You are ChatGPT, a large language model trained by OpenAI. You will answer questions precisely and coherently.",
		):
		response = openai.ChatCompletion.create(
			model=self.model,
			messages=[
				{'role': 'system', 'content': system_prompt},
				{'role': 'user', 'content': message}
			],
			temperature=self.temperature,
			stream=True)

		for chunk in response:
			print(chunk)
	# Incomplete

