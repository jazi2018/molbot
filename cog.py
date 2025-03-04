import discord
from discord.ext import commands, tasks
import datetime
import random

utc = datetime.timezone.utc

#midnight pst
midnight = datetime.time(hour=8, minute=0, tzinfo=utc)

class GroupLeader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.group_leader = None
        self.msg_id = None
        self.sel_alpha.start()

    def cog_unload(self):
        self.sel_alpha.cancel()

    async def fetch_message(self):
        '''fetches reaction message on bot startup to ensure
        it's not repeated & msg_id persists thru restarts'''
        welcome_id = 1159237538318389253 #welcome channel in doncord
        channel = self.bot.get_channel(welcome_id)
        if channel:
            pinned = await channel.pins()
            for msg in pinned:
                if msg.content == 'react with 🐺 to join the pack!! (a random pack member will be chosen daily to be the new group leader)':
                    self.msg_id = msg.id
                    print(f'located reaction message with id: {self.msg_id}')
                    return True
        print('no message found')
        return False

    @commands.Cog.listener()
    async def on_ready(self):
        '''attempts to fetch target message on reboot - 
        on fail prints a message to welcome channel'''
        print('on_ready running within cog')
        if not await self.fetch_message():
            welcome_id = 1159237538318389253 #welcome channel in doncord
            channel = self.bot.get_channel(welcome_id)
            if channel:
                message = await channel.send('react with 🐺 to join the pack!! (a random pack member will be chosen daily to be the new group leader)')
                self.msg_id = message.id #save id
                await message.add_reaction('🐺')
                await message.pin()
                print('msg sent and pinned')
            else:
                print('channel not found')

    ### GAME OPT-IN ###

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        '''adds role to users who react to specific message'''
        #check valid reaction at target message
        if reaction.message.id == self.msg_id and str(reaction.emoji) == '🐺':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='pack member')

            if role:
                member = guild.get_member(user.id) #get member id from reactor
                if member:
                    await member.add_roles(role) #adds role to user
                    print(f'assigned role to {user.name} ({user.id})')
                else:
                    print(f'could not find member {user.name} ({user.id})')
            else:
                print('no such role exists in current server')
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        '''removes role from people who un-react to a message'''
        if reaction.message.id == self.msg_id and str(reaction.emoji) == '🐺':
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, name='pack member')
            if role:
                member = guild.get_member(user.id) #get member id from reactor
                if member:
                    await member.remove_roles(role) #adds role to user
                    print(f'removed role from {user.name} ({user.id})')
                else:
                    print(f'could not find member {user.name} ({user.id})')
            else:
                print('no such role exists in current server')

    ### DAILY SELECTION ###

    @tasks.loop(time=midnight)
    async def sel_alpha(self):
        guild_id = 1159064214476959794 #doncord
        guild = self.bot.get_guild(guild_id)

        if guild:
            members = [member for member in guild.members if not member.bot] #and role (to subscribe to game) in member.roles
            role_name = 'pack member'
            role = discord.utils.get(guild.roles, name=role_name) #get pack member role
            members = [member for member in members if role in member.roles] #filter out non pack members
            if members:
                self.group_leader = random.choice(members)
                channel = guild.get_channel(1159064215735246921) #general
                #NOTE: make a fork for local testing
                if channel and self.group_leader:
                    try:
                        role_name = 'group leader'
                        role = discord.utils.get(guild.roles, name=role_name)

                        #clear out previous group leader
                        for member in members:
                            if role in member.roles:
                                await member.remove_roles(role)

                        await self.group_leader.add_roles(role)

                    except discord.DiscordException as e:
                        channel.send(f'error assigning role: {e}')

                    await channel.send(f'rise and grind alphas.... todays group leader is {self.group_leader.mention}!!')
                    await channel.send(f'https://tenor.com/view/haechan-127hivemind-alpha-wolf-nct-nct-haechan-gif-26541424')

    @sel_alpha.before_loop
    async def before_sel_alpha(self):
        await self.bot.wait_until_ready()
    
    @commands.command()
    async def leader(self, ctx):
        '''announces current group leader'''
        role = discord.utils.get(ctx.guild.roles, name='group leader')
        for member in ctx.guild.members:
            if role in member.roles:
                await ctx.send(f'your current group leader is {member.name}')
                return
        
        await ctx.send('this server does not currently have a group leader :-)')
    
    # @commands.command()
    # async def test(self, ctx):
    #     #set var to role
    #     try:
    #         role = discord.utils.get(ctx.guild.roles, name='group leader')
    #     except discord.DiscordException as e:
    #         print(f'role not found: {e}')
    #     if role:
    #         #remove roles from everyone
    #         members = [member for member in ctx.guild.members if not member.bot]
    #         if members:
    #             for member in members:
    #                 if role in member.roles:
    #                     try:
    #                         await member.remove_roles(role)
    #                     except discord.DiscordException as e:
    #                         print(f'failed to remove role: {e}')
    #             #choose random member and assign role
    #             sel = random.choice(members)
    #             try:
    #                 await sel.add_roles(role)
    #                 await ctx.send(f'{sel.name} has been given {role}')
    #             except discord.DiscordException as e:
    #                 print(f'failed to give role: {e}')
    #         else:
    #             print('member list failed')
    #     else:
    #         print('no role found')

async def setup(bot):
    await bot.add_cog(GroupLeader(bot))