import discord
import db_conn
import asyncio
import main

@client.event
async def on_member_join(user):
	user_db.add_person(user.id)
