import discord
import db_conn
import asyncio

client = discord.Client()

user_db = db_conn.DbConn('user.db')

@client.event
async def on_message(message):
    if (message.author == client.user):
        return

    print(f"{message}")

client.run('NzQ1MzUyNDMwODc0NTI1NzM2.Xzwhiw.D1wT8UeAirj8kNXuh-Rcl3_pyNU')
