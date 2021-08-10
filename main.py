import discord
import os
from random import choice

client = discord.Client()

@client.event
async def on_ready():
    print('Bot is ready')

channels = {}
replies = ['Okay, I got that!', 'Nice one!', 'I have added that!', 'Thanks for your input!', 'Cool, that\'s now in my book!']
lock = 0

@client.event
async def on_message(message):

    global channels, replies, lock

    if message.author == client.user:
        return

    channel_id = message.channel.id

    if channel_id not in channels:
        channels[channel_id] = {
          "Queue": [],
          "Story": '',
          "Note" : ''
        }
        

    if message.content.startswith('-me'):
        if len(channels[channel_id]["Queue"]) != 0 and message.author == channels[channel_id]["Queue"][-1]:
          return await message.channel.send('You cannot reserve consecutive spots.')
        
        name = message.author.name
        channels[channel_id]["Queue"].append(message.author)
        tag = str(name) + ' has been added to the queue'
        await message.channel.send(tag)
                  
    
    if message.content.startswith('-read'):
        if len(channels[channel_id]["Queue"]) == 0:
            return await message.channel.send('Please join the queue first.')

        if message.author != channels[channel_id]["Queue"][0]:
            tag = str(message.author.name) + ', please wait for your turn.'
            return await message.channel.send(tag)

        
        passage = message.content
        if passage[5] == '':
            passage = passage[6:]
        else:
            passage = passage[5:]

        channels[channel_id]["Story"] += '\n' + passage
        await message.channel.send(choice(replies))

        if len(channels[channel_id]["Queue"]) == 1:
            channels[channel_id]["Queue"] = []
            return await message.channel.send('There\'s nobody in the queue!')
        
                
        channels[channel_id]["Queue"] = channels[channel_id]["Queue"][1:]
        tag = str(channels[channel_id]["Queue"][0].name) + ', you\'re next'
        await message.channel.send(tag)

        if len(channels[channel_id]["Queue"]) == 2:
            await message.channel.send('There\'s only one person left in the queue!')

    if message.content.startswith('-flock') and message.author.guild_permissions.manage_messages == True:
        lock = 1
    
    if message.content.startswith('-funlock') and message.author.guild_permissions.manage_messages == True:
        lock = 0

    if message.content.startswith('-note'):
        Timestamp = message.channel.created_at
        passage = message.content
        passage = passage[5:]
        if lock == 0:
            if '-a' in message.content:
                channels[channel_id]["Note"] += '\n' + str(message.author) + ' : ' + passage[3:]
            if '-t' in message.content:
                channels[channel_id]["Note"] += '\n' + '[' + str(Timestamp) + ']: ' + passage[3:]
            if '-f' in message.content:
                channels[channel_id]["Note"] += '\n' + str(message.author) + ' at [' + str(Timestamp) + ']: ' + passage[4:]
        else:
            channels[channel_id]["Note"] += '\n' + passage
        
        await message.channel.send(choice(replies))

    if message.content.startswith('-narrate'):

        if '-s' in message.content:
            if len(channels[channel_id]["Story"]) == 0:
                await message.channel.send('You haven\'t written anything yet!')
            elif len(channels[channel_id]["Story"]) > 2000:
                await message.channel.send('The text is too large to preview. Please use the *-export* function.')
            else:     
                await message.channel.send(channels[channel_id]["Story"])

        if '-o' in message.content:
            if len(channels[channel_id]["Note"]) == 0:
                await message.channel.send('You haven\'t written anything yet!')
            elif len(channels[channel_id]["Note"]) > 2000:
                await message.channel.send('The text is too large to preview. Please use the *-export* function.')
            else:     
                await message.channel.send(channels[channel_id]["Note"])

        else:
            await message.channel.send('Please specify the corpus - s/o.')

    if message.content.startswith('-help'):
        help_message = ''' __**KarenBot Help**__
        
**-me** *Adds user to queue.*
**-read [text]** *Appends the text to the larger corpus.*
**-narrate -s/o** *Shares the full body of work till that point. Argument s returns regular corpus, while n returns timestamped notes.*
**-queue** *Displays order of users currently in the queue.*
**-CoC** *Helps one access the Rules and Code of Conduct of KarenBot.*

__The next two commands require the user to have 'Manage Messages' permission.__

**-skip** *Passes over the current user in the queue.*
**-reset** *Clears the queue and the corpus.*
**-export -s/o** *Creates a downloadable .txt file and shares it in the channel.*

'''

        await message.channel.send(help_message)
    
    if message.content.startswith('-skip'):
        if message.author.guild_permissions.manage_messages != True and message.author != channels[channel_id]["Queue"][0]:
            return await message.channel.send('You cannot skip positions on the queue.')

        if len(channels[channel_id]["Queue"]) == 0:
            return await message.channel.send('Cannot skip on an empty queue.')

        tag = str(channels[channel_id]["Queue"][0].name) + ' was skipped.'
        await message.channel.send(tag)
        
        if len(channels[channel_id]["Queue"]) > 1 :
            channels[channel_id]["Queue"] = channels[channel_id]["Queue"][1:]
            tag = str(channels[channel_id]["Queue"][0].name) + ', you\'re next'
            await message.channel.send(tag)
        
        elif len(channels[channel_id]["Queue"]) == 1:
            channels[channel_id]["Queue"] = []
            await message.channel.send('The queue looks empty.')

        else:
            await message.channel.send('The queue looks empty.')
            

    if message.content.startswith('-reset'):
        if message.author.guild_permissions.manage_messages:
            channels[channel_id]["Story"] = ''
            channels[channel_id]["Note"] = ''
            channels[channel_id]["Queue"] = []
            await message.channel.send('KarenBot has been reset.')
        else:
            await message.channel.send('You do not have the authority to reset KarenBot.')

    if message.content.startswith('-queue'):
        if len(channels[channel_id]["Queue"]) == 0:
            return await message.channel.send('There\'s nobody in the queue.')
        
        tag = 'Members in queue:'
        for member in channels[channel_id]["Queue"]:
            tag += '\n\t' + str(member.name)
        await message.channel.send(tag) 

    if message.content.startswith('-CoC'):
        await message.channel.send('https://hackclub.us/karenbot-code-of-conduct')

    if message.content.startswith('-manager'):
        await message.channel.send('https://tenor.com/view/michael-scott-frustrated-gif-13247684')

    if message.content.startswith('-export -s') and message.author.guild_permissions.manage_messages == True:
        name = message.content
        name = name[8:] + '.txt'
        file = open('content.txt', 'w')
        file.write(channels[channel_id]['Story'])
        file.close()
        with open('content.txt', 'rb') as fp:
            await message.channel.send(file=discord.File(fp, name))

    if message.content.startswith('-export -o') and message.author.guild_permissions.manage_messages == True:
        name = message.content
        name = name[11:] + '.txt'
        file = open('notes.txt', 'w')
        file.write(channels[channel_id]['Note'])
        file.close()
        with open('notes.txt', 'rb') as fp:
            await message.channel.send(file=discord.File(fp, name))

        os.remove('content.txt')

TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
