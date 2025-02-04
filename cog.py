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
        self.sel_alpha.start()

    def cog_unload(self):
        self.sel_alpha.cancel()

    @tasks.loop(time=midnight)
    async def sel_alpha(self):
        guild_id = 1159064214476959794 #doncord
        guild = self.bot.get_guild(guild_id)

        if guild:
            members = [member for member in guild.members if not member.bot]
            if members:
                self.group_leader = random.choice(members)
                #TODO: add file writing for group leader so it can be recalled in the leader command
                channel = guild.get_channel(1159064215735246921) #general
                if channel and self.group_leader:
                    await channel.send(f'rise and grind alphas.... todays group leader is {self.group_leader.mention}!!')
                    await channel.send(f'https://tenor.com/view/haechan-127hivemind-alpha-wolf-nct-nct-haechan-gif-26541424')

    @sel_alpha.before_loop
    async def before_sel_alpha(self):
        await self.bot.wait_until_ready()
    
    @commands.command()
    async def leader(self, ctx):
        if self.group_leader is None:
            await ctx.send('erm. there is no group leader today. wtf???')
        else:
            await ctx.send(f'your sigma group leader for today is {self.group_leader.name}')

async def setup(bot):
    await bot.add_cog(GroupLeader(bot))