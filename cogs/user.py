from discord import commands
import db_conn
import asyncio
import main

user_db = DbConn('user.db')

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(brief='User Queries', invoke_without_commmand=True)
    async def user(self, ctx):
        """Commands to get Activity List"""
        await ctx.send_help(ctx.command)

    async def on_member_join(user):
    	user_db.add_person(user.id)

    async def add_all_members():
        for member in client.get_all_members():
            if member.bot == False:
                user_db.add_person(member.id)
