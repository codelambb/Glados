import discord
import json
import aiofiles
from discord.ext.commands.errors import ChannelNotFound, MissingPermissions
from discord.utils import get
import asyncio
from discord.ext import commands    

#ignore_filter_data function
async def get_ignore_data():
    with open("ig.json", "r") as f:
        users = json.load(f)

    return users

#open_ignore function
async def open_ignore(server):
    users = await get_ignore_data()

    if str(server) in users:
        return False
    else:
        users[str(server)] = {}

    with open("ig.json","w") as f:
        json.dump(users,f,indent=4)
    return True 

#add_ignore function
async def add_ignore(server, channel):
    users = await get_ignore_data()
    users[str(server)][str(channel)] = 1

    with open("ig.json", "w") as f:
        json.dump(users,f,indent=4)

    return True

#remove_ignore function
async def remove_ignore(server, channel):
    users = await get_ignore_data()
    del users[str(server)][str(channel)]

    with open("ig.json", "w") as f:
        json.dump(users,f,indent=4)

#get_filter_data function
async def get_filter_data():
    with open("filter.json", "r") as f:
        users = json.load(f)

    return users


    return True

#open_filter function
async def open_filter(server):
    users = await get_filter_data()

    if str(server) in users:
        return False
    else:
        users[str(server)] = {}

    with open("filter.json","w") as f:
        json.dump(users,f,indent=4)
    return True 

#add_filter function
async def add_filter(server, word):
    users = await get_filter_data()
    users[str(server)][str(word.lower())] = 1

    with open("filter.json", "w") as f:
        json.dump(users,f,indent=4)

    return True

#remove_filter function
async def remove_filter(server, word):
    users = await get_filter_data()
    del users[str(server)][str(word.lower())]

    with open("filter.json", "w") as f:
        json.dump(users,f,indent=4)

    return True

#get_mail_data function
async def get_mail_data():
    with open("mailchannel.json","r") as f:
        users = json.load(f)

    return users

#open_mail function
async def open_mail(server):
    users = await get_mail_data()

    if str(server) in users:
        return False
    else:
        users[str(server)] = {}
        users[str(server)]["channel"] = "none"

    with open("mailchannel.json","w") as f:
        json.dump(users,f,indent=4)
    return True  

#open_donation function
async def open_donation(server):
    users = await get_donation_data()

    if str(server) in users:
        return False
    else:
        users[str(server)] = {}
        users[str(server)]["switch"] = "off"
        users[str(server)]["channel"] = "none"

    with open("donation_settings.json","w") as f:
        json.dump(users,f,indent=4)
    return True

#get_donation_data function
async def get_donation_data():
    with open("donation_settings.json", "r") as f:
        users = json.load(f)

    return users

#open_modmail function
async def open_modmail(server):
    users = await get_accept_data()

    if str(server) in users:
        return False
    else:
        users[str(server)] = {}
        users[str(server)]["number"] = 1

    with open("id.json","w") as f:
        json.dump(users,f,indent=4)
    return True

#get_modmail_data function
async def get_modmail_data():
    with open("id.json","r") as f:
        users = json.load(f)

    return users

#get_accept_data function
async def get_accept_data():
    with open("accept.json","r") as f:
        users = json.load(f)

    return users

#open_accept function
async def open_accept(server, id_, user):
    users = await get_accept_data()

    if str(server) in users:
        users[str(server)][id_] = user.id

        with open("accept.json","w") as f:
            json.dump(users,f,indent=4)
        return True
    else:
        users[str(server)] = {}
        users[str(server)][id_] = user.id

    with open("accept.json","w") as f:
        json.dump(users,f,indent=4)
    return True

#get_reaction_data function
async def get_reaction_data():
    with open("reaction_roles.json", "r") as f:
        users = json.load(f)

