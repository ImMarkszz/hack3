import discord
from discord.ext import commands
from discord import Member


class Exec(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Exec Cog is online')

    @commands.command()
    @commands.has_role('exec')
    async def clear(self, ctx, amount=5):
        if amount == 'all':
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=amount)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))

    @commands.command()
    @commands.has_role('exec')
    async def kick(self, ctx, member: Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.mention} for: {reason}')

    @commands.command()
    @commands.has_role('exec')
    async def ban(self, ctx, member: Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.mention} for: {reason}')

    @commands.command()
    @commands.has_role('exec')
    async def unban(self, ctx, *, member):
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
            await ctx.send('404 Command Not Found')
        else:
            await ctx.send(f'{error} error occured')


def setup(bot):
    bot.add_cog(Exec(bot))