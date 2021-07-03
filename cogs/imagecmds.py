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
import time
import datetime
import asyncio
import random
import typing
import PIL

from PIL import Image
from io import BytesIO

class Imagex(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('imagecmds file is ready')

    #wanted command
    @commands.command()
    async def wanted(self, ctx,*, user : discord.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open("wanted.jpg")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((357,280))

        wanted.paste(pfp, (58,232))
        wanted.save("wan.jpg")

        await ctx.send(file=discord.File("wan.jpg"))

    #nyan command
    @commands.command()
    async def nyan(self, ctx,*, user : discord.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open("nyancat.jpg")

        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((319,287))

        wanted.paste(pfp, (215,66))
        wanted.save("neon.jpg")

        await ctx.send(file=discord.File("neon.jpg"))

    #delete command
    @commands.command()
    async def delete(self, ctx, *, member: discord.Member = None):
        if member == None:
            member = ctx.author

        dele = Image.open("delete.png")

        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((82,105))

        dele.paste(pfp, (81,75))
        dele.save("dele.png")

        await ctx.send(file=discord.File("dele.png"))
        await ctx.send("Say `yes` if you want to delete it, otherwise say `no`")

        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 15,
                check = lambda message: message.author == ctx.author and message.channel == ctx.channel)

            if msg:
                if msg.content == "yes":
                    await ctx.send(f"Comp : `Succesfully deleted that trash`")

                elif msg.content == "no":
                    await ctx.send(f"Comp : `Ok, I didn't delete it`")

                else:
                    await ctx.send(f"Comp : `What are thinking?! That's not a valid option is it?`")

        except asyncio.TimeoutError:
            await ctx.send(f'Comp : `You are a turtle, you cant even choose an option in 15 seconds`')

    #meme command
    @commands.command()
    async def meme(self, ctx):
      subreddit = ['memes','dankmeme']
      subredditt = random.choice(subreddit)

      async with aiohttp.ClientSession() as cs:
          async with cs.get(f"https://www.reddit.com/r/{subredditt}/new.json?sort=hot,") as data:
              res = await data.json()
              choose = res['data']['children'] [random.randint(0, 25)]
              title = choose['data']['title']
              standard = 'https://www.reddit.com'
              lin = choose['data']['permalink']
              newlink = standard + lin
              embed = discord.Embed(description= f'[{title}]({newlink})')
              embed.set_image(url= choose['data']['url'] )
              likes = choose['data']['ups']
              replies = choose['data']['num_comments']
              embed.set_footer(text = f'👍 {likes} | 💬 {replies}')
              await ctx.send(embed=embed)

    #avatar command
    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member == None:
            await ctx.send(f"Please mention someone next time of whom you want the avatar of")
            return

        else:
    	    await ctx.send(member.avatar_url)

    #woof command
    @commands.command(aliases=['dog'])
    async def woof(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get ('https://random.dog/woof.json') as r:
                res=await r.json()
                res=res['url']
                em=discord.Embed(title="Woof Woof! :dog:", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)

    #meow command
    @commands.command(aliases=["cat"])
    async def meow(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get ('https://aws.random.cat/meow') as r:
                res=await r.json()
                res=res['file']
                em=discord.Embed(title="Meow Meow! :cat:", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)

    #foxxy command
    @commands.command(aliases=['fox'])
    async def foxxy(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get ('https://some-random-api.ml/img/fox') as r:
                res=await r.json()
                res=res['link']
                em=discord.Embed(title="Fox! :fox:", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)

    #chirp command
    @commands.command(aliases=["bird"])
    async def chirp(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/img/birb') as r:
                res=await r.json()
                res=res['link']
                em=discord.Embed(title="Chirp Chirp! :bird:", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)

    #koalaboi command
    @commands.command(aliases=["koala"])
    async def koalaboi(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/img/koala') as r:
                res=await r.json()
                res=res['link']
                em=discord.Embed(title="Koala! :koala:", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)

    #redpanda command
    @commands.command()
    async def redpanda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/img/red_panda') as r:
                res=await r.json()
                res=res['link']
                em=discord.Embed(title="Red Panda! :panda_face:", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)

    #panda command
    @commands.command()
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/img/panda') as r:
                res=await r.json()
                res=res['link']
                em=discord.Embed(title="Panda! :panda_face:", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)


    #wink command
    @commands.command()
    async def wink(self, ctx,*, member: discord.Member = None):
        if member == None:
            await ctx.send(f"Who you want to wink to? Please mention someone next time!")
            return

        if member == ctx.author:
            await ctx.send(f"You can't wink to yourself!")
            return

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/animu/wink') as r:
                res=await r.json()
                res=res['link']
                em=discord.Embed(title=f"{ctx.author.name} winks {member.name}", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)

    #pat command
    @commands.command()
    async def pat(self, ctx, *, member: discord.Member = None):
        if member == None:
            await ctx.send(f"Who you want to pat? Please mention someone next time!")
            return

        if member == ctx.author:
            await ctx.send(f"You can't pat yourself!")
            return

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/animu/pat') as r:
                res=await r.json()
                res=res['link']
                em=discord.Embed(title=f"{ctx.author.name} pats {member.name}", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)

    #hug command
    @commands.command()
    async def hug(self, ctx, *, member: discord.Member = None):
        if member == None:
            await ctx.send(f"Who you want to hug? Please mention someone next time!")
            return

        if member == ctx.author:
            await ctx.send(f"You can't hug yourself!")
            return

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://some-random-api.ml/animu/hug') as r:
                res=await r.json()
                res=res['link']
                em=discord.Embed(title=f"{ctx.author.name} hugs {member.name}", color=ctx.author.color)
                em.set_image(url=res)
                await ctx.send(embed=em)

def setup(client):
    client.add_cog(Imagex(client))
