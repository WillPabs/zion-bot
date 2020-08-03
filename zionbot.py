import discord


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
client = discord.Client()
commands = read_commands()

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send_message(f"""Welcome to Zionopolis {member.mention}""")


@client.event
async def on_message(message):
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
            await message.channel.send(f"""@{members_objects[0]} is the Almighty, Omnipotent, Omniscient overlord""")
        elif content == "!commands":
            await message.channel.send(commands)
        else:
            await message.channel.send(f"""User: {message.author} tried to do command {message.content}, in channel {message.channel}""")
    else:
        print(f"""User: {message.author} tried to do command {message.content}, in channel {message.channel}""")



client.run(token)
