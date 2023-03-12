from dotenv import load_dotenv
from module.langchain_chatbot import Langchain_Bot

load_dotenv()

bot = Langchain_Bot(temperature=0)
response = bot.chat(
	user_id="test", 
	message="Can you explain the techniques used by GPT?",
	thread_id="test"
	)
print(response)
