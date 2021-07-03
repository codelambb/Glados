from discord.ext.commands.errors import ChannelNotFound, MemberNotFound, RoleNotFound, MissingPermissions
import wikipedia
import aiofiles
import keep_alive
import discord
from discord import File
import json
from discord.ext import commands, tasks
import os
from random import choice
import aiohttp
from random import randint
import datetime
import asyncio
import random
import typing
import praw
import datetime

#open_warn_server function
async def open_warn_server(server, user):

    users = await get_warn_data()

    if str(user.id) in users:
        return False

    else:
        users[str(user.id)] = {}
        users[str(user.id)][str(server)] = 0


    with open("warns.json","w") as f:
        json.dump(users,f,indent=4)
    return True

#get_warn_data function
async def get_warn_data():
    with open("warns.json","r") as f:
        users = json.load(f)

    return users

class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('modcmds file is ready')

    # clear command
    @commands.command(aliases=["cls", "purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, ammount: int = None):
        syntax = str("""```fix\nSyntax:\n\nclear (amount)```""")

        if ammount == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please specify the amount of message to be cleared!\n\n\n", description=syntax, color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if ammount == 0:
            em = discord.Embed(title="<a:no:801303064178196520> You can't clear 0 messages?! Please specify the amount of messages above 0 and below or equal to 100!\n\n\n", color=discord.Color.red())
            em.add_field(name="Syntax", value=syntax)
            await ctx.send(embed=em)

        if ammount > 100:
            em = discord.Embed(title="<a:no:801303064178196520> 100 is the limit of clearing messages at one time\n\n\n", color=discord.Color.red())
            em.add_field(name="Syntax", value=syntax)
            await ctx.send(embed=em)
            return

        await ctx.channel.purge(limit=ammount + 1)
        em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully purged {ammount} messages\n\n\n", color=discord.Color.green())
        await ctx.send(embed=em, delete_after=5)
        return

    #mute command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None, mute_time = None, *, reason = "No reason provided"):
        if member == None:
            em = discord.Embed(title="<a:no:801303064178196520> Who do you want me to mute?! Please mention someone next time", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if member == ctx.author:
            em = discord.Embed(title="<a:no:801303064178196520> You can't mute yourself!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if member.top_role >= ctx.author.top_role:
            em = discord.Embed(title="<a:no:801303064178196520> You can't mute that user cause that user is same or higher than you!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if mute_time == None:
            mute_time = "permenantely"

        if mute_time[-1] != 's' and mute_time[-1] != 'm' and mute_time[-1] != 'h' and mute_time[-1] != 'd' and mute_time != "permenantely":
            em = discord.Embed(title="<a:no:801303064178196520> You need to have your last digit as `s/m/h/d` for example 5h", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not role:
            await ctx.guild.create_role(name='Muted')

            for channel in ctx.guild.channels:
                await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True,
                                              read_messages=True)

        if role in member.roles:
            em = discord.Embed(title="<a:no:801303064178196520> That user is already muted!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if member.bot == True:
            await member.add_roles(role)
            em = discord.Embed(title="<a:yes:803969799277248542> Successfully done!\n\n\n", description=f"Muted <@!{member.id}>\n\nMute Time : {mute_time}\n\nReason : {reason}", color=discord.Color.green())
            await ctx.send(embed=em)

            if mute_time != "permenantely":
                x = 0

                if mute_time[-1] == 's':
                    x = int(mute_time[:-1])
                    await asyncio.sleep(x)
                    await member.remove_roles(role)
                    await ctx.send(f"Unmuted {member.mention} because time is up")

                if mute_time == 'm':
                    x = int(mute_time[:-1]) * 60
                    await asyncio.sleep(x)
                    await member.remove_roles(role)
                    await ctx.send(f"Unmuted {member.mention} because time is up")

                if mute_time == 'h':
                    x = int(mute_time[:-1]) * 3600
                    await asyncio.sleep(x)
                    await member.remove_roles(role)
                    await ctx.send(f"Unmuted {member.mention} because time is up")

                if mute_time == 'd':
                    x = int(mute_time[:-1]) * 86400
                    await asyncio.sleep(x)
                    await member.remove_roles(role)
                    await ctx.send(f"Unmuted {member.mention} because time is up")

                await asyncio.sleep(x)
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} because time is up")

        else:
            await member.add_roles(role)
            em = discord.Embed(title="<a:yes:803969799277248542> Successfully done!\n\n\n", description=f"Muted <@!{member.id}>\n\nMute Time : {mute_time}\n\nReason : {reason}\n\nMuted by : <@!{ctx.author.id}>", color=discord.Color.green())
            await ctx.send(embed=em)
            await member.send(f"You have been muted in {ctx.guild.name}\n\nMuted by : <@!{ctx.author.id}>\n\nMute Time : {mute_time}\n\nReason : {reason}")

            if mute_time != "permenantely":
                x = 0
                
                if mute_time[-1] == 's':
                    x = int(mute_time[:-1])
                    await asyncio.sleep(x)
                    await member.remove_roles(role)
                    await ctx.send(f"Unmuted {member.mention} because time is up")

                if mute_time == 'm':
                    x = int(mute_time[:-1]) * 60
                    await asyncio.sleep(x)
                    await member.remove_roles(role)
                    await ctx.send(f"Unmuted {member.mention} because time is up")

                if mute_time == 'h':
                    x = int(mute_time[:-1]) * 3600
                    await asyncio.sleep(x)
                    await member.remove_roles(role)
                    await ctx.send(f"Unmuted {member.mention} because time is up")

                if mute_time == 'd':
                    x = int(mute_time[:-1]) * 86400
                    await asyncio.sleep(x)
                    await member.remove_roles(role)
                    await ctx.send(f"Unmuted {member.mention} because time is up")

    #nuke command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel: discord.TextChannel = None):
        position = channel.position

        if channel == None:
            em = discord.Embed(title="<a:no:801303064178196520> You did not specify a channel to nuke!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

        if nuke_channel is not None:
            new_channel = await nuke_channel.clone(reason="Has been Nuked!")
            await nuke_channel.delete()
            await new_channel.edit(position=position)
            em = discord.Embed(title=f"THIS CHANNEL HAS BEEN NUKED BY {ctx.author.name}", color=discord.Color.green())
            em.set_image(url="https://i.pinimg.com/originals/47/12/89/471289cde2490c80f60d5e85bcdfb6da.gif")
            await new_channel.send(embed=em)
            emb = discord.Embed(title="<a:yes:803969799277248542> Successfully nuked that channel!", color=discord.Color.green())
            await ctx.send(embed=emb)

        else:
            em = discord.Embed(title=f"<a:no:801303064178196520> No channel named {channel} was found!", color=discord.Color.red())
            await ctx.send(embed=em)

    # unmute command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, *, user: discord.Member = None):

        if user == None:
            em = discord.Embed(title="<a:no:801303064178196520> Who do you want to unmute!? Please mention someone next time", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        rolename = discord.utils.get(ctx.guild.roles, name="Muted")

        if rolename not in user.roles:
            em = discord.Embed(title="<a:no:801303064178196520> That user is not muted!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await user.remove_roles(rolename)
            em = discord.Embed(title="<a:yes:803969799277248542> Successfully done!", color=discord.Color.green())
            await ctx.send(embed=em)

    # unban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member=None):
        if member == None:
            em = discord.Embed(title="<a:no:801303064178196520> Who do you want to unban?! Please mention someone next time", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully unbanned {user.name}#{user.discriminator}", color=discord.Color.green())
                await ctx.send(embed=em)
                return

        em = discord.Embed(title="<a:no:801303064178196520> That user is not banned!", color=discord.Color.red())
        await ctx.send(embed=em)

    # ban command
    @commands.command(aliases=['b'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        if member == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please mention someone next time you want to ban!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            if member.top_role >= ctx.author.top_role:
                em = discord.Embed(title="<a:no:801303064178196520> You cannot ban that user cause that user is higher than or equal as you!", color=discord.Color.red())
                await ctx.send(embed=em)
                return

            elif member == ctx.author:
                em = discord.Embed(title="<a:no:801303064178196520> You can't ban yourself?!", color=discord.Color.red())
                await ctx.send(embed=em)
                return

            else:
                if member.bot == True:
                    await member.ban(reason=reason)

                else:
                     await member.send(f"You have been banned from the server {ctx.guild.name} by {ctx.author.name} because {reason}")
                     await member.ban(reason=reason)

                em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully banned {member}", color=discord.Color.green())
                await ctx.send(embed=em)

    # kick command
    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
        if member == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please mention someone next time you want to kick!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            if member.top_role >= ctx.author.top_role:
                em = discord.Embed(title="<a:no:801303064178196520> You cannot kick that user cause that user is higher than or equal as you!", color=discord.Color.red())
                await ctx.send(embed=em)
                return

            elif member == ctx.author:
                em = discord.Embed(title="<a:no:801303064178196520> You can't kick yourself?!", color=discord.Color.red())
                await ctx.send(embed=em)
                return

            else:
                if member.bot == True:
                    await member.kick(reason=reason)

                else:
                     await member.send(f"You have been kicked from the server {ctx.guild.name} by {ctx.author.name} because {reason}")
                     await member.kick(reason=reason)

                em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully kicked {member}", color=discord.Color.green())
                await ctx.send(embed=em)

    # announcemnt command
    @commands.command(aliases=["ann"])
    @commands.has_permissions(manage_messages=True)
    async def announce(self, ctx, *, message=None):
        if message == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please send the message you want to send announce next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        anno = discord.Embed(title=f"Announcement\n\n{message}", color=ctx.author.color)
        anno.set_footer(text=f"Announcement by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        anno.timestamp = datetime.datetime.utcnow()
        await ctx.send("Type `yes` if you want a image in your annoucement, otherwise type `no`")
        
        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 30,
                check = lambda message: message.author == ctx.author
                               and message.channel == ctx.channel
                )

            if msg:
                t = msg.content

                if t.lower() == "yes":
                    await ctx.send("Please send your image url!")

                    try:
                        msg = await self.client.wait_for(
                            "message",
                            timeout = 30,
                            check = lambda message: message.author == ctx.author
                                           and message.channel == ctx.channel
                            )

                        if msg:
                            anno.set_image(url=msg.content)
                            await ctx.message.delete()
                            await ctx.send(embed=anno)
                            return

                    except asyncio.TimeoutError:
                        await ctx.send('You were late to response')
                        return

                if t.lower() == "no":
                    await ctx.message.delete()
                    await ctx.send(embed=anno)
                    return

                else:
                    await ctx.send("That's not a valid option!")
                    return

        except asyncio.TimeoutError:
            await ctx.send('You were late to response')
            return

    # gstart command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def gstart(self, ctx, duration=None, *, prize=None):
        if duration == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please tell the duratation of the giveaway!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if prize == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please tell the prize of the giveaway!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if duration[-1] != 's' and duration[-1] != 'm' and duration[-1] != 'h' and duration[-1] != 'd':
            em = discord.Embed(title="<a:no:801303064178196520> Please tell the prize of the giveaway!", color=discord.Color.red())
            await ctx.send(embed=em)

        if duration[-1] == 's':
            b = int(duration[0:-1])
        elif duration[-1] == 'm':
            b = int(duration[0:-1]) * 60
        elif duration[-1] == 'h':
            b = int(duration[0:-1]) * 3600
        elif duration[-1] == 'd':
            b = int(duration[0:-1]) * 86400

        else:
            em = discord.Embed(title="<a:no:801303064178196520> You need to have your last digit as `s/m/h/d` for example 5h for your giveaway!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        em = discord.Embed(title=f"**Giveaway!**\n\n\n", description=f"**React with :tada: to enter the giveaway!**\n\nPrize: {prize}\n\nTime Remaining: {duration}\n\nHosted by: <@!{ctx.author.id}>", color=discord.Color.purple())
        em.set_image(url="https://media.discordapp.net/attachments/790570421111750676/800969932128780318/Untitled.png")

        await ctx.message.delete()

        msg = await ctx.send(embed=em)

        await msg.add_reaction("🎉")

        await asyncio.sleep(b)

        new_msg = await ctx.channel.fetch_message(msg.id)

        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)
        new_embed = discord.Embed(title=f"**Giveaway!**\n\n\n", description=f"**React with :tada: to enter the giveaway!**\n\nPrize: {prize}\n\nWinner: <@!{winner.id}>\n\nHosted by: <@!{ctx.author.id}>", color=discord.Color.purple())
        new_embed.set_image(url="https://media.discordapp.net/attachments/790570421111750676/800969932128780318/Untitled.png")
        new_embed.set_footer(text="This giveaway has been ended!")
        await msg.edit(embed=new_embed)

        await ctx.send(f"Congratulations! {winner.mention} won {prize}!:tada::tada:")

    # reroll command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def reroll(self, ctx, channel: discord.TextChannel = None, id_: int = None):

        if channel == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please also mention the channel of the your giveaway next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if id_ == None:
            em = discord.Embed(title="<a:no:801303064178196520> You need to give the id of your giveaway in order to reroll it", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        try:
            msg = await channel.fetch_message(id_)

        except:
            em = discord.Embed(title="<a:no:801303064178196520> The id was enetred incorrectly", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        users = await msg.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)

        await channel.send(f"Congratulations! {winner.mention} won!:tada::tada:")

    #slowmode command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time = None):
        if time == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide the time next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if time[-1] != 's' and time[-1] != 'm' and time[-1] != 'h':
            em = discord.Embed(title="<a:no:801303064178196520> You need to have your last digit for time as `s/m/h` for example 5h", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if time[-1] == 's':
            y = int(time[:-1])
            if y > 21600:
                em = discord.Embed(title="<a:no:801303064178196520> The limit of the slowmode is till 6 hours only!", color=discord.Color.red())
                await ctx.send(embed=em)
                return     

            await ctx.channel.edit(slowmode_delay=y)
            await ctx.send(f"Set the slowmode delay in this channel to {time} seconds!")

        elif time[-1] == 'm':
            x = int(time[:-1]) * 60
            if x > 21600:
                em = discord.Embed(title="<a:no:801303064178196520> The limit of the slowmode is till 6 hours only!", color=discord.Color.red())
                await ctx.send(embed=em)
                return  

            await ctx.channel.edit(slowmode_delay=x)
            await ctx.send(f"Set the slowmode delay in this channel to {time} seconds!")

        elif time[-1] == 'h':
            j = int(time[:-1]) * 3600
            if j > 21600:
                em = discord.Embed(title="<a:no:801303064178196520> The limit of the slowmode is till 6 hours only!", color=discord.Color.red())
                await ctx.send(embed=em)
                return  

            await ctx.channel.edit(slowmode_delay=j)
            await ctx.send(f"Set the slowmode delay in this channel to {time} seconds!")

    #softban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.Member = None, reason=None):
        if user == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please specify a user to be soft banned next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if user == ctx.author:
            em = discord.Embed(title="<a:no:801303064178196520> The user arguement can't be you!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if user.top_role >= ctx.author.top_role:
            em = discord.Embed(title="<a:no:801303064178196520> You can't soft ban that user as that user is higher or same rank as you!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if user.bot == True:
            await user.ban(reason=f"{reason} (Soft Ban)")
            
            banned_users = await ctx.guild.bans()
            u = f"{user.name}#{user.discriminator}"
            user_name, user_discriminator = u.split('#')

            for ban_entry in banned_users:
                member = ban_entry.user

                if (member.name, member.discriminator) == (user_name, user_discriminator):
                    await ctx.guild.unban(member)
                    em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully soft banned {member.name}#{member.discriminator}", color=discord.Color.green())
                    await ctx.send(embed=em)
                    return

            return

        await user.send(f"You have been soft banned from {ctx.guild.name} by {ctx.author} for {reason}")
        await user.ban(reason=f"{reason} (Soft Ban)")
        
        banned_users = await ctx.guild.bans()
        u = f"{user.name}#{user.discriminator}"
        user_name, user_discriminator = u.split('#')

        for ban_entry in banned_users:
            member = ban_entry.user

            if (member.name, member.discriminator) == (user_name, user_discriminator):
                await ctx.guild.unban(member)
                em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully soft banned {member.name}#{member.discriminator}", color=discord.Color.green())
                await ctx.send(embed=em)
                return

    #addrole command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member = None, role: discord.Role = None):
        if member == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide a member to give role to next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if role == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide the role to given to the member next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if role >= ctx.author.top_role:
            em = discord.Embed(title="<a:no:801303064178196520> Looks like the role you have provided is higher than or equal as you that's why you can't have it", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        await member.add_roles(role)
        em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully added {role.name} to {member.name}", color=discord.Color.green())
        await ctx.send(embed=em)

    #removerole command
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member = None, role: discord.Role = None):
        if member == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide a member to remove role from to next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if role == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide the role to be removed from the member next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if role >= ctx.author.top_role:
            em = discord.Embed(title="<a:no:801303064178196520> Looks like the role you have provided is higher than or equal as you that's why you can't have it", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        await member.remove_roles(role)
        em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully removed {role.name} from {member.name}", color=discord.Color.green())
        await ctx.send(embed=em)

    #lock command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.message.channel

        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully done!\n\n", description=f":lock: I have successfully locked <#{channel.id}> for the server's default role!", color=discord.Color.green())
        await ctx.send(embed=em)

    #unlock command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.message.channel

        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully done!\n\n", description=f":unlock: I have successfully unlocked <#{channel.id}> for the server's default role!", color=discord.Color.green())
        await ctx.send(embed=em)

    #nick command
    @commands.command(aliases=["nickname"])
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nick = None):
        if member == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide a member to change his/her nickname next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if nick == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide the nickname next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if member.top_role >= ctx.author.top_role and member != ctx.author:
            em = discord.Embed(title="<a:no:801303064178196520> You can't change the nickname of that user as that user is same or higher than you!", color=discord.Color.red())
            await ctx.send(embed=em)
            return            

        await member.edit(nick=nick)
        await ctx.send(f"Successfully changed {member.mention} nickname to {nick}")

    #all errors

    #nick error
    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return  

        if isinstance(error, MemberNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a member with that name/id.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)

    #lock error
    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return  

        if isinstance(error, ChannelNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a channel with that name/id.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)

    #unlock error
    @unlock.error
    async def unlock_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return  

        if isinstance(error, ChannelNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a channel with that name/id.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            ctx.send(error)

    #addrole error
    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return  

        if isinstance(error, MemberNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a member with that name.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, RoleNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a role with that name or id in this server.", color=discord.Color.red())
            await ctx.send(embed=em)
            return    

    #removerole error
    @removerole.error
    async def removerole_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return  

        if isinstance(error, MemberNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a member with that name.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, RoleNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a role with that name or id in this server.", color=discord.Color.red())
            await ctx.send(embed=em)
            return   

    #reroll error
    @reroll.error
    async def reroll_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, commands.MessageNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a message with that id", color=discord.Color.red())
            await ctx.send(embed=em)
            return        

        if isinstance(error, commands.ChannelNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a channel with that id", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

    #softban error
    @softban.error
    async def softban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, commands.MemberNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a member with that name.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

    #giveaway error
    @gstart.error
    async def gstart_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

    # announce error
    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

    # ban error
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, commands.MemberNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a member with that name.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return        

    # unban error
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send("Thats not a valid user!")
            return     

    # kick error
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, commands.MemberNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a member with that name.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

    #slowmode error
    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

    # mute error
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, commands.MemberNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a member with that name.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

    # unmute error
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, commands.MemberNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a member with that name.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

    #nuke error
    @nuke.error
    async def nuke_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, commands.ChannelNotFound):
            em = discord.Embed(title="<a:no:801303064178196520> I coudn't find a channel with that name/id.", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

    # clear error
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            em = discord.Embed(title="<a:no:801303064178196520> You dont have permissions to use that?!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if isinstance(error, Exception):
            em = discord.Embed(title="<a:no:801303064178196520> I don't have permissions to do that!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        else:
            await ctx.send(error)
            return

def setup(client):
    client.add_cog(Mod(client))
