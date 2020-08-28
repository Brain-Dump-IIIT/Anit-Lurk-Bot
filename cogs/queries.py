from discord.ext import commands
from utils import paginator
from utils import db_conn
from utils import table
import discord

user_db = db_conn.DbConn('user.db')

_USERS_PER_PAGE = 15
_NAME_MAX_LEN = 20
_PAGE_WAIT_TIME = 5 * 60 # 5 minutes

def make_pages(users, title):
    chunks = paginator.chunkify(users, _USERS_PER_PAGE)
    pages = []
    done = 0

    style = table.Style('{:>}  {:<}  {:<}')
    for chunk in chunks:
        t = table.Table(style)
        t += table.Header('#', 'Name', 'Score Count')
        t += table.Line()
        for i, (user, score) in enumerate(chunk):
            name = user.display_name
            if len(name) > _NAME_MAX_LEN:
                name = name[:_NAME_MAX_LEN - 1] + '…'
        
            t += table.Data(i + done, name, score)
        table_str = '```\n' + str(t) + '\n```'
        embed = discord.Embed(description=table_str)
        pages.append((title, embed))
        done += len(chunk)
    return pages

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
        res.sort(key=lambda tup: tup[1], reverse=True)

        users = [(ctx.guild.get_member(int(user_id)), score_count)
                for user_id, score_count in res if user_id]

        users = [(user, score) for user, score in users if user is not None]

        title = 'List of users'
        pages = make_pages(users, title)
        paginator.paginate(self.bot, ctx.channel, pages, 
                wait_time=_PAGE_WAIT_TIME, set_pagenum_footers=True)

def setup(bot):
    bot.add_cog(Queries(bot))
