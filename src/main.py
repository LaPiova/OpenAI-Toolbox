from module.ChatBotInterface.discord_chatbot import DiscordBot
from dotenv import load_dotenv
import sys
import signal

load_dotenv()
bot = DiscordBot()

def halting_handler(signum, frame):
    print("Received signal: ", signum)
    bot.save_user_history()
    exit(0)


if __name__ == '__main__': 
    signal.signal(signal.SIGTERM, halting_handler)
    signal.signal(signal.SIGINT, halting_handler)
    bot.run_discord_bot()
    
