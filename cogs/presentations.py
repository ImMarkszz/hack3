import discord, random
from discord.ext import commands


# presentations.py

class Present(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('presentations.py online')

    @commands.command()
    @commands.has_role('exec')
    async def present(self, ctx, *,role: discord.Role):
        voice_channel = ctx.guild.get_channel(697531358318166166)
        announcments = ctx.guild.get_channel(697528162954903572)
        #techhacks_role = ctx.guild.get_role('TechHacks')
        exec_role = ctx.guild.get_role('exec')
        exec_perms = discord.Permissions.voice()
        #await voice_channel.set_permissions(techhacks_role, overwrite=exec_perms)
        permissions = discord.PermissionOverwrite(speak=False, stream=False)
        pres_perms = discord.PermissionOverwrite(speak=True, stream=True)
        for all_roles in ctx.guild.roles:

            if not (all_roles == exec_role or all_roles == role): #or all_roles == techhacks_role):
                await voice_channel.set_permissions(all_roles, overwrite=permissions)
            else:
                await voice_channel.set_permissions(all_roles, overwrite=pres_perms)
        await announcments.send(f'everyone, team {role.mention} is now presenting! Show '
                                f'some respect and join the '
                                f'#presentations voice channel! ;)')
        await voice_channel.set_permissions(exec_role, overwrite=exec_perms)
        #await voice_channel.set_permissions(techhacks_role, overwrite=exec_perms)



    @commands.command()
    @commands.has_role('exec')
    async def hush(self, ctx):

        permissions = discord.PermissionOverwrite(speak=True, stream=True)
        techhacks_role = ctx.guild.get_role('TechHacks')
        exec_perms = discord.Permissions.voice()

        exec_role = ctx.guild.get_role('exec')
        voice_channel = ctx.guild.get_channel(697531358318166166)
        # await voice_channel.set_permissions(techhacks_role, overwrite=exec_perms)

        for all_roles in ctx.guild.roles:
            if not (all_roles == exec_role): # or all_roles == techhacks_role):
                await voice_channel.set_permissions(all_roles, overwrite=permissions)

        await voice_channel.set_permissions(exec_role, overwrite=exec_perms)
        await ctx.send('All presenters have been muted')



def setup(bot):
    bot.add_cog(Present(bot))
