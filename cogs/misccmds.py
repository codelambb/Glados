from cogs.configcmds import get_donation_data, open_donation
import wikipedia
import requests
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
import time
import datetime
import asyncio
import random
import typing
import praw

#get_afk_data function
async def get_afk_data():
    with open("afk.json", "r") as f:
        users = json.load(f)

    return users

#open_afk function
async def open_afk(server):
    users = await get_afk_data()

    if str(server) in users:
        return False

    else:
        users[str(server)] = {}

    with open("afk.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

#add_afk function
async def add_afk(server, user, message, image):
    users = await get_afk_data()

    users[str(server)] = {}
    users[str(server)][str(user.id)] = {}
    users[str(server)][str(user.id)]["message"] = message
    users[str(server)][str(user.id)]["image"] = image

    with open("afk.json", "w") as f:
        json.dump(users,f,indent=4)
    return True

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('misccmds file is ready')

    #afk command
    @commands.command()
    async def afk(self, ctx, *, message = None):
        await open_afk(ctx.guild.id)

        if message == None:
            await ctx.send("Please provide a message to be sent when somone pings you while your afk next time!")
            return          

        await ctx.send("Do you want any gif to your afk embed? If yes then type `yes` otherwise type `no`")
        em = discord.Embed(title=f"<a:yes:803969799277248542> Successfully done!\n\nAfk message: {message}", color=discord.Color.green())

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
                            em.set_image(url=msg.content)
                            await ctx.send(embed=em)
                            await add_afk(ctx.guild.id, ctx.author, message, msg.content)
                            return

                    except asyncio.TimeoutError:
                        await ctx.send(f'You were late to response')
                        return

                if t.lower() == "no":
                    await add_afk(ctx.guild.id, ctx.author, message, "None")
                    await ctx.send(embed=em)
                    return

                else:
                    await ctx.send("That's not a valid option!")
                    return

        except asyncio.TimeoutError:
            await ctx.send(f'You were late to response')
            return

    #define command
    @commands.command()
    async def define(self, ctx, *, ask=None):
        if ask == None:
            await ctx.send(f"What do you want the definition in the wikipedia?! Please tell next time")
            return

        definition = wikipedia.summary(ask, sentences=3, chars=1000, auto_suggest=False, redirect=True)
        search = discord.Embed(color=ctx.author.color)
        search.add_field(name=ask, value=definition, inline=False)
        await ctx.send(embed=search)

    #server info command
    @commands.command(aliases=["si"])
    async def serverinfo(self, ctx):
        name = str(ctx.guild.owner)
        description = str(ctx.guild.description)

        owner = ctx.guild.owner
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)

        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)

        await ctx.send(embed=embed)

    # userinfo command
    @commands.command(aliases=["ui"])
    async def userinfo(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send(f"Please mention someone next time of whom you want the userinfo of")
            return

        em = discord.Embed(color=member.color)

        em.set_author(name=f"{member.name}'s info")
        em.set_thumbnail(url=member.avatar_url)
        em.set_footer(text=f"Requested by {ctx.author.name}")

        em.add_field(name='Member Name', value=member.name)
        em.add_field(name="Member name in guild", value=member.display_name)

        em.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        await ctx.send(embed=em)

    #suggest command
    @commands.command()
    async def suggest(self, ctx, *, message=None):
        if message == None:
            await ctx.send(f"Please send a message you want to suggest next time")
            return

        await ctx.message.delete()
        em = discord.Embed(title="Suggestion", description=message, color=ctx.author.color)
        em.set_footer(text=f"Suggestion by {ctx.author.name}")
        message_ = await ctx.send(embed=em)
        await message_.add_reaction("✅")
        await message_.add_reaction("❎")

    #donate command
    @commands.command()
    async def donate(self, ctx, *, donation = None):
        if donation == None:
            await ctx.send("Please provide what you want to donate next time!")
            return

        await open_donation(ctx.guild.id)
        users = await get_donation_data()

        if users[str(ctx.guild.id)]["switch"] == "off":
            await ctx.send("Looks like the donation system is off in this server!")
            return

        if users[str(ctx.guild.id)]["channel"] == "none":
            await ctx.send("Look like the donation system dosen't have a channel setup!")
            return

        channel = self.client.get_channel(users[str(ctx.guild.id)]["channel"])
        em = discord.Embed(title="Dontation Request!", description=f"Sponser: <@!{ctx.author.id}>\n\nDonation: {donation}")
        em.set_thumbnail(url="https://i.pinimg.com/originals/42/7a/85/427a85c007c56a475da6e7cdffa9ee13.gif")

        e = await channel.send(embed=em)
        await e.add_reaction("✅")
        await e.add_reaction("❎")

        x = users[str(ctx.guild.id)]["channel"]
        await ctx.send(f"Successfully sent your donation request to <#{x}>")

    # all errors

    # define error
    @define.error
    async def define_error(self, ctx, error):
        await ctx.send(f"The bot could not find the definition of your querry.")
        return

    #afk error
    @afk.error
    async def afk_error(self, ctx, error):
        await ctx.send(f"The bot coudn't add that image to the embed for some reason try a new image!")
        return

def setup(client):
    client.add_cog(Misc(client))
