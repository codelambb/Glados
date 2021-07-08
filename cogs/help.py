import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('help file is ready')

    #help command
    @commands.command()
    async def help(self, ctx):
        em = discord.Embed(title="**Help Menu**", color = ctx.author.color)
        em.add_field(name="**:question: Info about us!**", value="`Type info`", inline=True)
        em.add_field(name="**<a:yes:803969799277248542> Support us!**", value="`Type supportus`\n", inline=True)
        em.add_field(name="**<:b_ban:813998683842150431> Moderation Command Menu**", value="`Type modhelp to access Moderation Command Menu`\n\n", inline=False)
        em.add_field(name="**:smirk: Miscelleneous Command Menu**", value="`Type mischelp to access Miscelleneous Command Menu`\n\n", inline=False)
        em.add_field(name="**:moneybag: Economy Command Menu**", value="`Type ecohelp to access Economy Command Menu`\n\n", inline=False)
        em.add_field(name="**:video_game: Fun Command Menu**", value="`Type funhelp to access the Fun Command Menu`\n\n", inline=False)
        em.add_field(name="**:camera: Image Command Menu**", value="`Type imagehelp to access the Image Command Menu`\n\n", inline=False)
        em.add_field(name="**<a:music:846058155335221269> Music Command Menu**", value="`Type musichelp to access the Music Command Menu`\n\n", inline=False)
        em.add_field(name="**:gear: Config Command Menu**", value="`Type confighelp to access the Config Command Menu`\n\n", inline=False)
        em.add_field(name="**<a:ThumbsUP:785824406546939915> Support Glados Links**", value="[Invite Me](https://discord.com/api/oauth2/authorize?client_id=791891067309785108&permissions=2147352567&scope=bot)•[Support Server](https://discord.gg/wkMuA6TjUD)•[Vote Me](https://top.gg/bot/791891067309785108/vote)\n\n", inline=False)
        em.set_thumbnail(url="https://am21.mediaite.com/tms/cnt/uploads/2015/07/Glados.jpg")
        await ctx.send(embed=em)

    #modhelp command
    @commands.command()
    async def modhelp(self, ctx):
        em = discord.Embed(title="<:b_ban:813998683842150431> Moderation Command Menu", description="`<requriment> : Meaning that requirement is optional`\n`(requirement) : Meaning that requirement is important`\n\n\n`clear (ammount) ` : Clears the specified ammount of messages\n\n`ban (user) <reason> ` : Bans the specified user from the server\n\n`kick (user) <reason> ` : Kicks the specified user from the server\n\n`mute (user) <time> <reason> ` : Mutes the specified user\n\n`unmute (user) ` : Unmutes the specified usern\n\n`unban (user)` : Unbans specified banned user from the server\n\n`announce (message) ` : Announces your message in a stylish embeded style!\n\n`gstart (duration) (prize)` : Creates a giveaway!\n\n`nuke (channel)` : Clear all the messages in the specified channel!\n\n`softban (user) <reason>`: Soft bans the specified user from the server and also clears all his/her messages\n\n`slowmode (time)`: Set the slowmode of a channel!\n\n`addrole (user) (role)`: Add the specified role to specified user!\n\n`removerole (user) (role)`: Remove the specified role from specified user\n\n`lock <channel>`: Lock the specified server's channel\n\n`unlock <channel>`: Unlock the specified server's channel\n\n`nick (user) (nickname)`: Change the nickname of the specified user\n\n`accept (id) (response)`: Accept a modmail using this command\n\n`cancel (id) (response)`: Reject a modmail using this command\n\n`add (name) (emoji_url)`: Add the specified emoji with specified name to the server using the given image url\n\n`rem (emoji_name)`: Removes the specified emoji from the server\n\n`steal (emoji_name)`: Steal a emoji with specified name from a server in which Glados is in and adds it in your server\n\n`emoji (querry)`: Add a emoji to the server according to specified querry\n\n", color=ctx.author.color, inline=False)
        await ctx.send(embed=em)

    #mischelp command
    @commands.command()
    async def mischelp(self, ctx):
        em = discord.Embed(title=":smirk: Miscelleneous Command Menu", description="`<requriment> : Meaning that requirement is optional`\n`(requirement) : Meaning that requirement is important`\n\n\n`ping` : Sends the bot's client's latency\n\n`serverinfo` : Send info about the server\n\n`userinfo (user)` : Sends info about specified user\n\n`suggest (suggestion)` : Suggest something to the server in a embeded style!\n\n`profile <user>` : Sends your profile if user not provided if provided it sends user's profile\n\n`define (querry)` : Sends a definition of querry from wikepedia\n\n`donate (donation)`: Send a donation request to the server!\n\n`modmail (problem)`: Send your a modmail to the server's staffs to ask for help\n\n`afk (message)`: Be afk in the server and when someone pings you, the bot send will them your afk message!\n\n", color=ctx.author.color, inline=False)
        await ctx.send(embed=em)

    #ecohelp command
    @commands.command()
    async def ecohelp(self, ctx):
        em = discord.Embed(title=":moneybag: Economy Command Menu", description="`<requriment> : Meaning that requirement is optional`\n`(requirement) : Meaning that requirement is important`\n\n\n`beg` : Beg people people for coins\n\n`slot (bet)` : Place a bet on casino machine if you win you will get double of your bet otherwise you will lose betted coins from your wallet\n\n`deposit (amount/all)` : Deposit your wallet money into your bank\n\n`withdraw (amount/all)` : Withdraw you bank money into your wallet\n\n`balance` : Check your balance\n\n`daily` : Get your daily coins!\n\n`search` : Search something and get coins or lose coins!\n\n`shop` : View the shop!\n\n`buy (item) (amount)` : Buy an item from the shop\n\n`inventory` : See your/someone's inventory\n\n", color=ctx.author.color)
        await ctx.send(embed=em)

    #funhelp command
    @commands.command()
    async def funhelp(self, ctx):
        em = discord.Embed(title=":video_game: Fun Command Menu", description="`<requriment> : Meaning that requirement is optional`\n`(requirement) : Meaning that requirement is important`\n\n\n`8ball (querry)` : Answers to the question asked a in a yes/no answer\n\n`marry (user)` : Sends a proposal for marriage to specified user\n\n`divorce` : Divorces without your current life partner\n\n`kill (user)` : Kills the specified user with a funny message\n\n`spc` : Play Stone Paper Scissor against a computer!\n\n`simprate` : Sends your simprate in a random percentage!\n\n`tictactoe (user)` : Play tic tac toe with specified user!\n\n`place (number)`: Place your X' or O's in your tictactoe match\n\n`minecraft (server)` : Search a minecraft server!\n\n`ascii (text)`: Convert your text into a stylish and interesting style!\n\n`aistart`: Start the AI settings in the message's channel!\n\n`aistop`: Stop the AI settings in message's channel\n\n`aichat (message)`: Chat with the AI using this command!\n\n`ailist`: Shows the channels in the server where AI is enabled!\n\n", color=ctx.author.color, inline=False)
        await ctx.send(embed=em)

    #imagehelp command
    @commands.command()
    async def imagehelp(self, ctx):
        em = discord.Embed(title=":camera: Image Command Menu", description="`<requriment> : Meaning that requirement is optional`\n`(requirement) : Meaning that requirement is important`\n\n\n`meme` : Sends a trending meme from reddit\n\n`avatar (user)` : Sends avatar about specified user\n\n`woof` : Sends a random dog image\n\n`meow` : Sends a random cat image\n\n`foxxy` : Sends a random fox image\n\n`chirp` :  Sends a random bird image\n\n`koalaboi` : See some random koala image\n\n`panda` : Sends a random panda image\n\n`redpanda` : Sends a random red panda image\n\n`pat (user)` : Pat's the specified user\n\n`wink (user)` : Winks to specified user\n\n`hug (user)` : Hugs specified user\n\n`wanted <user>` : Sends a wanted image of user\n\n`nyan <user>` :  Sends a nyan cat image of user\n\n", color=ctx.author.color)
        await ctx.send(embed=em)

    #confighelp command
    @commands.command()
    async def confighelp(self, ctx):
        em = discord.Embed(title=":gear: Config Command Menu", description="`<requriment> : Meaning that requirement is optional`\n`(requirement) : Meaning that requirement is important`\n\n\n`changeprefix (prefix)` : Changes bot's server prefix\n\n`set_reaction (role) (message_id) (emoji)` : Sets a reaction role to specified message\n\n`setdonation`: Change the settings of the donation system!\n\n`donationchannel (channel)`: Change the donation channel for the donation system!\n\n`mailchannel (channel)`: Set the modmail logs channel\n\n`filter (word)`: Blacklists that specified word from the server\n\n`fremove (word)`: Removes the specified word from the filter list\n\n`flist`: Shows words which are blacklisted in the server\n\n`ignore (channel)`: Allow a channel to use filtered words\n\n`rignore (channel)`: Remove a channel from the non-filtered list\n\n`lignore`: See the channels which are not being filtered\n\n", color=ctx.author.color)
        await ctx.send(embed=em)

    #musichelp command
    @commands.command()
    async def musichelp(self, ctx):
        em = discord.Embed(title="<a:music:846058155335221269> Music Command Menu", description="`<requriment> : Meaning that requirement is optional`\n`(requirement) : Meaning that requirement is important`\n\n\n`play (song)` : Plays the specified song in your voice channel\n\n`stop` : Stops the current song\n\n`pause` : Pauses the current song\n\n`resume` : Resumes the current paused song\n\n`join` : Glados joins your voice channel\n\n`leave` : Glados leaves you voice channel\n\n`queue <page>`: Shows the song queue of specified page\n\n`remove (number)` : Removes the specified song with that number from the queue\n\n`shuffle`: Shuffle the current songs in the queue in random order\n\n`current`: Shows the info of current song\n\n`summon`: Summon the bot in you voice channel!\n\n", color=ctx.author.color)
        await ctx.send(embed=em)

def setup(client):
    client.add_cog(Help(client))
