import wikipedia
import keep_alive
import discord
from discord import File
import json
from discord.ext import commands, tasks
import os

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

#prefix function of getting prefix
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

client.remove_command("help")

#start
@client.event
async def on_ready():
    print("The bot is ready to go!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"$help -gladosbot.ml"))

#load command
@client.command()
async def load(ctx, extension):
    if ctx.author.id == 586844180681195530:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"Succesfully loaded {extension}!")
        return

    await ctx.send(f"You don't have permission to use that command!")

#unload command
@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 586844180681195530:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f"Succesfully unloaded {extension}!")
        return

    await ctx.send(f"You dont have permission to use that command!")

#getserver command
@client.command()
async def getserver(ctx):
    if ctx.author.id == 586844180681195530:
        activeservers = client.guilds
        for guild in activeservers:
            await ctx.send(f"{guild.name} {guild.owner_id} {guild.id}")
        return

    await ctx.send(f"You don't have permissions to use that!")

#leaveserver command
@client.command()
async def leaveserver(ctx, id: int):
    if ctx.author.id == 586844180681195530:
        guild = client.get_guild(id)
        await guild.leave()
        await ctx.send(f"Left that server successfully")
        return

    await ctx.send(f"You don't have permissions to use that!")

#reload command
@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 586844180681195530:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"Succesfully reloaded {extension}")
        return

    await ctx.send(f"You dont have permission to use that command!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

#ping command
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! `{round(client.latency * 1000)}ms`')

#on_message event
@client.listen('on_message')
async def prefixresponse(message):
    try:
        if client.user in message.mentions:
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)

            prefix = prefixes[str(message.guild.id)]
            await message.channel.send(f"My prefix here is `{prefix}`")

    except:
        pass

#info command
@client.command()
async def info(ctx):
    em = discord.Embed(title=":question: Info about me!")
    em.add_field(name="**Bot description :**", value="Glados is fun and a moderation bot (Still in BETA mode) which allows you to access its various multiple unique features! Glados is coded in language Python (discord.py)", inline=False)
    em.add_field(name="**Version :**", value="11.4.3", inline=True)
    em.add_field(name="**Date of creation :**", value="21th September, 2020", inline=True)
    em.add_field(name="**Servers :**", value=len(client.guilds), inline=True)
    em.add_field(name="**Creator :**", value="<@!586844180681195530> and <@!789816228423139369>", inline=False)
    em.set_thumbnail(url="https://media.discordapp.net/attachments/793031241363750922/833362504964636703/IMG_20210416_233115_980.jpg?width=671&height=670")
    await ctx.send(embed=em)

#supportus
@client.command()
async def supportus(ctx):
    em = discord.Embed(title="<a:yes:803969799277248542> Support Us!", color=ctx.author.color)
    em.add_field(name="Invite me to your server!", value="[Click here to invite me!](https://discord.com/api/oauth2/authorize?client_id=791891067309785108&permissions=2147352567&scope=bot)\n\n", inline=False)
    em.add_field(name="Join our support server!", value="[Click here to join the support server](https://discord.gg/wkMuA6TjUD)\n\n", inline=False)
    em.add_field(name="Vote me!", value="[Click here to vote me on top.gg](https://top.gg/bot/791891067309785108/vote)\n[Click here to vote me on discord bot lists](https://discordbotlist.com/bots/glados/upvote)\n\n", inline=False)
    em.add_field(name="Visit My Website!", value="[Click here to visit my website](https://gladosbot.ml/index.html)\n\n")
    await ctx.send(embed=em)

