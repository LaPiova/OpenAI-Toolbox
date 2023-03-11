from dotenv import load_dotenv
from module.chat import ChatBot

load_dotenv()

if __name__ == '__main__':
	bot = ChatBot()
	bot.ask_stream(message="Who are you?")

