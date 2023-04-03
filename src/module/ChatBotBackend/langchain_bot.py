from module.ChatBotBackend.default import ChatBot, User
from module.ChatBotBackend.default import get_system_prompt

class LUser(User):
	def __init__(self, user_id):
		super().__init__(user_id)

	def create_thread(self, thread_id, prompt_key, prompt, lang, llm):
		prompt = get_system_prompt(prompt_key, prompt, lang)
		if not prompt:
			return "Prompt key or prompt does not exists."
