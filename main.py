from os import getenv
from dotenv import load_dotenv
import discord
from function import add,remove,change,check,reset,do,undo,help
import time

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == client.user:
            return
        if (arg := message_handler(message.content)) is None:
            return
        print(f'Message from {message.author}: {message.content} in {message.channel}')
        try:
            (action, arg) = respone_handler(arg)
            await action_handler(message,action,arg)
            # await message.channel.send("This is an automated reply")
        except Exception as e:
            print(e)

def message_handler(message):
    arg = message.split(' ')
    prefix = arg.pop(0)
    if prefix == 'bot' and arg != []:
        return arg
    return None
    
def respone_handler(arg):
    name = arg.pop(0)
    if name in name_list:
        func = func_list[name_list.index(name)]
        return func(arg)
    return ("reply","Something wrong, try again")

async def action_handler(msg,action,*args):
    match(action):
        case "reply":
            await msg.channel.send(args[0])
        case "react":
            await msg.add_reaction(args[0])

async def day_reset():
    while(True):
        if (time.time()["hour"] > 9):
            print("Time reset")

if __name__ == "__main__":

    intents = discord.Intents.default()
    intents.message_content = True

    name_list = ["add","rm","change","check","reset","do","undo","help"]
    func_list = [add,remove,change,check,reset,do,undo,help]

    load_dotenv()
    TOKEN = getenv('TOKEN')

    client = MyClient(intents=intents)
    client.run(TOKEN)