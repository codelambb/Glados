import dbl
from discord.ext import commands


class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc5MTg5MTA2NzMwOTc4NTEwOCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjExMjg0NYxfQ.aFfmHggviD60KVxn6eOv_6pLxbj8Yq84SCiGTvri--g' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(TopGG(bot))