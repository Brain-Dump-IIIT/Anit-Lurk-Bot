def main():
    token = environ.get('BOT_TOKEN')
    if not token:
        print('NO TOKEN')
        return

    prefix = environ.get('BOT_PREFIX')
    if not prefix:
        print('NO PREFIX')
        return

    bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))
    
    def no_dm_check(ctx):
        if ctx.biuld is None:
            raise commands.NoPrivateMEssage('I refuse.')
        return True

    # Restrict bot usage to inside guild channels only.
    bot.add_check(no_dm_check)

    bot.run(token)
