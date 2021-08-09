import discord
from collections import Counter
import pandas
import os

client = discord.Client()

@client.event
async def on_ready():
    print('Bot is ready')

Story = ''
Count = []
Queue = []

@client.event
async def on_message(message):
    global Queue
    global Story
    global Count
    global Mod

    if message.author == client.user:
        return

    if message.content.startswith('-me'):
        if len(Queue) == 0 or message.author != Queue[-1]:
            name = message.author.name
            Queue.append(message.author)
            tag = str(name) + ' has been added to the queue'
            await message.channel.send(tag)
        else:
            await message.channel.send('You cannot reserve consecutive spots.')
    
    if message.content.startswith('-read'):
        if len(Queue) != 0:
            if message.author == Queue[0]:
                passage = message.content
                if passage[5] == '':
                    passage = passage[6:]
                else:
                    passage = passage[5:]
                Story = Story + '\n' + passage
                await message.channel.send('Okay, I got that!')

                if len(Queue) == 1:
                    Queue = []
                    await message.channel.send('That\'s all for the day.')
                else:
                    Queue = Queue[1:]
                    tag = str(Queue[0].name) + ', you\'re next'
                    await message.channel.send(tag)
            else:
                tag = str(message.author.name) + ', please wait for your turn.'
                await message.channel.send(tag)

        else:
            await message.channel.send('Please join the queue first.')

    if message.content.startswith('-narrate'):
        if len(Story) == 0:
            await message.channel.send('You haven\'t written anything yet!')
        else:     
            await message.channel.send(Story)

    if message.content.startswith('-help'):
        help_message = ''' __**KarenBot Help**__
        
**-me** *Adds user to queue.*
**-read [text]** *Appends the text to the larger corpus.*
**-narrate** *Shares the full body of work till that point.*
**-queue** *Displays order of users currently in the queue.*

__The next two commands require the user to have 'Manage Messages' permission.__

**-skip** *Passes over the current user in the queue.*
**-reset** *Clears the queue and the corpus.*'''

        await message.channel.send(help_message)
    
    if message.content.startswith('-skip'):
        if message.author.guild_permissions.manage_messages == True or message.author == Queue[0]:
            if len(Queue) != 0:
                tag = str(Queue[0].name) + ' was skipped.'
                await message.channel.send(tag)
                Queue = Queue[1:]
                tag = str(Queue[0].name) + ', you\'re next'
                await message.channel.send(tag)

            else:
                await message.channel.send('Nobody in the queue.')
        
        else:
            await message.channel.send('You cannot skip positions on the queue.')

    if message.content.startswith('-reset'):
        if message.author.guild_permissions.manage_messages == True:  
            Story = ''
            Queue = []
            await message.channel.send('KarenBot has been reset.')
        else:
            await message.channel.send('You do not have the authority to reset KarenBot.')

    if message.content.startswith('-queue'):
        tag = 'Members in queue:'
        for member in Queue:
            tag += '\n\t' + str(member.name)
        
        await message.channel.send(tag) 

    if message.content.startswith('-roll'):
        await message.channel.send('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
