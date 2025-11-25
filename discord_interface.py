import discord
import os, shutil
from bot_interface import GeminiBot
from discord.ext import commands
from dotenv import load_dotenv

def delete_contents_from_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

@commands.command()
async def play(ctx : commands.Context):
    if not ctx.message.attachments:
        await ctx.send("Upload an audio file with this command.")
        return

    message : discord.Message = ctx.message
    attachment = message.attachments[0]
    file_path = f"./downloads/{attachment.filename}"
    await attachment.save(file_path)

    if ctx.author.voice is None:
        await ctx.send("Join a voice channel first!")
        return

    channel = ctx.author.voice.channel
    vc = None
    if ctx.voice_client is None:
        vc = await channel.connect()
    else:
        vc = ctx.voice_client

    if vc.is_playing():
        ctx.voice_client.stop()

    vc.play(discord.FFmpegPCMAudio(file_path), after=lambda e: delete_contents_from_folder("./downloads/"))
    await ctx.send(f"Now playing: {attachment.filename}")

class DiscordClient(commands.Bot):
    def __init__(self):
        load_dotenv()
        self.token = os.environ["DISCORD_TOKEN"]
        self.bot = GeminiBot()
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents, command_prefix="!")

        self.add_command(play)

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
            await message.channel.send(content=response[0:1999], reference=message)
        await self.process_commands(message)
        return


if __name__ == "__main__":
    discord_bot = DiscordClient()
    discord_bot.run(discord_bot.token)