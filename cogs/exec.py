#exec.py
import discord,time,random
from discord.ext import commands
from discord import Member


class Exec(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('exec.py is active')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5, Channel=''):
        await self.bot.wait_until_ready()
        if Channel == '':
            Channel = ctx.channel
        else:
            Channel = self.bot.get_channel(Channel)

        await Channel.purge(limit=amount)
        await Channel.send(f'Cleared by {ctx.author.mention}')

    @commands.command()
    @commands.has_role('exec')
    async def kick(self, ctx, member: Member, *, reason=None):
        await self.bot.wait_until_ready()
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for: {reason}')

    @commands.command()
    @commands.has_role('exec')
    async def ban(self, ctx, member: Member, *, reason=None):
        await self.bot.wait_until_ready()
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for: {reason}')

    @commands.command()
    @commands.has_role('exec')
    async def unban(self, ctx, *, member):
        await self.bot.wait_until_ready()
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required argument')
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f'The execs are a far greater power than I, {ctx.message.author}, and I am afraid'
                           f' they will not allow me to do that')
            return
        elif isinstance(error, commands.CommandNotFound):
            await ctx.add_reaction("😳")
            await ctx.send('404 Command Not Found')
        elif isinstance(error, commands.MissingRole):
            await ctx.send('You already have a team silly!')
        else:
            await ctx.send(f'{error} error occured')


def setup(bot):
    bot.add_cog(Exec(bot))
