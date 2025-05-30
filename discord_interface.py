import discord
import os
from bot_interface import GeminiBot
from discord.ext import commands
from dotenv import load_dotenv

class DiscordClient(commands.Bot):
    def __init__(self):
        load_dotenv()
        self.token = os.environ["DISCORD_TOKEN"]
        self.bot = GeminiBot()
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents, command_prefix="!")
    
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message :  discord.Message):
        if message.author == self.user:
            return
        bot_call = False
        for mention in message.mentions:
            if mention.bot and mention.name == self.user.name:
                bot_call = True
        if bot_call:
            question = (message.content[message.content.find(">"):])[2:]
            if message.reference:
                channel = message.channel
                replied_message = await channel.fetch_message(message.reference.message_id)
                replied_message_author = replied_message.author.display_name
                if not question:
                    question = message.content
                question= (
                    f"Previous Reply:\n"
                    f"{replied_message.content}\n\n"
                    f"Previous Reply Sent By: {replied_message_author}\n\n"
                    f"Question:\n{question}\n\n"
                    f"Question Author: {message.author.display_name}"
                )
            else:
                question= (
                    f"Question:\n{question}\n\n"
                    f"Question Author: {message.author.display_name}"
                )
            print(question)
            response = self.bot.complete_text(question)
            await message.channel.send(content=response[0:1999])
        return