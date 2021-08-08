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
Que = []

@client.event
async def on_message(message):
    global Queue
    global Story

    if message.author == client.user:
        return

    if message.content.startswith('$karen-me'):
        name = message.author.name
        Queue.append(message.author)
        tag = str(name) + ' has been added to the list!'
        await message.channel.send(tag)
    
    if message.content.startswith('$karen-read'):
        if len(Queue) != 0:
            if message.author == Queue[0]:
                passage = message.content
                passage = passage[11:]
                Story = Story + '\n' + passage
                await message.channel.send('Okay, I got that!')
                await message.channel.send(Story)

                if len(Queue) == 1:
                   await message.channel.send('That\'s all for the day.')
                else:
                    Queue = Queue[1:]
                    tag = str(Queue[0].name) + ', you\'re next'
                    await message.channel.send(tag)
        
        else:
            await message.channel.send('Where\'s everybody gone to?')

    if message.content.startswith('$karen-narrate'):
        if len(Story) == 0:
            await message.channel.send('You haven\'t written anything yet!')
        else:     
            await message.channel.send(Story)

    if message.content.startswith('$karen-help'):
        await message.channel.send('Where\'s your manager? You work for me; I don’t work for you.')
    
    if message.content.startswith('$karen-skip'):
        tag = str(Queue[0].name) + ' was skipped.'
        await message.channel.send(tag)
        Queue = Queue[1:]
        tag = str(Queue[0].name) + ', you\'re next'
        await message.channel.send(tag)
        

TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