#open_lvl function
async def open_lvl(user):
    users = await get_lvl_data()

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)]["level"] = 1
        users[str(user.id)]["experience"] = 0

    with open("level.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#get_lvl_data function
async def get_lvl_data():
    with open("level.json", "r") as f:
        users = json.load(f)

    return users

#add_experience function
async def add_experience(user, exp):
    users = await get_lvl_data()

    users[str(user.id)]["experience"] += exp

    with open("level.json", "w") as f:
        json.dump(users, f, indent=4)

#level_up function
async def level_up(user):
    users = await get_lvl_data()

    experience = users[str(user.id)]["experience"]
    lvl_start = users[str(user.id)]["level"]
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await user.send(f"Congrats {user.mention}! You have leveled up to level {lvl_end}! Keep going!\n")
        users[str(user.id)]["level"] = lvl_end
        with open("level.json", "w") as f:
            json.dump(users, f, indent=4)

#levelon_open function
async def levelon_open(server):
    users = await levelon_data()

    if str(server.id) in users:
        return False

    else:
        users[str(server.id)] = {}
        users[str(server.id)]["levelon"] = "off"

    with open("levelon.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#levelon_data function
async def levelon_data():
    with open("levelon.json", "r") as f:
        users = json.load(f)

    return users

#on_message event
@client.event
async def on_message(message):
	with open("afk.json", "r") as f:
			afk = json.load(f)

	if message != None:
			if str(message.guild.id) in afk:
					if str(message.author.id) in afk[str(message.guild.id)]:
							del afk[str(message.guild.id)][str(message.author.id)]

							with open("afk.json", "w") as f:
									json.dump(afk, f, indent=4)

							await message.channel.send(f"Welcome back {message.author.mention}! I have removed your afk message now!")

					else:
							try:
									for i in afk[str(message.guild.id)]:
											test = await client.fetch_user(int(i))
											if test in message.mentions:
													m = afk[str(message.guild.id)][i]["message"]
													em = discord.Embed(title=f"{test.name} is currently afk!\n\n{test.name}'s afk message: {m}", color=message.author.color)
													image = afk[str(message.guild.id)][i]["image"]
													
													if image == "None":
															await message.channel.send(embed=em)

													else:
															em.set_image(url=image)
															await message.channel.send(embed=em)

							except:
									pass

	with open('prefixes.json', 'r') as f:
			prefixes = json.load(f)

	with open("filter.json", "r") as f:
			users = json.load(f)

	with open("ig.json", "r") as f:
			ignore = json.load(f)

	if message.author.id != 791891067309785108:
		if str(message.guild.id) in users:
				if str(message.guild.id) in ignore:
						if str(message.channel.id) not in ignore[str(message.guild.id)]:
								x = message.content

								for i in users[str(message.guild.id)]:
										if i in x.lower():
												await message.delete()
												await message.channel.send(f"{message.author.mention}, you can't say that word in this server!")

	if str(message.guild.id) not in prefixes:
			prefixes[str(message.guild.id)] = "$"

			with open("prefixes.json","w") as f:
					json.dump(prefixes,f,indent=4)

	await levelon_open(message.guild)
	users = await levelon_data()
	server = message.guild

	if users[str(server.id)]["levelon"] == "on":
			if message.author.bot == True:
					return

			await open_lvl(message.author)
			await add_experience(message.author, 5)
			await level_up(message.author)

	await client.process_commands(message)

#levelsettings
@client.command()
@commands.has_permissions(manage_channels=True)
async def levelsettings(ctx, mode = None):
    syntax = "```yml\nSyntax: .levelsettings (mode)\nExample Usage: .levelsettings on```"

    if mode == None:
        embed = discord.Embed(title=":negative_squared_cross_mark: Please specify the mode! The mode can only be `on`/`off`\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return     

    if mode.lower() != "on" and mode.lower() != "off":
        embed = discord.Embed(title=":negative_squared_cross_mark: The mode arguement can only be `on`/`off`\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return  

    await levelon_open(ctx.guild)
    users = await levelon_data()

    server = ctx.guild

    if users[str(server.id)]["levelon"] == "on" and mode.lower() == "on":
        embed = discord.Embed(title=":negative_squared_cross_mark: The levelling system is already on!\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return  

    if users[str(server.id)]["levelon"] == "off" and mode.lower() == "off":
        embed = discord.Embed(title=":negative_squared_cross_mark: The levelling system is already off!\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return  

    users[str(server.id)]["levelon"] = mode.lower()

    with open("levelon.json", "w") as f:
        json.dump(users, f, indent=4)

    await ctx.send(f"Successfully changed the levelsettings mode to `{mode.lower()}`")

#level command
@client.command()
async def level(ctx, member: discord.Member = None):
    await levelon_open(ctx.guild)
    users = await levelon_data()
    server = ctx.guild

    if users[str(server.id)]["levelon"] == "on":
        if member == None:
            member = ctx.author

        level = Image.open("level.png")

        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((128,127))

        level.paste(pfp, (105,34))

        await open_lvl(member)
        users = await get_lvl_data()

        draw = ImageDraw.Draw(level)
        font = ImageFont.truetype("level.ttf", 40)

        l = users[str(member.id)]["level"]
        e = users[str(member.id)]["experience"]

        draw.text((355, 75), f": {member.name}", (0, 0, 0), font=font)
        draw.text((232, 180), f": {l}", (0, 0, 0), font=font)
        draw.text((220, 242), f": {e}", (0, 0, 0), font=font)

        level.save("lev.png")

        await ctx.send(file=discord.File("lev.png"))

        return

    await ctx.send("The leveling system is currently off! Inorder to use it turn it on!")

#rank command
@client.command(aliases=["lb"])
async def leaderboard(ctx, x = 3):
    syntax = "```yml\nSyntax: .leaderboard (number)\nExample Usage: .leaderboard 3```"

    if x <= 0:
        embed = discord.Embed(title=":negative_squared_cross_mark: The number can't be less than or equal to 0\n\n", description=syntax, color=discord.Color.red())
        await ctx.send(embed=embed)
        return     

    await levelon_open(ctx.guild)
    users = await levelon_data()
    server = ctx.guild

    if users[str(server.id)]["levelon"] == "off":
        await ctx.send("The leveling system is currently off! Inorder to use it turn it on!")
        return

    users = await get_lvl_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["experience"] + 0
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f"Top {x} experienced people", description="This is decided on the basis of the experience they have!", color=discord.Color.green())
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = ctx.guild.get_member(int(id_))
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)

#all errors

#load error
@load.error
async def load_error(ctx, error):
    await ctx.send(error)

#unload error
@unload.error
async def unload_error(ctx, error):
    await ctx.send(error)

#reload error
@reload.error
async def reload_error(ctx, error):
    await ctx.send(error)

#get_prefix error
@getserver.error
async def get_prefix_error(ctx, error):
    return

#on_command_error error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command is invalid")
        return
        
    raise error

keep_alive.keep_alive()
#run event
token = os.environ.get("Token")
client.run(token)
