# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Tic Tac Toe Bot by Jamezlz", command_prefix="!", pm_help = False)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Support Discord Server: https://discord.gg/FNNNgqb')
	print('Github Link: https://github.com/Habchy/BasicBot')
	print('--------')
	print('You are running BasicBot v2.1') #Do not change this. This will really help us support you, if you need support.
	print('Created by Habchy#1665')
	return await client.change_presence(game=discord.Game(name='Tic-Tac-Toe')) 
    
class InvalidInputError(Exception):
    pass
    
class TTTBoard():
    def __init__(self):
        self.squares = {}
        for i in range(1,10):
            self.squares[i] = i      
    def __str__(self):
        string = "{0}|{1}|{2}\n".format(self.squares[1],self.squares[2],self.squares[3])
        string = string + "{0}|{1}|{2}\n".format(self.squares[4],self.squares[5],self.squares[6])
        string = string + "{0}|{1}|{2}\n".format(self.squares[7],self.squares[8],self.squares[9])
        return string
    def addT(self, num, x):
        if self.squares[num] not in ["X","Y"]:
            self.squares[num] = x
        else:
            raise InvalidInputError      
    def winner(self):
        if self.squares[1] == self.squares[2] == self.squares[3]:
            return self.squares[1]
        elif self.squares[4] == self.squares[5] == self.squares[6]:
            return self.squares[4]
        elif self.squares[7] == self.squares[8] == self.squares[9]:
            return self.squares[7]
        elif self.squares[1] == self.squares[4] == self.squares[7]:
            return self.squares[1]
        elif self.squares[2] == self.squares[5] == self.squares[8]:
            return self.squares[2]
        elif self.squares[3] == self.squares[6] == self.squares[9]:
            return self.squares[3]
        elif self.squares[1] == self.squares[5] == self.squares[9]:
            return self.squares[1]
        elif self.squares[3] == self.squares[5] == self.squares[7]:
            return self.squares[3]
        else:
            return None


Player1 = None
Player2 = None
active = False
active_player = None
board = TTTBoard()

@client.command(pass_context=True)
async def TTT(ctx, arg1 = None):
    global active
    global Player1
    global Player2
    global board
    global active_player
    if active:
        if ctx.message.author == active_player:
            try:
                arg1 = int(arg1)
                if arg1 not in range(1,10):
                    raise InvalidInputError
                if active_player == Player1:
                    board.addT(arg1,"X")
                else:
                    board.addT(arg1,"Y")
                await client.send_message(ctx.message.channel, content = board.__str__())
                winner = board.winner()
                if winner is not None:
                    await client.send_message(ctx.message.channel, content = "Player {} wins".format(winner))
                    Player1 = None
                    Player2 = None
                    active = False
                    active_player = None
                    board = TTTBoard()
                else:
                    if active_player == Player1:
                        active_player = Player2
                        await client.send_message(ctx.message.channel, content = "Player 2 type in a number on the board to place an Y there")
                    else:
                        active_player = Player1
                        await client.send_message(ctx.message.channel, content = "Player 1 type in a number on the board to place an X there")
            except (InvalidInputError, NameError):
                await client.send_message(ctx.message.channel, content = "Invalid Input: Number must be 1-9 and not used")
        else:
            await client.send_message(ctx.message.channel, content = "It isn't your turn {}".format(ctx.message.author))
    else:
        if Player1 is None:
            Player1 = ctx.message.author
            await client.send_message(ctx.message.channel, content = 'Player 1: {}. Waiting for Player 2'.format(Player1))
        elif Player2 is None:
            Player2 = ctx.message.author
            string = 'All Players Ready. Let The Game Begin\n' + "Welcome to Tic-Tac-Toe.\n" + board.__str__() + "\nPlayer 1 type in a number on the board to place an X there\n"
            await client.send_message(ctx.message.channel, content = string)
            active = True
            active_player = Player1

client.run('token')