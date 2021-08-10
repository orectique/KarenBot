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

    if message.content.startswith('-me'):
        if len(Queue) != 0 and message.author == Queue[-1]:
          return await message.channel.send('You cannot reserve consecutive spots.')
        
        name = message.author.name
        Queue.append(message.author)
        tag = str(name) + ' has been added to the queue'
        await message.channel.send(tag)
                  
    
    if message.content.startswith('-read'):
        if len(Queue) == 0:
            return await message.channel.send('Please join the queue first.')

        if message.author != Queue[0]:
            tag = str(message.author.name) + ', please wait for your turn.'
            return await message.channel.send(tag)

        passage = message.content
        if passage[5] == '':
            passage = passage[6:]
        else:
            passage = passage[5:]
            
        Story = Story + '\n' + passage
        await message.channel.send('Okay, I got that!')

        if len(Queue) == 1:
            Queue = []
            return await message.channel.send('There\'s nobody in the queue!')
        
        Queue = Queue[1:]
        tag = str(Queue[0].name) + ', you\'re next'
        await message.channel.send(tag)


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
        if message.author.guild_permissions.manage_messages != True and message.author != Queue[0]:
            return await message.channel.send('You cannot skip positions on the queue.')

        if len(Queue) == 0:
            return await message.channel.send('Cannot skip on an empty queue.')

        tag = str(Queue[0].name) + ' was skipped.'
        await message.channel.send(tag)
        
        if len(Queue) != 0:
            Queue = Queue[1:]
            tag = str(Queue[0].name) + ', you\'re next'
            await message.channel.send(tag)

        else:
            await message.channel.send('The queue looks empty.')
            

    if message.content.startswith('-reset'):
        if message.author.guild_permissions.manage_messages == True:  
            Story = ''
            Queue = []
            await message.channel.send('KarenBot has been reset.')
        else:
            await message.channel.send('You do not have the authority to reset KarenBot.')

    if message.content.startswith('-queue'):
        if len(Queue) == 0:
            return await message.channel.send('There\'s nobody in the queue.')
        
        tag = 'Members in queue:'
        for member in Queue:
            tag += '\n\t' + str(member.name)
        await message.channel.send(tag) 

    if message.content.startswith('-CoC'):
        await message.channel.send('https://hackclub.us/karenbot-code-of-conduct')

    if message.content.startswith('-export'):
        name = message.content
        name = name[8:] + '.txt'
        file = open('content.txt', 'w')
        file.write(Story)
        file.close()
        with open('content.txt', 'rb') as fp:
            await message.channel.send(file=discord.File(fp, name))

        os.remove('content.txt')

TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
