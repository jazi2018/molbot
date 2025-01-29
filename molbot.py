#invite url https://discord.com/api/oauth2/authorize?client_id=1202724630847160411&permissions=412317207616&scope=bot

#discord API wrapper
import discord
from discord.ext import commands
#.env token import
import os
from dotenv import load_dotenv
#bot functionality
import random
import csv
import asyncio

load_dotenv()
BOT_TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

players = []
playerNumber = 0
impostorNumber = 0
gameRunning = 0
impostor = []

async def load_extensions():
    await bot.load_extension('cog')

@bot.event
async def setup_hook():
    await load_extensions()

@bot.event
async def on_ready():
    print("Bot is online.")

@bot.command()
async def members(ctx):
    guild = ctx.guild
    member_list = [member.name for member in guild.members if not member.bot]
    await ctx.send(f'Members in {guild.name}:\n{', '.join(member_list)}')

@bot.command()
async def quote(ctx, *args):

    if(len(args) > 0):
        if(len(args) == 1):
            await ctx.send("Incorrect number of arguments. Correct format:\
                            ```$quote [username] [quote (with no quotation marks)]```")
            return
        
        username = args[0]
        quote = " ".join(args[1:])

        with open("quotes.csv" , "a" , newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([username, quote])
            csvfile.close()

        await ctx.send(f'Registered that {username} said \"{quote}\"')
    else:
        with open("quotes.csv", 'r') as csvfile:
            csv_reader = csv.reader(csvfile)

            lines = []

            for line in csv_reader:
                lines.append(line)

            picked_line = (random.randint(1 , len(lines) - 1))
            await ctx.send(f'\"{lines[picked_line][1]}\" -{lines[picked_line][0]}')
            return
            
#include functionality to guess who said quote

@bot.command()
async def startgame(ctx, *args):
    global gameRunning
    global playerNumber
    global impostorNumber

    if(len(args) != 2):
        await ctx.send("Incorrect number of arguments. Correct format:\
                       \n```$startgame [number of players] [number of impostors]```")
        return

    playerNumber = int(args[0])
    impostorNumber = int(args[1])

    if(playerNumber <= 1):
        await ctx.send("Need at least 2 players to start a game.")
        return
    
    if(impostorNumber < 1):
        await ctx.send("There must be at least 1 impostor.")
        return

    if(gameRunning == 0):
        players.append(ctx.message.author.id)
        await ctx.send(f"{ctx.message.author.name} has joined. {playerNumber - len(players)} more players are required to begin. Type **$join** to join!")
        gameRunning = 1
    elif(gameRunning == 1):
        await ctx.send("Game is already running! Please join or wait for the game to end before trying to start a new one.")
        return

@bot.command()
async def join(ctx):
    global gameRunning
    global playerNumber
    global impostorNumber

    if(gameRunning == 0):
        await ctx.send("No game running! Please start a game to enable joining.")
        return
    
    if(ctx.message.author.id in players):
        await ctx.send("You are already in the game!")
        return
    
    responses = ["https://tenor.com/view/we-do-a-little-trolling-gif-21041353" , "https://tenor.com/view/imposter-detected-gif-21973555" , "https://tenor.com/view/sus-dog-sussy-baka-sussy-dog-ring-doorbell-gif-24026808" , \
                 "https://tenor.com/view/vince-mcmahon-entrance-wwe-walk-time-to-troll-gif-17431096" , "https://tenor.com/view/cat-troll-trolling-we-do-a-little-trolling-we-do-gif-21450570" , "https://tenor.com/view/silly-cat-cat-meme-face-cat-shocked-orange-cat-what-da-hell-gif-15285770798606642445 (you are the impostor)"]
    
    if(len(players) < playerNumber):
        players.append(ctx.message.author.id)
        await ctx.send(f"{ctx.message.author.name} has joined. {playerNumber - len(players)} more players are required to begin.")
        if(len(players) >= playerNumber):
            await ctx.send("Game starting! Check your DMs for a message from me!")
            count = 0
            while (count < impostorNumber):
                user = bot.get_user(random.choice(players))
                if (user not in impostor):
                    impostor.append(user)
                    await user.send(random.choice(responses))
                    count += 1
            await ctx.send("DM(s) Sent! Good luck!")

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
async def finishgame(ctx):
    global impostor
    global gameRunning

    if (ctx.message.author.id == players[0] and gameRunning == 1):
        if (impostorNumber == 1):
            await ctx.send("The impostor was...")
        elif (impostorNumber > 1):
            await ctx.send("The impostors were...")
        else:
            await ctx.send("There were no impostors!")
        for name in impostor:
            await ctx.send(f"||{name}!||")
        gameRunning = 0
        players.clear()
        impostor.clear()
    elif(gameRunning == 0):
        await ctx.send("There is no game currently running.")
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

async def main():
    await bot.start(BOT_TOKEN)

asyncio.run(main())

#add functionality to start game early (w less than 5)
#add functionality to make game cancelable after a set amount of time
#resolve discord.ext.commands.errors.CommandNotFound: Command "  " is not found (error message?)
#add chance for multiple people to be impostor, nobody, etc. (make this OPTIONAL!)
#voting system in discord?
#ELO!!!!

#could make a game, guess who said the quote

#consider defining classes so global variables are avoided
