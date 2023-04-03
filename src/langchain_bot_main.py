from module.ChatBotBackend.langchain_bot import LUser

user = LUser("test")
print(user.id)
print(user.last_thread)
print(user.threads)