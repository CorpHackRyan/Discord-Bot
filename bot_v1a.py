# All the available API's available on Discord: https://discordpy.readthedocs.io/en/latest/api.html#

import os
import discord
from discord.ext import commands
import random
from dotenv import load_dotenv


# Load environment variables - Token required for Discord
load_dotenv("bottoken.env")
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# As of discord.py v1.5.0, you are required to use Intents for your bot, you can read more about
# them by clicking link below. (This deviates from the initial tutorial but is a requirement to work properly.
# https://discordpy.readthedocs.io/en/latest/api.html#discord.Intents

# Presence Intent switch. Otherwise, this will not work.
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


# There's 2 different ways to use this function. If we don't include the '*' then it will only return
# the first word in the command. The * will consume all of the string.
# async def password(ctx, var):
@client.command()
async def password(ctx, *, var):
    await ctx.send(var)
    password_input = var

    # This is the next bit of code I need to write to execute the password and spit it back to user


@client.event
async def on_ready():
    # on_ready is an event handler which handles the event when client has connected to discord bot
    # and it has finished preparing the data that Discord has sent
    # on_ready() will be called (and message will be printed) once client is ready for further action

    # Print server info (name/id from discord)
    print(f'{client.user} has connected to Discord!')
    print(client.guilds)

    # The below prints the guild name loaded from the .env file
    print("\n\n Guild name loaded in the the .env file: ", GUILD, "\n")


    # Note: Even though we can be pretty confident at this point in the tutorial that our bot is only connected
    # to a single guild (so client.guilds[0] would be simpler), it’s important to realize that a bot user can be
    # connected to many guilds.
    # Therefore, a more robust solution is to loop through client.guilds to find the one we’re looking for.

    # We loop through the guild data that Discord has sent client (which I printed above), namely client.guilds.
    # Then, we found the guild with the matching name and printed a formatted string to stdout.
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        'Using a for loop\n'
        f'{client.user} is connected to the following guild:\n'
        f'Server name & id: {guild.name} (id: {guild.id})\n'
    )

    # An alternative utility functions available in discord.py - discord.utils.find() - is one utility that
    # can improve the simplicity and readability of this code by replacing the for loop with an intuitive,
    # abstracted function, and will produce the same result
    #
    # find() takes a function, called a predicate, which identifies some characteristic of the element in the iterable
    # that you’re looking for. Here, we used a particular type of anonymous function, called a lambda, as the
    # predicate.
    #
    # In this case, you’re trying to find the guild with the same name as the one you stored in the DISCORD_GUILD
    # environment variable. Once find() locates an element in the iterable that satisfies the predicate, it
    # will return the element. This is essentially equivalent to the break statement in the previous example,
    # but cleaner.

    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
            'Using the discord.utils.find() function\n'
            f'{client.user} is connected to the following guild:\n'
            f'Server name & id: {guild.name} (id: {guild.id})\n'
    )

    # discord.py has even abstracted this concept one step further with the get() utility:
    # get() takes the iterable and some keyword arguments. The keyword arguments represent
    # attributes of the elements in the iterable that must all be satisfied for get() to return the element.

    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        'Using the discord.utils.get() function\n'
        f'{client.user} is connected to the following guild:\n'
        f'Server name & id: {guild.name} (id: {guild.id})\n'
    )

    # As demonstrated, all 3 functions yield the same printed results.

    # The below prints the total member count in the guild, by referencing the member_count field
    print(f'Total member count: {guild.member_count}')

    # The below iterates through all the members in the server and prints their respective names and ID's
    print('Guild members:')
    membercount = 1

    # There is a better way to do this, and I'd like to figure out how to print the current enumeration
    # as it goes through the for loop without having to introduce an additional variable (membercount)

    for member in guild.members:
        print(str(membercount) + f'  - {member.name}')
        membercount += 1

    # RESPONDING TO MESSAGES FROM THE CHAT ROOM
    # We now need to incorporate the 'import random' to be able to use the random.choice() function
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        brooklyn_99_quotes = [
            'I\'m the human form of the 100 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        if message.content == '!membercount':
            await message.channel.send(f'There are {guild.member_count} members in the {guild.name} guild')

        if message.content == 'bad bot':
            await message.channel.send('Then program me correctly so I\'m not a bad bot!')

        if message.content == 'good bot':
            await message.channel.send('Ahh.. you finally programmed me the way you want me to be!')

        if message.content == '!robots_use':
            await message.channel.send('My use is to serve you sire. Your wish is my command. Whatever thee asks, '
                                       'ye shall get.')

        # This overrides the the default on_message from any commands being used
        await client.process_commands(message)

    @client.event
    async def on_member_join(member):
        channel = guild.get_channel(759819859428638753)
        await channel.send(f"Hello {member}! Thanks for joining us. Be sure to check out the <#772866366515445761> "
                           f"for the servers rules and guidelines. The <#772864039406927902> room contains information "
                           f"containing our discussion meetup times. "
                           f"We hope you enjoy your stay!")

client.run(TOKEN)


