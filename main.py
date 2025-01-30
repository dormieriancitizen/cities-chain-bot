import asyncio
import itertools
import os
from dotenv import load_dotenv
load_dotenv()

from discord.ext import commands

# Load messages from a file
def message_file_reader():
    with open("chain.txt", "r") as file:
        for line in file:
            yield line.rstrip()        

# message_cycle = itertools.islice(itertools.cycle(messages), len(messages))  # Cycle through messages repeatedly
message_cycle = message_file_reader()
turn_condition = asyncio.Condition()  # Ensures alternation
current_bot_turn = 1  # Bot 1 starts first

# Bot setup
intents = None  # Selfbots don't use intents
bot1 = commands.Bot(command_prefix="!", self_bot=True, intents=intents)
bot2 = commands.Bot(command_prefix="!", self_bot=True, intents=intents)

TOKEN1: str = os.getenv("TOKEN1") # type: ignore
TOKEN2: str = os.getenv("TOKEN2") # type: ignore
TARGET_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Replace with your channel ID
CITIES_CHAIN_UUID = 1126539776120606750

last_city_file = open("last_city.txt","w")

async def send_message(bot, bot_id):
    def check(reaction, user):
        return user.id == CITIES_CHAIN_UUID and reaction.message.id == command.id #<---- The check performed

    global current_bot_turn
    await bot.wait_until_ready()
    channel = bot.get_channel(TARGET_CHANNEL_ID)

    if not channel:
        print(f"Bot {bot_id}: Channel not found!")
        return

    while True:
        async with turn_condition:
            await turn_condition.wait_for(lambda: current_bot_turn == bot_id)
            
            try:
                message = "!" + next(message_cycle)
            except StopIteration:
                print(f"Bot {bot_id}: No more messages left in file.")
                return

            command = await channel.send(message)

            last_city_file.seek(0)
            last_city_file.write(message)
            last_city_file.truncate()
            last_city_file.flush()

            print(f"Bot {bot_id}: Sent message -> {message}")

            current_bot_turn = 3 - bot_id  # Switch between 1 and 2
            turn_condition.notify_all()

            try:
                await bot.wait_for('reaction_add',check=check)
            except:
                await asyncio.sleep(5) 

@bot1.event
async def on_ready(): # type: ignore
    print(f"Bot 1 logged in as {bot1.user}")
    asyncio.create_task(send_message(bot1, 1))

@bot2.event
async def on_ready():
    print(f"Bot 2 logged in as {bot2.user}")
    asyncio.create_task(send_message(bot2, 2))

# Run both bots
async def main():
    task1 = bot1.start(TOKEN1)
    task2 = bot2.start(TOKEN2)
    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    asyncio.run(main())
