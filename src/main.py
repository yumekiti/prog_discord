import discord
from discord.ext import commands
from datetime import datetime

import write

import os
import random
from dotenv import load_dotenv
load_dotenv()

class MyBot(commands.Bot):
  async def setup_hook(self):
    await self.load_extension('task')
    await self.tree.sync()

bot = MyBot(command_prefix='/', intents=discord.Intents.all())

attendance_enojis = ['๐','๐']

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')

@bot.command()
async def attend(ctx):
  message = await ctx.send(f'<@&{1026379495478927410}>{datetime.now().strftime("%Y/%m/%d")}ใงใใๅบๅธญใใพใใ๏ผ')

  for emoji in attendance_enojis:
    await message.add_reaction(emoji)

  today = datetime.now().strftime("%Y/%m/%d")
  while today == datetime.now().strftime("%Y/%m/%d"):
    reaction, user = await bot.wait_for('reaction_add')
    if reaction.emoji == '๐' and user != bot.user:
      roles = [role.name for role in user.roles]
      await write.main(ctx, [], { 'name': user.name, 'roles': roles })

@bot.command()
async def report(ctx):
  roles = [role.name for role in ctx.author.roles]
  if len(ctx.message.content.split()) > 1:
    body = { "name": ctx.author.name, "content": ctx.message.content.split()[1] }
  else: body = []
  await write.main(ctx, body, { "name": ctx.author.name, "roles": roles })

# @bot.command()
# async def record(ctx):
#   await write.record()
#   await ctx.send('ๆฌๆฅใฎๆดปๅๅๅฎนใ่จ้ฒใใพใใใ')

@bot.command()
async def ping(ctx):
  await ctx.send('pong')

if __name__ == '__main__':
  bot.run(os.getenv('TOKEN'))
