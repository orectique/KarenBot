![GitHub](https://img.shields.io/github/license/orectique/KarenBot) ![Hit count](https://hits.vercel.app/orectique/karenbot.svg) [![Add to Server](https://img.shields.io/badge/Discord-Add%20to%20Server-blue)](https://discord.com/api/oauth2/authorize?client_id=873981661187039263&permissions=100352&scope=bot)

## Welcome to KarenBot.

KarenBot is a Discord bot that can be used to order a discussion or take notes at meetings. It allows users in the server to add themselves to a queue to formally voice their points.

### Features

- -help
>> Displays list of all commands.
- -me
>> Adds user to queue.
- -read [text]
>> Appends the text to the larger corpus.
- -note -a/t/f
>> Takes notes. Works exclusive to the queue. -a/t/f are format modifiers to use when 'f' is unlocked (See -flock/-funlock): '-a' registers author's name along with the message, '-t' adds the timestamp on the message, and 'f' displays both the details.
- -narrate -s/o
>> Shares the full body of work till that point. Access specifiers '-s' refers to the log of -read and '-o' refers to the log of -note.
- -queue
>> Displays order of users currently in the queue.
- -skip
>> Skips self on one's own turn.
- -CoC
>> Helps one access the Rules and Code of Conduct of KarenBot.

#### High level commands - User needs the 'Manage Messages' permission
- -skip
>> Passes over the current user in the queue.
- -flock/-funlock
>> Enables/Disables the 'f' lock. If 'f' is locked, Karen always registers the timestamp and author of the note. Works with -note.
- -reset -s/o
>> Clears the queue and the specified corpus.
- -export -s/o
>> Creates a downloadable .txt file and shares it in the channel.
