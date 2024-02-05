#invite url https://discord.com/api/oauth2/authorize?client_id=1202724630847160411&permissions=412317207616&scope=bot

import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

players = []
gameRunning = 0
impostor = "null"

@bot.event
async def on_ready():
    print("Bot is online.")

#@bot.command()
#async def helpTest(ctx):
    #await ctx.send("https://cdn.discordapp.com/attachments/1202726587238191177/1202773408279035914/851pg9.png?ex=65cead06&is=65bc3806&hm=192fba503473055a1d6464dc679ee172b6a1bdb2cec67287a4fa7258aa04cb59& \
             #\n You asked for help. This is a test. \
             #\n https://cdn.discordapp.com/attachments/1202726587238191177/1202807666892865536/oqcptj21hq151.png?ex=65ceccee&is=65bc57ee&hm=ad95faafab9234672d448919c3f7b066defbf3487436c65248cdd3bb29f5f6bc&")

@bot.command()
async def startkey(ctx):
    global gameRunning
    if(gameRunning == 0):
        players.append(ctx.message.author.id)
        await ctx.send(f"{ctx.message.author.name} has joined. {5 - len(players)} more players are required to begin. Type **$join** to join!")
        gameRunning = 1
    elif(gameRunning == 1):
        await ctx.send("Game is already running! Please join or wait for the game to end before trying to start a new one.")
        return

@bot.command()
async def join(ctx):
    global gameRunning
    global impostor
    if(gameRunning == 0):
        await ctx.send("No game running! Please start a game to enable joining.")
        return
    if(ctx.message.author.id in players):
        await ctx.send("You are already in the game!")
        return
    if(len(players) < 5):
        players.append(ctx.message.author.id)
        await ctx.send(f"{ctx.message.author.name} has joined. {5 - len(players)} more players are required to begin.")
        if(len(players) == 5):
            await ctx.send("Game starting! Check your DMs for a message from me!")
            user = bot.get_user(random.choice(players))
            impostor = user
            await user.send("You are the impostor :sunglasses:")
            await ctx.send("DM Sent! Good luck!")

    else:
        await ctx.send("Game is full!")

@bot.command()
async def cancel(ctx):
    global gameRunning
    if(ctx.message.author.id == players[0]):
        await ctx.send("Game cancelling...")
        gameRunning = 0
        players.clear()
        await ctx.send("Game cancelled.")
    else:
        await ctx.send("Cannot cancel a game you did not initialize!")
        return
    
@bot.command()
async def finishkey(ctx):
    global impostor
    global gameRunning
    if (ctx.message.author.id == players[0]):
        await ctx.send("The impostor was...")
        await ctx.send(f"**{impostor}**!")
        gameRunning = 0
        players.clear()
        impostor = "null"
    else:
        await ctx.send("Cannot end a game you did not initialize!")
        return

@bot.command()
async def creature(ctx):
    creatureList = ["https://shorturl.at/rIS16" , "https://shorturl.at/klntU" , "https://shorturl.at/rwK37" , "https://shorturl.at/gvJS4" , \
                    "https://shorturl.at/fiqT6" , "http://tinyurl.com/mrxzcrwm" , "http://tinyurl.com/43m3yprf" , "http://tinyurl.com/5ut6xcnh" , \
                    "http://tinyurl.com/2smp56t3" , "http://tinyurl.com/375fzan7" , "http://tinyurl.com/ycxf8vua" , "http://tinyurl.com/4f6txjyy"]
    await ctx.send(random.choice(creatureList))

@bot.command()
async def birthday(ctx):
    await ctx.send("holy flip happy flipping birthday!")
    await ctx.send("https://media1.tenor.com/m/Y89slvaDQ1sAAAAC/suguru-geto-geto.gif")

bot.run(BOT_TOKEN)

#add functionality to start game early (w less than 5)
#allow for input of number of players and impostors
#add functionality to make game time out after a set amount of time
#resolve discord.ext.commands.errors.CommandNotFound: Command "  " is not found (error message?)
#add various messages that the bot can send to the impostor
#add chance for multiple people to be impostor, nobody, etc. (make this OPTIONAL!)
#voting system in discord?
