import discord
from discord.ext import commands
import sys
import traceback
import os

#pylint: disable=import-error
from modules import bot_utils


DESCRIPTION = "Howdy."
TOKEN = os.environ['ANNA_BOT_TOKEN']

bot = commands.Bot(command_prefix="!", description=DESCRIPTION)

# this specifies what extensions to load when the bot starts up
startup_extensions = ["cogs.moderation"]

# <------ Events ------>
@bot.event
async def on_ready ():
    print('Started up successfully.')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message: discord.message.Message):
    # Trust me, this is the simplest approach to all these checks...
    if message.author is not bot.user:
        if message.guild is not None:
            if bot.user in message.mentions:
                
                rasa_responses = bot_utils.get_rasa_response(message.content, message.author)
                
                for response in rasa_responses:
                    actual_response = f"{message.author.mention} {response}"
                    await message.channel.send(actual_response)

        else:
            await message.channel.send("Sorry, I don't have DM functionality enabled at the moment.")

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """The event triggered when an error is raised while invoking a command.
    ctx   : Context
    error : Exception"""
    # This prevents any commands with local handlers being handled here in on_command_error.
    if hasattr(ctx.command, 'on_error'):
        return

    ignored = (commands.UserInputError, commands.BadArgument)

    # Allows us to check for original exceptions raised and sent to CommandInvokeError.
    # If nothing is found. We keep the exception passed to on_command_error.
    error = getattr(error, 'original', error)

    # Anything in ignored will return and prevent anything happening.
    if isinstance(error, ignored):
        return

    elif isinstance(error, commands.NoPrivateMessage):
        try:
            return await ctx.author.send(f'Sorry, {ctx.command} can not be used in Private Messages.')
        except:
            pass
    elif isinstance(error, commands.NotOwner):
        return await ctx.send("This command can only be run by Acey#4962. Please ping him if I'm causing trouble!", delete_after=10)
    elif isinstance(error, commands.MissingPermissions):
        return await ctx.send(error.message, delete_after=10)

    # All other Errors not returned come here... And we can just print the default TraceBack.
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

# <------ Commands ------>
@bot.command()
@commands.is_owner()
async def disconnect():
    """Disconnect"""
    print('Exit command received. Ending process.')
    await bot.logout()
    exit()

if __name__ == "__main__":
    bot.run(TOKEN)
