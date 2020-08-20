from discord.ext import commands
import db_conn

user_db = db_conn.DbConn('user.db')

# In order: INITIAL, ELON MUSK
offtopic = [742298510409334805, 745687511891968191]

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(brief='User Queries', invoke_without_commmand=True)
    async def user(self, ctx):
        """Commands to get Activity List"""
        await ctx.send_help(ctx.command)

    @commands.Cog.listener()
    async def on_member_join(self, user):
        """Add person to db on member join"""
        user_db.add_person(user.id)

    @commands.Cog.listener()
    async def on_member_remove(self, user):
        """Remove person from db on member leave"""
        user_db.remove_person(user.id)

    @user.command(brief='Add all members')
    @commands.has_any_role('Admin', 'Moderator')
    async def addall(self, ctx):
        """Adds all members to db"""
        for member in self.bot.get_all_members():
            if member.bot == False:
                user_db.add_person(member.id)
        await ctx.send("Done!")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Increment score on message""" 
        if message.author.bot:
            return
        if message.channel.category_id in offtopic:
            return

        user_db.message_count_increment(message.author.id, 1,
                len(message.content), 1)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Decrement score on message delete"""
        if message.author.bot:
            return
        if message.channel.category_id in offtopic:
            return

        user_db.message_count_increment(message.author.id, -1,
                -len(message.content), -1)

    @user.command(brief='Resets score of all members')
    @commands.has_any_role('Admin', 'Moderator')
    async def reset(self, ctx):
        """Reset score of all members"""
        user_db.reset()

def setup(bot):
    bot.add_cog(User(bot))
