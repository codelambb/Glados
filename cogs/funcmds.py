import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown
import json
import requests
import random
from random import choice
from random import randint
import asyncio
import random_word
from random_word import RandomWords
import pyfiglet
import prsaw
from prsaw import RandomStuffV2  

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


r = RandomWords()

#marry open
async def open_marry(user):

    u = await get_marry_data()

    if str(user.id) in u:
        return False
    else:
        u[str(user.id)] = {}
        u[str(user.id)]["married"] = "No one"

    with open("marry.json","w") as f:
        json.dump(u,f,indent=4)
    return True

#open_marryx
async def open_marryx(user):

    u = await get_marry_data()

    if str(user) in u:
        return False
    else:
        u[str(user)] = {}
        u[str(user)]["married"] = "No one"

    with open("marry.json","w") as f:
        json.dump(u,f,indent=4)
    return True

#marry data
async def get_marry_data():
    with open("marry.json","r") as f:
        users = json.load(f)

        return users

#open_account function
async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json","w") as f:
        json.dump(users,f)
    return True

#get_bank_data function
async def get_bank_data():
    with open("mainbank.json","r") as f:
        users = json.load(f)

    return users

#update_bank function
async def update_bank(user, change = 0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal

#open_rep function
async def open_rep(user):

    users = await get_rep_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["reputation"] = 0

    with open("rep.json","w") as f:
        json.dump(users,f, indent=4)
    return True

#get_rep_data function
async def get_rep_data():
    with open("rep.json","r") as f:
        users = json.load(f)

    return users

#winner check function
def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

#get_ai_data function
async def get_ai_data():
    with open("ai.json", "r") as f:
        users = json.load(f)

    return users

#open_ai function
async def open_ai(server):
    users = await get_ai_data()

    if str(server) in users:
        return False

    else:
        users[str(server)] = {}

    with open("ai.json", "w") as f:
        json.dump(users, f, indent=4)

    return True

#add_ai function
async def add_ai(server, channel):
    users = await get_ai_data()

    if str(channel) in users[str(server)]:
        return False

    else:
        users[str(server)][str(channel)] = 1

    with open("ai.json", "w") as f:
        json.dump(users, f, indent=4)

    return True

#remove_ai function
async def remove_ai(server, channel):
    users = await get_ai_data()

    if str(channel) not in users[str(server)]:
        return False

    else:
        del users[str(server)][str(channel)]

    with open("ai.json", "w") as f:
        json.dump(users, f, indent=4)

    return True

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('funcmds file is ready')

    #aistart command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def aistart(self, ctx):
        await open_ai(ctx.guild.id)
        users = await get_ai_data()

        if str(ctx.channel.id) in users[str(ctx.guild.id)]:
            await ctx.send(f"Ai-chat is already on in this channel!")
            return

        await add_ai(ctx.guild.id, ctx.channel.id)
        await ctx.send(f"Successfully enabled Ai-chat in this channel!")

    #aistop command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def aistop(self, ctx):
        await open_ai(ctx.guild.id)
        users = await get_ai_data()

        if str(ctx.channel.id) not in users[str(ctx.guild.id)]:
            await ctx.send(f"Ai-chat is not enabled in this channel!")
            return

        await remove_ai(ctx.guild.id, ctx.channel.id)
        await ctx.send(f"Successfully disabled Ai-chat in this channel!")
 
    #aichat command
    @commands.command()
    async def aichat(self, ctx, *, message):
        await open_ai(ctx.guild.id)
        users = await get_ai_data()

        if str(ctx.channel.id) in users[str(ctx.guild.id)]:
            rs = RandomStuffV2()
            response = rs.get_ai_response(message)
            await ctx.message.reply(response)

        elif ctx.author.id == 791891067309785108:
            return

        else:
            await ctx.send(f"I can't chat with you in this channel! Use `aichannel` command to see in which channels I can talk with you")

    #aichannel command
    @commands.command(aliases=["ailist"])
    async def aichannel(self, ctx):
        await open_ai(ctx.guild.id)
        users = await get_ai_data()
        em = discord.Embed(title=f"{ctx.guild.name}'s Ai-Channels -:", color=ctx.author.color)
        s = 1

        for i in users[str(ctx.guild.id)]:
            em.add_field(name=f"{s})", value=f"<#{int(i)}>")
            s += 1

        await ctx.send(embed=em)

    #tictactoe command
    @commands.command(aliases=["tao"])
    async def tictactoe(self, ctx, p2: discord.Member):
        await ctx.send(f"{p2.mention}, {ctx.author.mention} invites you to play a game of tic tac toe with him/her. Say `yes` if you want to otherwise `no`")
        
        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 30,
                check = lambda message: message.author == p2
                               and message.channel == ctx.channel
                )

            if msg:
                e = msg.content
                if e.lower() == "yes":
                    global count
                    global player1
                    global player2
                    global turn
                    global gameOver

                    if gameOver:
                        global board
                        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                                ":white_large_square:", ":white_large_square:", ":white_large_square:",
                                ":white_large_square:", ":white_large_square:", ":white_large_square:"]
                        turn = ""
                        gameOver = False
                        count = 0

                        player1 = ctx.author
                        player2 = p2

                        # print the board
                        line = ""
                        for x in range(len(board)):
                            if x == 2 or x == 5 or x == 8:
                                line += " " + board[x]
                                await ctx.send(line)
                                line = ""
                            else:
                                line += " " + board[x]

                        # determine who goes first
                        num = random.randint(1, 2)
                        if num == 1:
                            turn = player1
                            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
                        elif num == 2:
                            turn = player2
                            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")

                if e.lower() == "no":
                    await ctx.send(f"You declined {ctx.author.name}'s invite!")
                    return

                else:
                    await ctx.send("Thats now a valid option?!")
                    return

        except asyncio.TimeoutError:
            await ctx.send(f"You didn't respond in time!")
            return

        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")
            return

    #place command
    @commands.command()
    async def place(self, ctx, pos: int):
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    print(count)
                    if gameOver == True:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send("Please start a new game using the !tictactoe command.")

    #decipher command
    @commands.command()
    async def decipher(self, ctx):
        w = r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1, maxDictionaryCount=10, minLength=5, maxLength=10)
        reversed_string = w[::-1]
        await ctx.send(f"You must decipher `{reversed_string}` in 30 seconds!")

        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 30,
                check = lambda message: message.author == ctx.author
                               and message.channel == ctx.channel
                )

            if msg:
                if msg.content == w:
                    await ctx.send(f"You got it right! the word was `{w}`")

                else:
                    await ctx.send(f"Wrong answer.. the word was `{w}`")

        except asyncio.TimeoutError:
            await ctx.send(f"You didn't decipher the word in time! The word was `{w}`")

    #minecraft command
    @commands.command()
    async def minecraft(self, ctx,*, arg):
        e = requests.get('https://api.minehut.com/server/' + arg + '?byName=true')
        json_data = e.json()

        description = json_data["server"]["motd"]
        online = str(json_data["server"]["online"])
        playerCount = str(json_data["server"]["playerCount"])

        embed = discord.Embed(
            title=arg + " Server Info",
            description='Description: ' + description + '\nOnline: ' + online + '\nPlayers: ' + playerCount,
            color=discord.Color.dark_green()
        )
        embed.set_thumbnail(
            url="https://i1.wp.com/www.craftycreations.net/wp-content/uploads/2019/08/Grass-Block-e1566147655539.png?fit=500%2C500&ssl=1")

        await ctx.send(embed=embed)

    #profile command
    @commands.command()
    async def profile(self, ctx, *, member : discord.Member = None):
        if member == None:
            member = ctx.author
            await open_marry(ctx.author)
            await open_account(ctx.author)
            user = ctx.author
            users = await get_marry_data()
            bal = await get_bank_data()
            await open_rep(ctx.author)
            reps = await get_rep_data()

            marriage_user = users[str(user.id)]["married"]

            e = int(bal[str(user.id)]["wallet"]) + int(bal[str(user.id)]["bank"])

            r = reps[str(user.id)]["reputation"]

            if marriage_user == "No one":
                em = discord.Embed(title=f"{ctx.author.name}'s profile", color = ctx.author.color)
                em.add_field(name="Married to", value=f"No one", inline=True)
                em.add_field(name="Balance", value=f"{e} :coin:", inline=True)
                em.add_field(name="Reputation Points", value=r, inline=False)
                em.set_thumbnail(url=ctx.author.avatar_url)
                if member.id == 586844180681195530:
                    em.add_field(name="Rank", value="[Creator of Glados](https://gladosbot.ml)", inline=False)
                
                if member.id == 746026228082802699:
                    em.add_field(name="Rank", value="[Website Developer of Glados](https://gladosbot.ml)", inline=False)
                    
                if member.id == 699767957374500941:
                    em.add_field(name="Rank", value="[Head Website Developer of Glados](https://gladosbot.ml)", inline=False)

                if member.id == 789816228423139369:
                    em.add_field(name="Rank", value="[Creator of Glados](https://gladosbot.ml)", inline=False)

                await ctx.send(embed=em)
                return

            o = discord.Embed(title=f"{ctx.author.name}'s profile", color = ctx.author.color)
            o.add_field(name="Married to", value=f"<@{marriage_user}>", inline=True)
            o.add_field(name="Balance", value=f"{e} :coin:", inline=True)
            o.add_field(name="Reputation Points", value=r, inline=False)
            o.set_thumbnail(url=ctx.author.avatar_url)
            if member.id == 586844180681195530:
                o.add_field(name="Rank", value="[Creator of Glados](https://gladosbot.ml)", inline=False)
            
            if member.id == 746026228082802699:
                o.add_field(name="Rank", value="[Website Developer of Glados](https://gladosbot.ml)", inline=False)
                
            if member.id == 699767957374500941:
                o.add_field(name="Rank", value="[Head Website Developer of Glados](https://gladosbot.ml)", inline=False)

            if member.id == 789816228423139369:
                o.add_field(name="Rank", value="[Creator of Glados](https://gladosbot.ml)", inline=False)

            await ctx.send(embed=o)

        else:
            await open_marry(member)
            await open_account(member)
            user = member
            users = await get_marry_data()
            bal = await get_bank_data()
            reps = await open_rep(member)
            reps = await get_rep_data()

            marriage_user = users[str(user.id)]["married"]

            e = int(bal[str(user.id)]["wallet"]) + int(bal[str(user.id)]["bank"])

            r = int(reps[str(user.id)]["reputation"])

            if marriage_user == "No one":
                em = discord.Embed(title=f"{member.name}'s profile", color = ctx.author.color)
                em.add_field(name="Married to", value=f"No one", inline=True)
                em.add_field(name="Balance", value=f"{e} :coin:", inline=True)
                em.add_field(name="Reputation Points", value=r, inline=False)
                em.set_thumbnail(url=member.avatar_url)

                if member.id == 586844180681195530:
                    em.add_field(name="Rank", value="[Creator of Glados](https://gladosbot.ml)", inline=False)
                
                if member.id == 746026228082802699:
                    em.add_field(name="Rank", value="[Website Developer of Glados](https://gladosbot.ml)", inline=False)
                    
                if member.id == 699767957374500941:
                    em.add_field(name="Rank", value="[Head Website Developer of Glados](https://gladosbot.ml)", inline=False)

                if member.id == 789816228423139369:
                    em.add_field(name="Rank", value="[Creator of Glados](https://gladosbot.ml)", inline=False)

                await ctx.send(embed=em)
                return

            x = discord.Embed(title=f"{member.name}'s profile", color = ctx.author.color)
            x.add_field(name="Married to", value=f"<@{marriage_user}>", inline=True)
            x.add_field(name="Balance", value=f"{e} :coin:", inline=True)
            x.add_field(name="Reputation Points", value=r, inline=False)
            x.set_thumbnail(url=member.avatar_url)

            if member.id == 586844180681195530:
                x.add_field(name="Rank", value="[Creator of Glados](https://gladosbot.ml)", inline=False)
            
            if member.id == 746026228082802699:
                x.add_field(name="Rank", value="[Website Developer of Glados](https://gladosbot.ml)", inline=False)
                
            if member.id == 699767957374500941:
                x.add_field(name="Rank", value="[Head Website Developer of Glados](https://gladosbot.ml)", inline=False)

            if member.id == 789816228423139369:
                x.add_field(name="Rank", value="[Creator of Glados](https://gladosbot.ml)", inline=False)

            await ctx.send(embed=x)

    #ascii command
    @commands.command(aliases=["ascii"])
    async def _ascii(self, ctx, *, text=None):
        if text == None:
            await ctx.send("Please provide a text next time!")
            return

        if len(text) > 500:
            await ctx.send("Please provide a shorter text next time!")
            return

        result = pyfiglet.figlet_format(text) 
        await ctx.send(f"```{result}```")

    #giverep command
    @commands.command()
    @cooldown(1,1800,BucketType.user)
    async def giverep(self, ctx, *, member: discord.Member = None):
        if member == None:
            await ctx.send(f"To whom do you want to give reputation point!? Please mention someone next time")
            return

        if member == ctx.author:
            await ctx.send(f"You can't give a reputaion point to yourself?")
            return

        await open_rep(member)
        user = member
        users = await get_rep_data()

        users[str(user.id)]["reputation"] += 1

        with open("rep.json","w") as f:
            json.dump(users,f,indent=4)

        await ctx.send(f"Successfully given 1 reputation point to {member.mention} :tada:")

    #divorce command
    @commands.command()
    async def divorce(self, ctx):
        await open_marry(ctx.author)
        user = ctx.author
        users = await get_marry_data()

        marriage_user = users[str(user.id)]["married"]

        await open_marryx(marriage_user)

        if users[str(user.id)]["married"] == "No one":
            await ctx.send(f"You are not married to anyone")
            return

        users[str(marriage_user)]["married"] = "No one"

        users[str(user.id)]["married"] = "No one"

        with open("marry.json","w") as f:
            json.dump(users,f)

        await ctx.send(f"You have successfully divorced with your marriage partner")

    #marry command
    @commands.command()
    async def marry(self, ctx, *, member : discord.Member = None):
        await open_marry(ctx.author)
        await open_marry(member)
        user = ctx.author
        users = await get_marry_data()

        if users[str(user.id)]["married"] != "No one":
            await ctx.send(f"You are already married to someone!")
            return

        if users[str(member.id)]["married"] != "No one":
            await ctx.send(f"That user is already married to someone!")
            return

        if member == ctx.author:
            await ctx.send(f"You can't marry yourself!")
            return

        if member == None:
            await ctx.send(f'Whom you want to marry? you didnt mention someone to marry!')
            return

        await ctx.send(f'{member.mention} has 60 seconds to accept the proposal from {ctx.author.mention}. Say ``yes`` if you accept otherwise say ``no``')

        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 60,
                check = lambda message: message.author == member
                               and message.channel == ctx.channel
                )

            if msg:
                if msg.content == "yes":
                    await ctx.send(f"{member.mention} has accepted {ctx.author.mention}'s proposal! Congrats you guys are married now!!:tada::tada:")
                    users[str(user.id)]["married"] = member.id
                    users[str(member.id)]["married"] = ctx.author.id

                    with open("marry.json","w") as f:
                        json.dump(users,f)
                    return

                elif msg.content == "no":
                    await ctx.send(f"{member.mention} has rejected {ctx.author.mention}'s proposal..")
                    return

                elif msg.content == "Yes":
                    await ctx.send(f"{member.mention} has accepted {ctx.author.mention}'s proposal! Congrats you guys are married now!!:tada::tada:")
                    users[str(user.id)]["married"] = member.id
                    users[str(member.id)]["married"] = ctx.author.id

                    with open("marry.json","w") as f:
                        json.dump(users,f)
                    return

                elif msg.content == "No":
                    await ctx.send(f"{member.mention} has rejected {ctx.author.mention}'s proposal..")
                    return

                elif msg.content == "YES":
                    await ctx.send(f"{member.mention} has accepted {ctx.author.mention}'s proposal! Congrats you guys are married now!!:tada::tada:")
                    users[str(user.id)]["married"] = member.id
                    users[str(member.id)]["married"] = ctx.author.id

                    with open("marry.json","w") as f:
                        json.dump(users,f)
                    return

                elif msg.content == "NO":
                    await ctx.send(f"{member.mention} has rejected {ctx.author.mention}'s proposal..")
                    return

                else:
                    await ctx.send(f"That's not a valid response for the proposal!")
                    return

        except asyncio.TimeoutError:
            await ctx.send(f'You were late to response')

    #simprate command
    @commands.command()
    async def simprate(self, ctx):
        a = random.randint(20,100)
        await ctx.send(f"Your simprate is {a}%")

    #kill command
    @commands.command()
    async def kill(self, ctx, *, user : discord.Member):

        if user == None:
            await ctx.send(f"Who you want to kill? Please mention someone next time")

        if user == ctx.author:
            await ctx.send(f"Ok, your dead now please tag different person except you to kill")
            return

        else:
            k = random.randint(0,9)

            if k == 0:
                await ctx.send(f'You challenged {user.mention} to a fist fight to the death. You won.')
            
            if k == 1:
                await ctx.send(f"{user.mention} was sucked into the **black hole** and died.")
            
            if k == 2:
                await ctx.send(f'{user.mention} had a mid air collision with nyan-cat')
            
            if k == 3:
                await ctx.send(f'{user.mention} fell down a cliff while playing Pokemon Go. Good job on keeping your nose in that puny phone. :iphone:')
            
            if k == 4:
                await ctx.send(f"{user.mention} presses a random button and is teleported to the height of 100m, allowing them to fall to their inevitable death.\nMoral of the story: Don't go around pressing random buttons.")
            
            if k == 5:
                await ctx.send(f'{user.mention} is sucked into Minecraft. {user.mention}, being a noob at the so called Real-Life Minecraft faces the Game Over screen.')
            
            if k == 6:
                await ctx.send(f"{user.mention} died because RemindMeBot forgot to remind them to breathe")
            
            if k == 7:
                await ctx.send(f"{user.mention} got roasted by {ctx.author.mention} and died")

            if k == 8:
                await ctx.send(f"{user.mention} died a brutal death cause {user.mention} tried inventing the airplane before the Wright Brothers")

            if k == 9:
                await ctx.send(f"{user.mention} was burnt to a crisp by {ctx.author.mention} using BREAD")

    #8ball command
    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, querry = None):
    	responses = ["It is certain.",
    				"It is decidedly so.",
    				"Without a doubt.",
    				"Yes - definitely.",
    				"You may rely on it.",
    				"As I see it, yes.",
    				"Most likely.",
    				"Outlook good.",
    				"Yes.",
    				"Signs point to yes.",
    				"Reply hazy, try again.",
    				"Ask again later.",
    				"Better not tell you now.",
    				"Cannot predict now.",
    				"Concentrate and ask again.",
    				"Don't count on it.",
    				"My reply is no.",
    				"My sources say no.",
    				"Outlook not so good.",
    				"Very doubtful."]

    	await ctx.send(f'{random.choice(responses)}')

    #spc command
    @commands.command()
    async def spc(self, ctx):
        await ctx.send(f"Alright! Please choose your move! Type ``s`` for stone, ``p`` for paper and ``sc`` for scissor. You have 15 seconds to choose your move!")

        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 15,
                check = lambda message: message.author == ctx.author and message.channel == ctx.channel)

            if msg:
                if msg.content == "s":
                    response = ["Stone","Scissor","Paper"]
                    x = random.choice(response)

                    if x == "Stone":
                        await ctx.send(f"Its a draw.. You choose Stone and The comp choose Stone too!")
                        return

                    elif x == "Scissor":
                        await ctx.send(f"You won! You choose Stone and The comp choose Scissor!")
                        return

                    elif x == "Paper":
                        await ctx.send(f"You lose.. You choose Stone and The comp choose Paper.")
                        return

                elif msg.content == "p":
                    response = ["Stone","Scissor","Paper"]
                    x = random.choice(response)

                    if x == "Stone":
                        await ctx.send(f"You won! You choose Paper and The comp choose Stone!")
                        return

                    elif x == "Scissor":
                        await ctx.send(f"You lose.. You choose Paper and The comp choose Scissor.")
                        return

                    elif x == "Paper":
                        await ctx.send(f"Its a draw.. You choose Paper and The comp choose Paper too!")
                        return

                elif msg.content == "sc":
                    response = ["Stone","Scissor","Paper"]
                    x = random.choice(response)

                    if x == "Stone":
                        await ctx.send(f"You lose.. You choose Scissor and The comp choose Stone.")
                        return

                    elif x == "Scissor":
                        await ctx.send(f"Its a draw.. You choose Scissor and The comp choose Scissor too!")
                        return

                    elif x == "Paper":
                        await ctx.send(f"You won! You choose Scissor and The comp choose Paper!")
                        return

                else:
                    await ctx.send(f"What are you thinking? That's not a valid move!")
                    return

        except asyncio.TimeoutError:
            await ctx.send(f'You were late to choose a move')

    #all errors

    #giverep error
    @giverep.error
    async def giverep_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"You need to wait ``{error.retry_after:,.2f}`` to use that command again")

    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 2 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

    @place.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")

    @_ascii.error
    async def ascii_error(self, ctx, error):
        await ctx.send("I can't send the ascii of that long text. Please make it shorter!")
        return

def setup(client):
    client.add_cog(Fun(client))
