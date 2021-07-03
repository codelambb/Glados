import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown
import json
import random
from random import choice
from random import randint
import asyncio

#shop items
mainshop = [{"name":"Laptop","price":5000,"description":"Hack stuff and earn money, if caught you have to pay money to police"}]

#open_account function
async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["passive"] = "off"

    with open("mainbank.json","w") as f:
        json.dump(users,f,indent=4)
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
        json.dump(users,f, indent=4)

    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal

#buy_this function
async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            obj = {"item":item_name, "amount":amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name, "amount":amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json","w") as f:
        json.dump(users,f,indent=4)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

#sell_this function
async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = item["price"] 
            break

    if name_ == None:
        return [False,1]

    cost = price*amount
    users = get_bank_data()
    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False,3]
    except:
        return [False,3]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "wallet")

    return [True,"Worked"]

class Economy(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('economy file is ready')

    #balance command
    @commands.command(aliases=["bal"])
    async def balance(self, ctx,*, member : discord.Member = None):
        if member == None:
            await open_account(ctx.author)
            user = ctx.author
            users = await get_bank_data()

            x = random.randint(1,9)

            if(x == 5 or x == 9 ):
                await ctx.send(f'Tip to support me:\nJoin my support server its cool there! https://discord.gg/wkMuA6TjUD')

            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]

            em = discord.Embed(title=f"{ctx.author.name}'s bank account", color=ctx.author.color)
            em.add_field(name="Wallet Balance", value=f"{wallet_amt} :coin:")
            em.add_field(name="Bank Balance", value=f"{bank_amt} :coin:")
            await ctx.send(embed=em)
            return

        await open_account(member)
        user = member
        users = await get_bank_data()

        x = random.randint(1,9)

        if(x == 5 or x == 9 ):
            await ctx.send(f'Tip to support me:\nJoin my support server its cool there! https://discord.gg/wkMuA6TjUD')

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        em = discord.Embed(title=f"{member.name}'s bank account", color=ctx.author.color)
        em.add_field(name="Wallet Balance", value=f"{wallet_amt} :coin:")
        em.add_field(name="Bank Balance", value=f"{bank_amt} :coin:")
        await ctx.send(embed=em)

    #slot command
    @commands.command()
    @cooldown(1, 20, BucketType.user)
    async def slot(self, ctx, amount=None):
        await open_account(ctx.author)

        if amount == None:
            await ctx.send(f'Please enter the amount you want to bet')
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive!")
            return

        x = random.randint(0,1)
        i = random.randint(0,1)
        e = random.randint(0,1)

        u = "sda"
        l = "dasd"
        p = "dasd"

        if x == 0:
            u = ":regional_indicator_x:"

        elif x == 1:
            u = ":regional_indicator_o:"

        if i == 0:
            l = ":regional_indicator_x:"

        elif i == 1:
            l = ":regional_indicator_o:"

        if e == 0:
            p = ":regional_indicator_x:"

        elif e == 1:
            p = ":regional_indicator_o:"

        await ctx.send(f"|{u}  {l}  {p}|")

        if u == l and u == p:
            await update_bank(ctx.author,2*amount)
            await ctx.send(f'You won and won {amount*2} :coin:!')
        else:
            await update_bank(ctx.author,-1*amount)
            await ctx.send(f'You lost and lost {amount} :coin:..')

    #daily command
    @commands.command()
    @cooldown(1, 86400, BucketType.user)
    async def daily(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings = 2000

        x = random.randint(1,9)

        await ctx.send(f"Given 2000 :coin: daily coins!")

        if x == 5 or x == 9 or x == 1 or x == 4:
            await ctx.send(f'Tip to support me:\nJoin my support server its cool there! https://discord.gg/wkMuA6TjUD')

        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json","w") as f:
            json.dump(users,f)

    #search command
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def search(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        searche = ["air","car","uber","bus","discord"]
        x = random.choice(searche)
        searche.remove(x)
        e = random.choice(searche)
        searche.remove(e)
        u = random.choice(searche)

        await ctx.send(f"What do you want to search? Type the name of it from the following options below\n\n``{x}`` ``{e}`` ``{u}``")

        try:
            msg = await self.client.wait_for(
                "message",
                timeout = 60,
                check = lambda message: message.author == ctx.author
                               and message.channel == ctx.channel
                )

            if msg:
                z = msg.content

                if z.lower() == x and x == "air":
                    p = random.randint(1000,1300)
                    await ctx.send(f"You searched ``air`` and found {p} :coin:. What the heck?")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                elif z.lower() == x and x == "car":
                    p = random.randint(100,200)
                    if int(users[str(user.id)]["wallet"]) > 200:
                        await ctx.send(f"You searched ``car`` and got caught by the police and paid {p} :coin: to get out of jail! Nice job robbing someone's car..")

                        users[str(user.id)]["wallet"] -= p

                        with open("mainbank.json","w") as f:
                            json.dump(users,f)

                        return

                    if int(users[str(user.id)]["wallet"]) <= 200:
                        await ctx.send(f"You searched ``car`` and earned {p} :coin:! I suggest not doing it again..")

                        users[str(user.id)]["wallet"] += p

                        with open("mainbank.json","w") as f:
                            json.dump(users,f)

                        return

                elif z.lower() == x and x == "uber":
                    p = random.randint(400,500)
                    await ctx.send(f"You searched an ``uber`` and robbed {p} :coin: from the uber driver..")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                elif z.lower() == x and x == "bus":
                    p = random.randint(100,200)
                    await ctx.send(f"You robbed a ``bus`` with children in it and got {p} :coin:. Do you feel proud to scare them?")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                elif z.lower() == x and x == "discord":
                    p = random.randint(50,250)
                    await ctx.send(f"You searched the whole ``discord`` and found {p} :coin:")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                if z.lower() == e and e == "air":
                    p = random.randint(1000,1300)
                    await ctx.send(f"You searched ``air`` and found {p} :coin:. What the heck?")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                elif z.lower() == e and e == "car":
                    p = random.randint(100,200)
                    if int(users[str(user.id)]["wallet"]) > 200:
                        await ctx.send(f"You searched ``car`` and got caught by the police and paid {p} :coin: to get out of jail! Nice job robbing someone's car..")

                        users[str(user.id)]["wallet"] -= p

                        with open("mainbank.json","w") as f:
                            json.dump(users,f)

                        return

                    if int(users[str(user.id)]["wallet"]) <= 200:
                        await ctx.send(f"You searched ``car`` and earned {p} :coin:! I suggest not doing it again..")

                        users[str(user.id)]["wallet"] += p

                        with open("mainbank.json","w") as f:
                            json.dump(users,f)

                        return

                elif z.lower() == e and e == "uber":
                    p = random.randint(400,500)
                    await ctx.send(f"You searched an ``uber`` and robbed {p} :coin: from the uber driver..")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                elif z.lower() == e and e == "bus":
                    p = random.randint(100,200)
                    await ctx.send(f"You robbed a ``bus`` with children in it and got {p} :coin:. Do you feel proud to scare them?")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                elif z.lower() == e and e == "discord":
                    p = random.randint(50,250)
                    await ctx.send(f"You searched the whole ``discord`` and found {p} :coin:")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                if z.lower() == u and u == "air":
                    p = random.randint(1000,1300)
                    await ctx.send(f"You searched ``air`` and found {p} :coin:. What the heck?")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                elif z.lower() == u and u == "car":
                    p = random.randint(100,200)
                    if int(users[str(user.id)]["wallet"]) > 200:
                        await ctx.send(f"You searched ``car`` and got caught by the police and paid {p} :coin: to get out of jail! Nice job robbing someone's car..")

                        users[str(user.id)]["wallet"] -= p

                        with open("mainbank.json","w") as f:
                            json.dump(users,f)

                        return

                    if int(users[str(user.id)]["wallet"]) <= 200:
                        await ctx.send(f"You searched ``car`` and earned {p} :coin:! I suggest not doing it again..")

                        users[str(user.id)]["wallet"] += p

                        with open("mainbank.json","w") as f:
                            json.dump(users,f)

                        return

                elif z.lower() == u and u == "uber":
                    p = random.randint(400,500)
                    await ctx.send(f"You searched an ``uber`` and robbed {p} :coin: from the uber driver..")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                elif z.lower() == u and u == "bus":
                    p = random.randint(100,200)
                    await ctx.send(f"You robbed a ``bus`` with children in it and got {p} :coin:. Do you feel proud to scare them?")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                elif z.lower() == u and u == "discord":
                    p = random.randint(50,250)
                    await ctx.send(f"You searched the whole ``discord`` and found {p} :coin:")

                    users[str(user.id)]["wallet"] += p

                    with open("mainbank.json","w") as f:
                        json.dump(users,f)

                    return

                else:
                    await ctx.send(f"What are you thinking man? That's not a valid response!")
                    return

        except asyncio.TimeoutError:
            await ctx.send(f'You were late to response')

    #sell command
    @commands.command()
    async def sell(self, ctx, item, amount=1):
        await open_account(ctx.author)
        res = await sell_this(ctx.author, item, amount, 0)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("That item isn't there!")
                return

            if res[1] == 2:
                await ctx.send(f"You don't own that have {amount} {item} in your bag.")
                return

            if res[1] == 3:
                await ctx.send(f"You don't have {item} in your bag.")
                return

        await ctx.send(f"You just sold **{amount} {item}**.")

    #beg command
    @commands.command()
    @cooldown(1, 20, BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        earnings = random.randrange(101)

        await ctx.send(f"Somone gave you {earnings} :coin:!")

        x = random.randint(1,9)

        if(x == 5 or x == 9 or x == 1 or x == 4):
            await ctx.send(f'Tip to support me:\nJoin my support server its cool there! https://discord.gg/wkMuA6TjUD')

        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json","w") as f:
            json.dump(users,f,indent=4)

    #withdraw command
    @commands.command(aliases=["with"])
    async def withdraw(self, ctx, amount = None):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        if amount == None:
            await ctx.send(f'Please enter the amount you want to withdraw')
            return

        bal = await update_bank(ctx.author)

        if amount == "all":
            bank_amt = users[str(user.id)]["bank"]

            if int(bank_amt) == 0:
                await ctx.send(f"You have 0 :coin: in your bank!")
                return

            await update_bank(ctx.author,int(bank_amt) )
            await update_bank(ctx.author,-1*bank_amt,"bank")

            await ctx.send(f"You withdrew {bank_amt} :coin:!")

        else:
            amount = int(amount)

            if amount == 0:
                await ctx.send(f"You can't withdraw 0 :coin:")
                return

            if amount > bal[1]:
                await ctx.send("You don't have that much money!")
                return

            if amount < 0:
                await ctx.send("Amount must be positive!")
                return

            await update_bank(ctx.author,amount)
            await update_bank(ctx.author,-1*amount,"bank")

            await ctx.send(f"You withdrew {amount} :coin:!")

    #deposit command
    @commands.command(aliases=["dep"])
    async def deposit(self, ctx, amount = None):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        if amount == None:
            await ctx.send(f'Please enter the amount you want to deposit')
            return

        bal = await update_bank(ctx.author)

        if amount == "all":
            wallet_amt = users[str(user.id)]["wallet"]

            if int(wallet_amt) == 0:
                await ctx.send(f"You have 0 :coin: in your wallet!")
                return

            await update_bank(ctx.author,-1*int(wallet_amt) )
            await update_bank(ctx.author,wallet_amt,"bank")

            await ctx.send(f"You deposited {wallet_amt} :coin:!")

        else:
            amount = int(amount)

            if amount == 0:
                await ctx.send(f"You can't deposit 0 :coin:")
                return

            if amount > bal[0]:
                await ctx.send("You don't have that much money!")
                return

            if amount < 0:
                await ctx.send("Amount must be positive!")
                return

            await update_bank(ctx.author,-1*amount)
            await update_bank(ctx.author,amount,"bank")

            await ctx.send(f"You deposited {amount} :coin:!")

    #gift command
    @commands.command()
    async def gift(self, ctx, member : discord.Member = None, amount = None):
        await open_account(ctx.author)
        await open_account(member)

        if amount == None:
            await ctx.send(f'Please enter the amount you want to gift to someone')
            return

        if member == None:
            await ctx.send(f'To whome you want to to gift it to? You didnt even mention!')

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("You don't have that much money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive!")
            return

        await update_bank(ctx.author,-1*amount)
        await update_bank(member,amount)

        x = random.randint(1,9)

        if(x == 5 or x == 9 or x == 1 or x == 4):
            await ctx.send(f'Tip to support me:\nJoin my support server its cool there! https://discord.gg/wkMuA6TjUD')

        await ctx.send(f"You successfully gave {member} {amount} :coin:!")

    #passive mode command
    @commands.command()
    @cooldown(1, 3600, BucketType.user)
    async def passive_mode(self, ctx, mode):
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        if str(users[str(user.id)]["passive"])  == mode and mode == "on":
            await ctx.send(f"Passive mode is already on for you!")
            return

        if str(users[str(user.id)]["passive"])  == mode and mode == "off":
            await ctx.send(f"Passive mode is already on for you!")
            return

        users[str(user.id)]["passive"] = mode
        await ctx.send(f"Successfully done!")

        with open("mainbank.json","w") as f:
            json.dump(users,f,indent=4)

    #shop command
    @commands.command()
    async def shop(self, ctx):
        em = discord.Embed(title="Glados Shop", color=ctx.author.color)

        for item in mainshop:
            name = item["name"]
            price = item["price"]
            descp = item["description"]
            em.add_field(name=name, value=f"{price} :coin: | {descp}", inline=False)

        await ctx.send(embed=em )

    #buy command
    @commands.command()
    async def buy(self, ctx, item, amount=1):
        await open_account(ctx.author)

        res = await buy_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send(f"That item isn't there in the shop!?")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have enough money in your wallet to buy that")
                return

        await ctx.send(f"You just bought {amount} {item}")

    #inventory command
    @commands.command(aliases=["inv"])
    async def inventory(self, ctx,*, member : discord.Member = None):
        if member == None:
            await open_account(ctx.author)
            user = ctx.author
            users = await get_bank_data()

            try:
                bag = users[str(user.id)]["bag"]
            except:
                bag = []

            em = discord.Embed(title=f"{ctx.author.name}'s Inventory", color=ctx.author.color)
            for item in bag:
                name = item["item"]
                amount = item["amount"]

                em.add_field(name=name, value=amount)

            await ctx.send(embed=em)
            return

        await open_account(member)
        user = member
        users = await get_bank_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = discord.Embed(title=f"{member}'s Inventory", color=ctx.author.color)
        for item in bag:
            name = item["item"]
            amount = item["amount"]

            em.add_field(name=name, value=amount)

        await ctx.send(embed=em)

    #rob command
    @commands.command()
    @cooldown(1,30,BucketType.user)
    async def rob(self, ctx,*, member : discord.Member = None):
        await open_account(member)
        await open_account(ctx.author)

        users = await get_bank_data()

        user = ctx.author

        if member == ctx.author:
            await ctx.send(f"You cannot rob yourself!")
            return

        if member == None:
            await ctx.send(f"Who do you want to rob?! Please mention someone next time")
            return

        if str(users[str(member.id)]["passive"])  == "on":
            await ctx.send(f"That user is in passive mode! Leave that peace loving man alone")
            return

        if int(str(users[str(member.id)]["wallet"])) <= 250:
            await ctx.send(f"That user dosent even have 250 :coin: in his wallet, Not worth it man.")
            return

        if int(str(users[str(user.id)]["wallet"])) <= 250:
            await ctx.send(f"You need to have 250 more coins")
            return

        a = random.randint(200,300)
        users[str(user.id)]["wallet"] += a
        users[str(member.id)]["wallet"] -= a

        with open("mainbank.json","w") as f:
            json.dump(users,f,indent=4)

        await ctx.send(f"You robbed {a} :coin: from that user's wallet")

    #all the error

    #beg error
    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"You need to wait ``{error.retry_after:,.2f}`` seconds to use that command again.")

    #daily error
    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"You need to wait ``{error.retry_after:,.2f}`` seconds to use that command again.")

    #search error
    @search.error
    async def search_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"You need to wait ``{error.retry_after:,.2f}`` seconds to use that command again.")

    #slot error
    @slot.error
    async def slot_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"You need to wait ``{error.retry_after:,.2f}`` seconds to use that command again.")

    #passive_mode error
    @passive_mode.error
    async def passive_mode_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"You need to wait ``{error.retry_after:,.2f}`` seconds to use that command again.")

    #rob command error
    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(f"You need to wait ``{error.retry_after:,.2f}`` seconds to use that command again.")

def setup(client):
    client.add_cog(Economy(client))
