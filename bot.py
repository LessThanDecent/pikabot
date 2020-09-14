import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print(f"PikaBot is online ({client.user})")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run('NzU1MTA4NjU0Nzg0NDQ2NDkw.X1-fvA.Y32w2FLkJ6ULoHU64KmQEVkwpqI')