#open_reaction_server function
async def open_reaction_server(server):
    users = await get_reaction_data()

    if str(server) in users:
        return False

    else:
        users[str(server)] = {}

    with open("reaction_roles.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#open_reaction_message function
async def open_reaction_message(server, message):
    users = await get_reaction_data()

    if str(message.id) in users[str(server)]:
        return False

    else:
        users[str(server)][str(message.id)] = {}

    with open("reaction_roles.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#get_rnumber_data function
async def get_rnumber_data():
    with open("rnumber.json", "r") as f:
        users = json.load(f)

#open_number_server function
async def open_number_server(server):
    users = await get_rnumber_data()

    if str(server) in users:
        return False

    else:
        users[str(server)] = {}

    with open("rnumber.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#open_number_message function
async def open_number_message(server, message):
    users = await get_rnumber_data()

    if str(message.id) in users[str(server)]:
        return False

    else:
        users[str(server)][str(message.id)] = {}
        users[str(server)][str(message.id)]["number"] = 1

    with open("rnumber.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#add_number function
async def add_number(server, message):
    number = await get_rnumber_data()
    n = number[str(server)][str(message.id)]["number"]
    number[str(server)][str(message.id)]["number"] = n + 1

    with open("rnumber.json", "w") as f:
        json.dump(number, f, indent=4)

#add_reaction function
async def add_reaction(server, message, emoji, role):
    users = await get_reaction_data()
    number = await get_rnumber_data()
    n = number[str(server)][str(message.id)]["number"]
    users[str(server)][str(message.id)][int(n)] = {}
    users[str(server)][str(message.id)][int(n)][str(emoji)] = str(role.id)

    with open("reaction_roles.json", "w") as f:
        json.dump(users, f, indent=4)

#remove_reaction function
async def remove_reaction(server, message, number):
    users = await get_reaction_data()
    del users[str(server)][str(message.id)][int(number)]

    with open("reaction_roles.json", "w") as f:
        json.dump(users, f, indent=4)

#remove_number function
async def remove_rnumber(server, message):
    users = await get_rnumber_data()
    del users[str(server)][str(message.id)]

    with open("rnumber.json", "w") as f:
        json.dump(users, f, indent=4)

class Configcmds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.reaction_roles = []
        self.client.sniped_messages = {}

        for file in ["reaction_roles.txt"]:
            async with aiofiles.open(file, mode="a") as temp:
                pass

        async with aiofiles.open("reaction_roles.txt", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(" ")
                self.client.reaction_roles.append((int(data[0]), int(data[1]), data[2].strip("\n")))

        print('configcmds file is ready')

    #rr_add command
    @commands.command(aliases=["rr add"])
    @commands.has_permissions(manage_roles=True)
    async def rr_add(self, ctx, message: discord.Message = None, role: discord.Role = None, emoji = None):
        if message == None:
            await ctx.send(f"Please provide the message id next time!")
            return

        if role == None:
            await ctx.send(f"Please provide the role id next time!")
            return

        if emoji == None:
            await ctx.send(f"Please provide a emoji next time!")
            return

        await open_number_server(ctx.guild.id)
        await open_number_message(ctx.guild.id, message)
        await open_reaction_server(ctx.guild.id)
        await open_reaction_message(ctx.guild.id, message)
        users = await get_reaction_data()
        e = emoji.encode("utf-8")
        
        for i in users[str(ctx.guild.id)][str(message.id)]:
            if str(e) in users[str(ctx.guild.id)][str(message.id)][i]:
                await ctx.send(f"That emoji is already assigned to a role in that message!")
                return

        await add_reaction(ctx.guild.id, message, e, role)
        await add_number(ctx.guild.id, message)
        await message.add_reaction(emoji)
        await ctx.send(f"Successfully the reaction role of {role.name} with {emoji} on the message: {message.id}")

    #fignore command
    @commands.command(aliases=["ignore", "ignore_add"])
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def fignore(self, ctx, channel: discord.TextChannel = None):
        await open_ignore(ctx.guild.id)
        users = await get_ignore_data()

        if channel == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide a channel to not be filtered next time!.", color=discord.Color.red())
            await ctx.send(embed=em)
            return          

        if str(channel.id) in users[str(ctx.guild.id)]:
            em = discord.Embed(title="<a:no:801303064178196520> The channel you provided to not being filtered is already there.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        await add_ignore(ctx.guild.id, str(channel.id))

        em = discord.Embed(title="<a:yes:803969799277248542> Successfully done!", color=discord.Color.green())
        await ctx.send(embed=em)

    #rignore command
    @commands.command(aliases=["ignore_remove"])
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def rignore(self, ctx, channel: discord.TextChannel = None):
        await open_ignore(ctx.guild.id)
        users = await get_ignore_data()

        if channel == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide the channel to be removed next time!.", color=discord.Color.red())
            await ctx.send(embed=em)
            return   

        if str(channel.id) not in users[str(ctx.guild.id)]:
            em = discord.Embed(title="<a:no:801303064178196520> The channel you provided to be removed is not there.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        await remove_ignore(ctx.guild.id, str(channel.id))

        em = discord.Embed(title="<a:yes:803969799277248542> Successfully done!", color=discord.Color.green())
        await ctx.send(embed=em)        

    #lignore command
    @commands.command(aliases=["ignore_list"])
    async def lignore(self, ctx):
        await open_ignore(ctx.guild.id)
        users = await get_ignore_data()
        em = discord.Embed(title="Ignored Channel List\n\n", color=ctx.author.color)
        s = 1

        for i in users[str(ctx.guild.id)]:
            if i == None:
                e = discord.Embed(title="Ignored Channel List\n\nThere are no blacklisted channels in this server!", color=ctx.author.color)
                await ctx.send(embed=e)
                return
            em.add_field(name=f"{s})", value=f"<#{i}>\n")
            s += 1

        await ctx.send(embed=em) 

    #filter command
    @commands.command(aliases=["filter"])
    @commands.has_permissions(manage_messages=True)
    async def filter_add(self, ctx, word = None):
        await open_filter(ctx.guild.id)
        users = await get_filter_data()

        if word == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide the word to be filtered next time!.", color=discord.Color.red())
            await ctx.send(embed=em)
            return          

        if str(word.lower()) in users[str(ctx.guild.id)]:
            em = discord.Embed(title="<a:no:801303064178196520> The word you provided to be filtered is already there.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        await add_filter(ctx.guild.id, str(word))

        em = discord.Embed(title="<a:yes:803969799277248542> Successfully done!", color=discord.Color.green())
        await ctx.send(embed=em)

    #fremove command
    @commands.command(aliases=["filter_remove"])
    @commands.has_permissions(manage_messages=True)
    async def fremove(self, ctx, word = None):
        await open_filter(ctx.guild.id)
        users = await get_filter_data()

        if word == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide the word to be removed next time!.", color=discord.Color.red())
            await ctx.send(embed=em)
            return   

        if str(word.lower()) not in users[str(ctx.guild.id)]:
            em = discord.Embed(title="<a:no:801303064178196520> The word you provided to be removed is not there.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        await remove_filter(ctx.guild.id, str(word))

        em = discord.Embed(title="<a:yes:803969799277248542> Successfully done!", color=discord.Color.green())
        await ctx.send(embed=em)        

    #flist command
    @commands.command(aliases=["filter_list"])
    async def flist(self, ctx):
        await open_filter(ctx.guild.id)
        users = await get_filter_data()
        em = discord.Embed(title="Filter List\n\n", color=ctx.author.color)
        s = 1

        for i in users[str(ctx.guild.id)]:
            if i == None:
                e = discord.Embed(title="Filter List\n\nThere are no blacklisted words in this server!", color=ctx.author.color)
                await ctx.send(embed=e)
                return
            em.add_field(name=f"{s})", value=f"{i}\n")
            s += 1

        await ctx.send(embed=em) 

    #reaction_remove
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        for role_id, msg_id, emoji in self.client.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
                await payload.member.add_roles(self.client.get_guild(payload.guild_id).get_role(role_id))
                return

    #reaction_add
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        for role_id, msg_id, emoji in self.client.reaction_roles:
            if msg_id == payload.message_id and emoji == str(payload.emoji.name.encode("utf-8")):
                guild = self.client.get_guild(payload.guild_id)
                member = await self.client.fetch_user(payload.user_id)
                role = get(guild.roles, id=role_id)
                await member.remove_roles(role)
                return

    #set_reaction command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def set_reaction(self, ctx, role: discord.Role=None, msg: discord.Message=None, emoji=None):
        if role != None and msg != None and emoji != None:
            await msg.add_reaction(emoji)
            self.client.reaction_roles.append((role.id, msg.id, str(emoji.encode("utf-8"))))
            
            async with aiofiles.open("reaction_roles.txt", mode="a") as file:
                emoji_utf = emoji.encode("utf-8")
                await file.write(f"{role.id} {msg.id} {emoji_utf}\n")

            await ctx.channel.send("Reaction has been set.")
            
        else:
            await ctx.send("Invalid arguments.")

    #message_delete
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.client.sniped_messages[message.guild.id] = (message.content, message.author, message.channel.name, message.created_at)

    #snipe command
    @commands.command()
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time = self.client.sniped_messages[ctx.guild.id]
            
        except:
            await ctx.channel.send("Couldn't find a message to snipe!")
            return

        embed = discord.Embed(description=contents, color=ctx.author.color, timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
        embed.set_footer(text=f"Deleted in : #{channel_name}")

        await ctx.channel.send(embed=embed)

    #prefix joinset
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "$"

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    #prefix removeset
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        del prefixes[str(guild.id)]

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    #changeprefix command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def changeprefix(self, ctx, prefix = None):

        if prefix == None:
            em = discord.Embed(title="<a:no:801303064178196520> What prefix you want to set for the bot?! Please specify the prefix next time", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully set prefix to `{prefix}`\n\n\n", color=discord.Color.green())
        await ctx.send(embed=em)

    #setdonation command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def setdonation(self, ctx):
        await ctx.send("Please choose the option from below you want to do!\n\n`switch`: Set the donation settings on/off\n\nType either of the options if you want to configure them.")
        
        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 30,
                check = lambda message: message.author == ctx.author
                               and message.channel == ctx.channel
                )

            if msg:
                w = msg.content 

                if w.lower() == "switch":
                    await ctx.send("Please tell if you want to turn the donation system `on` or `off`. Type either of the options out!")

                    try:
                        msg = await self.client.wait_for(
                            "message",
                            timeout = 30,
                            check = lambda message: message.author == ctx.author
                                        and message.channel == ctx.channel
                            )

                        if msg:
                            x = msg.content
                            
                            if x.lower() == "on":
                                await open_donation(ctx.guild.id)
                                users = await get_donation_data()
                                if users[str(ctx.guild.id)]["switch"] == "on":
                                    await ctx.send("The donation system is already on!")
                                    return

                                users[str(ctx.guild.id)]["switch"] = "on"

                                with open("donation_settings.json", "w") as f:
                                    json.dump(users, f, indent=4)

                                await ctx.send("Successfully turned the donation system `on`!")
                                return

                            if x.lower() == "off":
                                await open_donation(ctx.guild.id)
                                users = await get_donation_data()
                                if users[str(ctx.guild.id)]["switch"] == "off":
                                    await ctx.send("The donation system is already off!")
                                    return

                                users[str(ctx.guild.id)]["switch"] = "off"

                                with open("donation_settings.json", "w") as f:
                                    json.dump(users, f, indent=4)

                                await ctx.send("Successfully turned the donation system `off`")
                                return

                            else:
                                await ctx.send("Thats not a valid option?!")
                                return

                    except asyncio.TimeoutError:
                        await ctx.send("You didn't answer in time!")
                        return

                    return

                else:
                    await ctx.send("Thats not a valid option?!")
                    return

        except asyncio.TimeoutError:
            await ctx.send("You didn't answer in time!")
            return

    #donationchannel command
    @commands.command(aliases=["dc"])
    @commands.has_permissions(manage_channels=True)
    async def donationchannel(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            await ctx.send("Please provide a channel next time!")
            return

        await open_donation(ctx.guild.id)
        users = await get_donation_data()
        users[str(ctx.guild.id)]["channel"] = channel.id

        with open("donation_settings.json", "w") as f:
            json.dump(users, f, indent=4)

        await ctx.send(f"Successfully changed the channel for donations to <#{channel.id}>")

    #mailchannel command
    @commands.command(aliases=["mc"])
    @commands.has_permissions(manage_roles=True)
    async def mailchannel(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            await ctx.send("Please provide a channel next time!")
            return

        await open_mail(ctx.guild.id)
        users = await get_mail_data()
        users[str(ctx.guild.id)]["channel"] = channel.id

        with open("mailchannel.json", "w") as f:
            json.dump(users, f, indent=4)

        await ctx.send(f"Successfully changed the channel for the modmail logs to <#{channel.id}>")

    #modmail command
    @commands.command()
    async def modmail(self, ctx):
        await ctx.send("Please see your DM!")
        await ctx.author.send("What is your report for the server?")
        
        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 300,
                check = lambda message: message.author == ctx.author
                                and message.channel == message.channel
                )

            if msg:
                await open_modmail(ctx.guild.id)
                users = await get_modmail_data()
                number = users[str(ctx.guild.id)]["number"]
                await open_mail(ctx.guild.id)
                mail = await get_mail_data()
                x = mail[str(ctx.guild.id)]["channel"]
                channel =  await self.client.fetch_channel(x)

                if channel == "none":
                    await ctx.send("Looks like the channel for the modmail is not setup! Please set it up by using the `mailchannel` command!")
                    return

                users[str(ctx.guild.id)]["number"] += 1
                em = discord.Embed(title=f"ModMail from {ctx.author}\n\n", description=f"Report: {msg.content}\n\n", color=ctx.author.color)
                em.add_field(name="id", value=f"`{number}`")
                em.set_footer(text="Use accept (id) (response) command and cancel (id) (response) command to accept or cancel the modmail")
                await channel.send(embed=em)
                await ctx.author.send(f"Successfully sent a ModMail to the staff with id: `{number}`. The staff will notify you soon about your modmail soon as possible!")
                with open("id.json", "w") as f:
                    json.dump(users, f)
                await open_accept(ctx.guild.id, number, ctx.author)

        except asyncio.TimeoutError:
            await ctx.author.send('You were late to response')

    #accept command
    @commands.command(aliases=["ac"])
    @commands.has_permissions(manage_roles=True)
    async def accept(self, ctx, _id = None, *, response = None):
        if _id == None:
            await ctx.send("Please provide the id next time!")
            return

        if response == None:
            await ctx.send("Please provide a response next time!")
            return

        users = await get_accept_data()
        user = users[str(ctx.guild.id)][_id]
        member = await ctx.guild.fetch_member(int(user))
        await member.send(f"Your modmail in **{ctx.guild.name}** with id: `{_id}` has been accepted! The response from the staff is: **{response}**. If you have any doubts, please DM {ctx.author}")
        del users[str(ctx.guild.id)][_id]

        with open('accept.json','w') as f:
            json.dump(users,f,indent=4)

        await ctx.send(f"Successfully accepted `{_id}` and given the specified response to <@!{user}>")

    #cancel command
    @commands.command(aliases=["ca", "reject"])
    @commands.has_permissions(manage_roles=True)
    async def cancel(self, ctx, _id = None, *, reason = None):
        if _id == None:
            await ctx.send("Please provide the id next time!")
            return

        if reason == None:
            await ctx.send("Please provide a reason next time!")
            return

        users = await get_accept_data()
        user = users[str(ctx.guild.id)][_id]
        member = await ctx.guild.fetch_member(int(user))
        await member.send(f"Your modmail in **{ctx.guild.name}** with id: `{_id}` has been rejected for the following reason: **{reason}**. If you have any doubt please DM {ctx.author} about it.")
        del users[str(ctx.guild.id)][_id]

        with open('accept.json','w') as f:
            json.dump(users,f,indent=4)

        await ctx.send(f"Successfully rejected `{_id}` and given the specified reason to <@!{user}>")

    #all errors

    #fignore error
    @fignore.error
    async def fignore_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
            return

        if isinstance(error, ChannelNotFound):
            await ctx.send("I can't find the channel you provided in this server!")
            return

        else:
            await ctx.send(error)

    #rignore error
    @rignore.error
    async def fremove_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
            return

        if isinstance(error, ChannelNotFound):
            await ctx.send("I can't find the channel you provided in this server!")
            return

        else:
            await ctx.send(error)


    #filter error
    @filter_add.error
    async def filter_add_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
            return

        else:
            await ctx.send(error)

    #fremove error
    @fremove.error
    async def fremove_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
            return

        else:
            await ctx.send(error)

    #setdonation error
    @setdonation.error
    async def setdonation_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
            return

        else:
            await ctx.send(error)

    #mailchannel error
    @mailchannel.error
    async def mailchannel_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
            return

        if isinstance(error, ChannelNotFound):
            await ctx.send("I coudn't find a channel with that name or id")
            return

        else:
            await ctx.send(error)

    #donationchannel error
    @donationchannel.error
    async def donationchannel_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to use this command!")
            return

        if isinstance(error, ChannelNotFound):
            await ctx.send("I coudn't find a channel with that name or id")
            return

        else:
            await ctx.send(error)

    #accept error
    @accept.error
    async def accept_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to use that!")
            return

        else:
            await ctx.send("Coudn't find a modmail with that id!")
            return

    #cancel error
    @cancel.error
    async def cancel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permissions to use that command!")
            return

        else:
            await ctx.send("Coudn't find a modmail with that id!")
            return

    #error handler
    async def on_command_error(self, ctx, error):
        return

def setup(client):
    client.add_cog(Configcmds(client))