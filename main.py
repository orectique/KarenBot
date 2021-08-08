import discord
from collections import Counter
import pandas
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Bot is ready')

Story = ''

Queue = []

@client.event
async def on_message(message):
    global Queue
    global Story

    if message.author == client.user:
        return

    if message.content.startswith('$karen-me'):
        name = message.author.name
        Queue.append(message.author.name)
        await message.channel.send(name, ' has been added to the list!')
    
    while len(Queue) != 0:
        if message.author == Queue[0]:
            if message.content.startswith('$karen-read'):
                passage = message.content
                passage = passage[11:]
                Story = Story + '\n' + passage
                Queue = Queue[1:]
                await message.channel.send('Okay, I got that!')
                await message.channel.send(Story)
                tag = '<@!' + str(Queue[0].name) + '>, you\'re next'
                await message.channel.send(tag)

    if message.content.startswith('$karen-narrate'):
        if len(Story) == 0:
            await message.channel.send('You haven\'t written anything yet!')
        else:     
            await message.channel.send(Story)

TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
