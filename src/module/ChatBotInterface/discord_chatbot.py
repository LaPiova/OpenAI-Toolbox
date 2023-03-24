import discord
import os
from discord import app_commands
from dotenv import load_dotenv
from module.ChatBotInterface.utils import log
from module.ChatBotBackend.OpenAI import ChatBot, User
from discord.ext import tasks
import traceback

logger = log.setup_logger(__name__)
load_dotenv("../../.env")


class aclient(discord.Client):
	def __init__(self) -> None:
		intents = discord.Intents.default()
		intents.message_content = True
		super().__init__(intents=intents)
		self.tree = app_commands.CommandTree(self)
		self.activity = discord.Activity(
			type=discord.ActivityType.watching,
			name="/chat for sending messages. | /help for user manual."
			)

class DiscordBot:

	def __init__(self, temperature=0, model="gpt-3.5-turbo-0301"):
		self.bot = ChatBot(temperature=temperature, model=model)
		self.users = self.bot.load_history()

	def init_user_and_isPrivate(self, user_id, private=True) -> bool:
		if (user_id in self.users):
			# logger.info(f"User {user_id} already exists")
			return self.users[user_id]["isPrivate"]
		else:
			self.users[user_id] = {"isPrivate": True}
			self.bot.users[user_id] = User(user_id)
			logger.info(f"User {user_id} created")
		return private

	def save_user_history(self):
		self.bot.save_history()
		logger.info("User history saved.")

	@tasks.loop(seconds=10)
	async def save_history_loop(self):
		self.save_user_history()

	async def send_message(self, message, user_message):
		isPrivate = self.init_user_and_isPrivate(message.user.id)
		isReplyAll =  os.getenv("REPLYING_ALL")
		if isReplyAll == "False":
			author = message.user.id
			await message.response.defer(ephemeral=isPrivate)
		else:
			author = message.user.id
		try:
			response = (f'> **{user_message}** - <@{str(author)}' + '> \n\n')
			try:
				response = f"{response}{await self.bot.ask_stream(user_id=author, message=user_message)}"
			except:
				logger.error("Error in asking stream. Please try again.")
			char_limit = 1900
			if len(response) > char_limit:
				# Split the response into smaller chunks of no more than 1900 characters each(Discord limit is 2000 per chunk)
				if "```" in response:
					# Split the response if the code block exists
					parts = response.split("```")

					for i in range(len(parts)):
						if i%2 == 0: # indices that are even are not code blocks
							if isReplyAll == "True":
								await message.channel.send(parts[i])
							else:
								await message.followup.send(parts[i], ephemeral=isPrivate)

						else: # Odd-numbered parts are code blocks
							code_block = parts[i].split("\n")
							formatted_code_block = ""
							for line in code_block:
								while len(line) > char_limit:
									# Split the line at the 50th character
									formatted_code_block += line[:char_limit] + "\n"
									line = line[char_limit:]
								formatted_code_block += line + "\n"  # Add the line and seperate with new line

							# Send the code block in a separate message
							if (len(formatted_code_block) > char_limit+100):
								code_block_chunks = [formatted_code_block[i:i+char_limit]
													 for i in range(0, len(formatted_code_block), char_limit)]
								for chunk in code_block_chunks:
									if isReplyAll == "True":
										await message.channel.send(f"```{chunk}```")
									else:
										await message.followup.send(f"```{chunk}```", ephemeral=isPrivate)
							elif isReplyAll == "True":
								await message.channel.send(f"```{formatted_code_block}```")
							else:
								await message.followup.send(f"```{formatted_code_block}```", ephemeral=isPrivate)

				else:
					response_chunks = [response[i:i+char_limit]
									   for i in range(0, len(response), char_limit)]
					for chunk in response_chunks:
						if isReplyAll == "True":
							await message.channel.send(chunk)
						else:
							await message.followup.send(chunk, ephemeral=isPrivate)
			elif isReplyAll == "True":
				await message.channel.send(response)
			else:
				await message.followup.send(response, ephemeral=isPrivate)
		except Exception as e:
			if isReplyAll == "True":
				await message.channel.send("> **Error: Something went wrong, please try again later!**")
			else:
				await message.followup.send("> **Error: Something went wrong, please try again later!**", ephemeral=isPrivate)
			logger.exception(f"Error while sending message: {e}")


	async def send_start_prompt(self, client):
		global bot
		import os.path

		config_dir = os.path.abspath(f"{__file__}/../../")
		prompt_name = 'starting-prompt.txt'
		prompt_path = os.path.join(config_dir, prompt_name)
		discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")
		try:
			if os.path.isfile(prompt_path) and os.path.getsize(prompt_path) > 0:
				with open(prompt_path, "r", encoding="utf-8") as f:
					prompt = f.read()
					if (discord_channel_id):
						logger.info(f"Send starting prompt with size {len(prompt)}")
						# chat_model = os.getenv("CHAT_MODEL")
						response = ""
						# if chat_model == "OFFICIAL":
							# response = f"{response}{await responses.official_handle_response(prompt)}"
						response = f"{response}{await self.bot.ask_stream(user_id=author, message=prompt, thread_id='test')}"
						# elif chat_model == "UNOFFICIAL":
						# 	response = f"{response}{await responses.unofficial_handle_response(prompt)}"
						channel = client.get_channel(int(discord_channel_id))
						await channel.send(response)
						logger.info(f"Starting prompt response:{response}")
					else:
						logger.info("No Channel selected. Skip sending starting prompt.")
			else:
				logger.info(f"No {prompt_name}. Skip sending starting prompt.")
		except Exception as e:
			logger.exception(f"Error while sending starting prompt: {e}")


	def run_discord_bot(self):
		client = aclient()

		@client.event
		async def on_ready():
			await self.send_start_prompt(client)
			await client.tree.sync()
			logger.info(f'{client.user} is now running!')
			self.save_history_loop.start()

		@client.event
		async def on_error(self, event, *args, **kwargs):
		    exc_type, value, tb = sys.exc_info()
		    traceback_text = ''.join(traceback.format_exception(exc_type, value, tb))
		    print(f"Ignoring exception in {event}:\n{traceback_text}")
		    await client.logout()
		    await client.login()

		@client.tree.command(name="chat", description="Have a chat with ChatGPT")
		async def chat(interaction: discord.Interaction, *, message: str):
			# isReplyAll =  os.getenv("REPLYING_ALL")
			# if isReplyAll == "True":
			# 	await interaction.response.defer(ephemeral=False)
			# 	await interaction.followup.send(
			# 		"> **Warn: You already on replyAll mode. If you want to use slash command, switch to normal mode, use `/replyall` again**")
			# 	logger.warning("\x1b[31mYou already on replyAll mode, can't use slash command!\x1b[0m")
			# 	return
			if interaction.user == client.user:
				return
			username = str(interaction.user)
			user_message = message
			channel = str(interaction.channel)
			logger.info(
				f"\x1b[31m{username}\x1b[0m : 'Sent a message'")
			await self.send_message(interaction, user_message)

		@client.tree.command(name="private", description="Toggle private access")
		async def private(interaction: discord.Interaction):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			await interaction.response.defer(ephemeral=False)
			if not isPrivate:
				# isPrivate = not isPrivate
				self.users[author]["isPrivate"] = True
				#
				logger.warning("\x1b[31mSwitch to private mode\x1b[0m")
				await interaction.followup.send(
					"> **Info: Next, the response will be sent via private message. If you want to switch back to public mode, use `/public`**")
			else:
				logger.info("You already on private mode!")
				await interaction.followup.send(
					"> **Warn: You already on private mode. If you want to switch to public mode, use `/public`**")

		@client.tree.command(name="public", description="Toggle public access")
		async def public(interaction: discord.Interaction):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			await interaction.response.defer(ephemeral=False)
			if isPrivate:
				# isPrivate = not isPrivate
				self.users[author]["isPrivate"] = False
				#
				await interaction.followup.send(
					"> **Info: Next, the response will be sent to the channel directly. If you want to switch back to private mode, use `/private`**")
				logger.warning("\x1b[31mSwitch to public mode\x1b[0m")
			else:
				await interaction.followup.send(
					"> **Warn: You already on public mode. If you want to switch to private mode, use `/private`**")
				logger.info("You already on public mode!")

		# @client.tree.command(name="replyall", description="Toggle replyAll access")
		# async def replyall(interaction: discord.Interaction):
		# 	isReplyAll =  os.getenv("REPLYING_ALL")
		# 	os.environ["REPLYING_ALL_DISCORD_CHANNEL_ID"] = str(interaction.channel_id)
		# 	await interaction.response.defer(ephemeral=False)
		# 	if isReplyAll == "True":
		# 		os.environ["REPLYING_ALL"] = "False"
		# 		await interaction.followup.send(
		# 			"> **Info: The bot will only response to the slash command `/chat` next. If you want to switch back to replyAll mode, use `/replyAll` again.**")
		# 		logger.warning("\x1b[31mSwitch to normal mode\x1b[0m")
		# 	elif isReplyAll == "False":
		# 		os.environ["REPLYING_ALL"] = "True"
		# 		await interaction.followup.send(
		# 			"> **Info: Next, the bot will response to all message in this channel only.If you want to switch back to normal mode, use `/replyAll` again.**")
		# 		logger.warning("\x1b[31mSwitch to replyAll mode\x1b[0m")
			

		# @client.tree.command(name="chat-model", description="Switch different chat model")
		# @app_commands.choices(choices=[
		# 	app_commands.Choice(name="Official GPT-3.5", value="OFFICIAL"),
		# 	app_commands.Choice(name="Website ChatGPT", value="UNOFFCIAL")
		# ])
		# async def chat_model(interaction: discord.Interaction, choices: app_commands.Choice[str]):
		# 	await interaction.response.defer(ephemeral=False)
		# 	if choices.value == "OFFICIAL":
		# 		os.environ["CHAT_MODEL"] = "OFFICIAL"
		# 		await interaction.followup.send(
		# 			"> **Info: You are now in Official GPT-3.5 model.**\n> You need to set your `OPENAI_API_KEY` in `env` file.")
		# 		logger.warning("\x1b[31mSwitch to OFFICIAL chat model\x1b[0m")
		# 	elif choices.value == "UNOFFCIAL":
		# 		os.environ["CHAT_MODEL"] = "UNOFFICIAL"
		# 		await interaction.followup.send(
		# 			"> **Info: You are now in Website ChatGPT model.**\n> You need to set your `SESSION_TOKEN` or `OPENAI_EMAIL` and `OPENAI_PASSWORD` in `env` file.")
		# 		logger.warning("\x1b[31mSwitch to UNOFFICIAL(Website) chat model\x1b[0m")
				
		@client.tree.command(name="delete", description="Complete reset ChatGPT conversation history")
		async def delete(interaction: discord.Interaction, *, thread_id:str=None):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			self.bot.users[author].delete_thread(thread_id=thread_id)
			await interaction.response.defer(ephemeral=False)
			await interaction.followup.send("> **Info: I have deleted this thread.**")
			logger.warning(
				"\x1b[31mChatGPT bot has successfully deleted this thread.\x1b[0m")
			await self.send_start_prompt(client)

		@client.tree.command(name="reset", description="Complete reset ChatGPT conversation history")
		async def reset(interaction: discord.Interaction, *, thread_id:str=None):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			self.bot.users[author].reset_thread(thread_id=thread_id)
			await interaction.response.defer(ephemeral=False)
			await interaction.followup.send("> **Info: I have forgotten everything.**")
			logger.warning(
				"\x1b[31mChatGPT bot has successfully reset this thread.\x1b[0m")
			await self.send_start_prompt(client)


		@client.tree.command(name="create", description="Create a new conversation thread")
		async def create_thread(interaction: discord.Interaction, *, thread_id:str, prompt_key:str, prompt:str=None, lang:str="English"):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			response = self.bot.users[author].create_thread(thread_id, prompt_key, prompt, lang)
			await interaction.response.defer(ephemeral=isPrivate)
			await interaction.followup.send("> **" + response + "**")

		@client.tree.command(name="threads", description="Show all conversation threads stored in the bot and current conversation you are on")
		async def list_thread(interaction: discord.Interaction):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			thread_list, cur_thread = self.bot.users[author].list_thread()
			await interaction.response.defer(ephemeral=isPrivate)
			if thread_list:
				if cur_thread:
					await interaction.followup.send("> **Info: You have: " + thread_list + " Currently, you are on " + cur_thread +".**")
				else:
					await interaction.followup.send("> **Info: You have: " + thread_list + " Currently, you are not on any threads.**")
			else:
				await interaction.followup.send("> **Info: You haven't started any conversation yet.**")

		@client.tree.command(name="select", description="Select a conversation thread to chat with")
		async def select_thread(interaction: discord.Interaction, *, thread_id: str):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			response = self.bot.users[author].select_thread(thread_id)
			await interaction.response.defer(ephemeral=isPrivate)
			await interaction.followup.send("> **" + response + "**")

		@client.tree.command(name="set", description="Change the thread_ID of your current thread")
		async def set_thread_id(interaction: discord.Interaction, *, thread_id: str):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			response = self.bot.users[author].set_thread_id(thread_id)
			await interaction.response.defer(ephemeral=isPrivate)
			await interaction.followup.send("> **" + response + "**")

		@client.tree.command(name="export", description="Export the chat history.")
		async def export_chat_history(interaction: discord.Interaction, *, thread_id: str=None):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			file = self.bot.users[author].export_chat_history(thread_id)
			await interaction.response.defer(ephemeral=isPrivate)
			await interaction.followup.send("> **Info: Your chat history has been sent to you in DM.**")
			await interaction.user.send(file=file)

		@client.tree.command(name="help", description="Show help for the bot")
		async def help(interaction: discord.Interaction):
			author = interaction.user.id
			isPrivate = self.init_user_and_isPrivate(author)
			await interaction.response.defer(ephemeral=False)
			await interaction.followup.send(""":star:**BASIC COMMANDS** \n
			- `/chat [message]` Chat with ChatGPT!
			- `/public` ChatGPT switch to public mode
			- `/replyall` ChatGPT switch between replyall mode and default mode
			- `/reset` Clear ChatGPT conversation history
			- `/threads` Show all conversation threads stored in the bot and current conversation you are on
			- `/select [thread_id]` Select a conversation thread to chat with
			- `/set [thread_id]` Change the thread_ID of your current thread
			- `/create [thread_id] [prompt_key] [prompt:optional] [lang:optional]` Create a new thread named `[thread_id]`, with prompt template `[prompt_key]` or optional customized prompt `[prompt]`. The responses will be given in language `[lang]`. By default, the response will be in English.\n
			- Sample prompt_key:
				`default`: Default question-answering bot.
				`translator`: Translate into the language you specified.
				`linux`: Simulates a linux terminal.
				`grammarly`: Improves and translate the input into the specified language with explanation.
			For complete documentation, please visit https://github.com/LaPiova/OpenAI-Toolbox""")
			logger.info(
				"\x1b[31mSomeone need help!\x1b[0m")

		@client.event
		async def on_message(message):
			isReplyAll =  os.getenv("REPLYING_ALL")
			if isReplyAll == "True" and message.channel.id == int(os.getenv("REPLYING_ALL_DISCORD_CHANNEL_ID")):
				if message.author == client.user:
					return
				username = str(message.author)
				user_message = str(message.content)
				channel = str(message.channel)
				logger.info(f"\x1b[31m{username}\x1b[0m : '{user_message}' ({channel})")
				await self.send_message(message, user_message)

		TOKEN = os.getenv("DISCORD_BOT_TOKEN")

		client.run(TOKEN)
