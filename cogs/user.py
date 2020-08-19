from discord.ext import commands
import db_conn

user_db = db_conn.DbConn('user.db')

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(brief='User Queries', invoke_without_commmand=True)
    async def user(self, ctx):
        """Commands to get Activity List"""
        await ctx.send_help(ctx.command)

    async def on_member_join(user):
    	user_db.add_person(user.id)

    @user.command(brief='Add all members')
    @commands.has_any_role('Admin', 'Moderator')
    async def addall(self, ctx):
        """Adds all members to db"""
        for member in self.bot.get_all_members():
            if member.bot == False:
                user_db.add_person(member.id)
        await ctx.send("Done!")

def setup(bot):
    bot.add_cog(User(bot))
