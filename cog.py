from discord.ext import commands, tasks
import datetime
import random

utc = datetime.timezone.utc

#midnight pst
midnight = datetime.time(hour=8, minute=0, tzinfo=utc)

class GroupLeader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sel_alpha.start()

    def cog_unload(self):
        self.sel_alpha.cancel()

    @tasks.loop(time=midnight)
    async def sel_alpha(self):
        print("determining group leader.....")
        guild_id = 1159064214476959794
        guild = self.bot.get_guild(guild_id)

        if guild:
            members = [member for member in guild.members if not member.bot]
            if members:
                group_leader = random.choice(members)
                channel = guild.get_channel(1159064215735246921)
                if channel:
                    await channel.send(f'rise and grind alphas.... todays group leader is {group_leader.mention}!!')
                    await channel.send(f'https://tenor.com/view/haechan-127hivemind-alpha-wolf-nct-nct-haechan-gif-26541424')

    @sel_alpha.before_loop
    async def before_sel_alpha(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(GroupLeader(bot))