# ChatGPT Discord Bot

> ### Build your own Discord bot using ChatGPT

## Features

* `/chat [message]` Chat with ChatGPT!
* `/private` ChatGPT switch to private mode. This flag only applies to the user who execute it.
* `/public`  ChatGPT switch to public  mode. This flag only applies to the user who execute it.
* `/reset` Clear ChatGPT conversation history of the current conversation thread you are on.
* `/create thread_id prompt_key prompt:optional lang:optional` Create a new thread named `thread_id`, with system prompt template `prompt_key`, or customized template `prompt`, and replies you in the language `lang`.
* `/threads` List threads you have and the thread you are currently on.
* `/select thread_id` Switch between your existing threads.

### Mode

* `public mode (default)`  the bot directly reply on the channel

  ![image](https://user-images.githubusercontent.com/89479282/206565977-d7c5d405-fdb4-4202-bbdd-715b7c8e8415.gif)

* `private mode` the bot's reply can only be seen by the person who used the command

  ![image](https://user-images.githubusercontent.com/89479282/206565873-b181e600-e793-4a94-a978-47f806b986da.gif)

### Prompt_key Templates:
* `default` The bot will answer precisely and coherently. If it doesn't know, it will honestly reply "I don't know".
* `translator` The bot will translate user input in any language into the `lang` you specified.
* `linux` The bot will act as a simulated linux terminal.
* `grammarly` The bot will translate your input into the language you have specified. If it is already the language you specified, the bot will try to make the translation more elegant and accurate.

# Setup

## Critical prerequisites to install

* run ```pip3 install -r requirements.txt```

* **Rename the file `.env.dev` to `.env`**

* Recommended python version `3.10`
## Step 1: Create a Discord bot

1. Go to https://discord.com/developers/applications create an application
2. Build a Discord bot under the application
3. Get the token from bot setting

   ![image](https://user-images.githubusercontent.com/89479282/205949161-4b508c6d-19a7-49b6-b8ed-7525ddbef430.png)
4. Store the token to `.env` under the `DISCORD_BOT_TOKEN`

   <img height="190" width="390" alt="image" src="https://user-images.githubusercontent.com/89479282/222661803-a7537ca7-88ae-4e66-9bec-384f3e83e6bd.png">

5. Turn MESSAGE CONTENT INTENT `ON`

   ![image](https://user-images.githubusercontent.com/89479282/205949323-4354bd7d-9bb9-4f4b-a87e-deb9933a89b5.png)

6. Invite your bot to your server via OAuth2 URL Generator

   ![image](https://user-images.githubusercontent.com/89479282/205949600-0c7ddb40-7e82-47a0-b59a-b089f929d177.png)
## Step 2: Official API authentication

### Geanerate an OpenAI API key
1. Go to https://beta.openai.com/account/api-keys

2. Click Create new secret key

   ![image](https://user-images.githubusercontent.com/89479282/207970699-2e0cb671-8636-4e27-b1f3-b75d6db9b57e.PNG)

3. Store the SECRET KEY to `.env` under the `OPENAI_API_KEY`

4. You're all set for [Step 3](#step-3-run-the-bot-on-the-desktop)

## Step 2: Website ChatGPT authentication - 2 approaches

### Email/Password authentication (Not supported for Google/Microsoft accounts)
1. Create an account on https://chat.openai.com/chat

2. Save your email into `.env` under `OPENAI_EMAIL`

3. Save your password into `.env` under `OPENAI_PASSWORD`

4. You're all set for [Step 3](#step-3-run-the-bot-on-the-desktop)

### Session token authentication
1. Go to https://chat.openai.com/chat log in

2. Open console with `F12`

2. Open `Application` tab > Cookies

    ![image](https://user-images.githubusercontent.com/36258159/205494773-32ef651a-994d-435a-9f76-a26699935dac.png)

3. Copy the value for `__Secure-next-auth.session-token` from cookies and paste it into `.env` under `SESSION_TOKEN`

4. You're all set for [Step 3](#step-3-run-the-bot-on-the-desktop)

## Step 3: Run the bot on the desktop

1. Open a terminal or command prompt

2. Navigate to the directory where you installed the ChatGPT Discord bot

3. Run `python3 main.py` to start the bot

### Have a good chat!
## Optional: Disable logging

* Set the value of `LOGGING` in the `.env` to False
## Optional: Setup starting prompt

* A starting prompt would be invoked when the bot is first started or reset
* You can set it up by modifying the content in `starting-prompt.txt`
* All the text in the file will be fired as a prompt to the bot  
* Get the first message from ChatGPT in your discord channel!

   1. Right-click the channel you want to recieve the message, `Copy  ID`

        ![channel-id](https://user-images.githubusercontent.com/89479282/207697217-e03357b3-3b3d-44d0-b880-163217ed4a49.PNG)

   2. paste it into `.env` under `DISCORD_CHANNEL_ID`
