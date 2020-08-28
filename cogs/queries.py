from discord.ext import commands
import db_conn

user_db = db_conn.DbConn('user.db')

class Queries(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(brief='Database Queries', invoke_without_command=True)
    async def query(self, ctx):
        """Commands to query on database"""
        await ctx.send_help(ctx.command)

    @query.command(brief='Return message count list')
    @commands.has_any_role('Admin', 'Moderator')
    async def list(self, ctx):
        """Returns a list of users along with their message count"""
        res = user_db.get_user_list()
        for i in range(10):
            print(res[i])


def setup(bot):
    bot.add_cog(Queries(bot))
