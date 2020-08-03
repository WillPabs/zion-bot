import discord
import time
import asyncio

messages = joined = 0


def read_token():
    with open("text_files/secrets.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


def read_commands():
    with open("text_files/commands.txt", "r") as f:
        lines = f.readlines()
        return [line for line in lines]


# INFO
token = read_token()
server_id = 704717649707270224
commands = read_commands()
client = discord.Client()


async def update_stats():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("text_files/stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0
            joined = 0

            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)


@client.event
async def on_member_update(before, after):
    n = after.nick
    if n:
        if n.lower().count("zion") > 0:
            last = before.nick
            if last:
                await after.edit(nick=last)
            else:
                await after.edit(nick="You're not worthy")


@client.event
async def on_member_join(member):
    global joined
    joined += 1

    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send_message(f"""Welcome to Zionopolis {member.mention}""")


@client.event
async def on_message(message):
    global messages
    messages += 1

    server = client.get_guild(server_id)
    channels = ["zion-bot-test"]
    valid_users = ["brookln#2760"]
    members_objects = server.members
    content = message.content

    # COMMANDS
    if str(message.channel) in channels and str(message.author) in valid_users:
        if content.find("!hello") != -1:
            await message.channel.send(f"""Hi, {str(message.author).split("#")[0]}!""")
        elif content == "!users":
            await message.channel.send(f"""# of Members: {server.member_count}""")
        elif content == "!whoisgod":
            await message.channel.send(f"""@{members_objects[3]} is the Almighty, Omnipotent, Omniscient overlord""")
        elif content == "!commands":
            embed = discord.Embed(title="Help on Zion", description="List of current Zion commands")
            embed.add_field(name="!hello", value="Greets the user")
            embed.add_field(name="!users", value="Prints the number of users")
            embed.add_field(name="!whoisgod", value="Declaration of your overlord")
            embed.add_field(name="!commands", value="Prints a list of usable commands")
            await message.channel.send(content=None, embed=embed)
        else:
            await message.channel.send(
                f"""User: {message.author} tried to do command {message.content}, in channel {message.channel}""")
    else:
        print(f"""User: {message.author} tried to do command {message.content}, in channel {message.channel}""")

    banned_words = ["bad", "stop", "45"]

    for word in banned_words:
        if message.content.count(word) > 0:
            print("You attempted to use a bad word")
            await message.channel.purge(limit=1)


client.loop.create_task(update_stats())  # runs update_stats() constantly in the background
client.run(token)



