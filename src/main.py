# from dotenv import load_dotenv
# from module.ChatBotBackend.langchain_chatbot import Langchain_Bot

# load_dotenv()

# bot = Langchain_Bot(temperature=0)
# response = await bot.chat(
# 	user_id="test", 
# 	message="Can you explain the techniques used by GPT?",
# 	thread_id="test"
# 	)
# print(response)

# ----------------------------------------------------------

# from module.ChatBotInterface.GPT_discord_bot.src import bot
# from dotenv import load_dotenv
# import sys
# import pdb

# def check_verion() -> None:
#     import pkg_resources
#     import module.ChatBotInterface.GPT_discord_bot.src.log

#     load_dotenv()
#     logger = module.ChatBotInterface.GPT_discord_bot.src.log.setup_logger(__name__)

#     # Read the requirements.txt file and add each line to a list
#     with open('module/ChatBotInterface/GPT_discord_bot/requirements.txt') as f:
#         required = f.read().splitlines()

#     # For each library listed in requirements.txt, check if the corresponding version is installed
#     for package in required:
#         # Use the pkg_resources library to get information about the installed version of the library
#         package_name, package_verion = package.split('==')
#         installed = pkg_resources.get_distribution(package_name)
#         # Extract the library name and version number
#         name, version = installed.project_name, installed.version
#         # Compare the version number to see if it matches the one in requirements.txt
#         if package != f'{name}=={version}':
#             logger.error(f'{name} version {version} is installed but does not match the requirements')
#             sys.exit();

# if __name__ == '__main__': 
#     check_verion()
#     bot.run_discord_bot()

# -------------------------------------------------------------

from module.ChatBotInterface.discord_chatbot import DiscordBot
from dotenv import load_dotenv
import sys
import pdb

def check_verion() -> None:
    import pkg_resources

    load_dotenv()

    # Read the requirements.txt file and add each line to a list
    with open('../requirements.txt') as f:
        required = f.read().splitlines()

    # For each library listed in requirements.txt, check if the corresponding version is installed
    for package in required:
        # Use the pkg_resources library to get information about the installed version of the library
        package_name, package_verion = package.split('==')
        installed = pkg_resources.get_distribution(package_name)
        # Extract the library name and version number
        name, version = installed.project_name, installed.version
        # Compare the version number to see if it matches the one in requirements.txt
        if package != f'{name}=={version}':
            logger.error(f'{name} version {version} is installed but does not match the requirements')
            sys.exit();

if __name__ == '__main__': 
    # check_verion()
    load_dotenv()
    bot = DiscordBot()
    bot.run_discord_bot()
