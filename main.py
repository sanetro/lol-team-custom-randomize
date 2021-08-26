import discord
import os
import random

from discord.ext import commands, tasks
from discord.ext.commands import check

intents = discord.Intents.default()
intents.members = True


lol_squad = [] # Leageu of legends teams container
voice_channel_list = []
voiceChannel_1, voiceChannel_2 = None, None
team1, team2 = 0, 0


bot = commands.Bot(intents=intents, command_prefix='$') # Client object app name - bot, command always start with '$' before




# -------- TEAMS BOARD -------- #
def justify_lead_board(lol_squad):
  border = "-"*34
  tabs = "\t"*3
  tmp2 = f">>> {border}{border}\n  {tabs}Team 1{tabs}{tabs}{tabs}Team 2{tabs}\t\n {border}{border}\n"
  result = tmp2
  for i in range(len(lol_squad)//2):
    result += tabs + lol_squad[i] + tabs*3 + lol_squad[i+5] + "\n"    
  return result

# -------- SCORES BOARD -------- #
def justify_score_board(team1,team2):
  tmp = f'```diff\n\n+\t\tTeam 1\t\tTeam 2\n-\t\t  {team1}\t\t:\t  {team2}\n\n```'
  tmp = f'''
  >>>                Score
  -------------------------
    Team 1      :   **{team1}**
    Team 2      :   **{team2}**
  -------------------------
  '''
  return tmp

# -------- USERS LIST -------- #
def returnListOfSqad_lol(lol_squad):
  tmp = ">>> Here is your users list:\n"
  for i in range(len(lol_squad)):
    tmp +=  f"{i}\t" + str(lol_squad[i].name) + "\n"
  return tmp 



# -------- SET PLAYERS -------- #
@bot.command()
async def players(ctx, *members : discord.Member):
  # Description
  # Input users after 'at' (@) symbol. For example: $players @sanetro @someone @etc ... 
  global lol_squad 
  for user in members:
    lol_squad.append(user)  

# -------- MOVE ALL USERS -------- #
@bot.command()
async def start(ctx):
  # Description
  # Most important. This sends to particular channels ('Team_1'; 'Team_2')
  # It sends a embed (something like message, but with better border)
  global lol_squad
  vc1 = voice_channel_list[voiceChannel_1]
  vc2 = voice_channel_list[voiceChannel_2]
  for i in range(len(lol_squad)):
    try:
      if(i % 2 == 0):
        await lol_squad[i].move_to(vc1)
        mbed = discord.Embed(title='{} moved to {}.'.format(lol_squad[i].name, vc1),
                          description="by {}".format(ctx.message.author.name),
                          colour = discord.Colour.orange())
      else:
        await lol_squad[i].move_to(vc2)
        mbed = discord.Embed(title='{} moved to {}.'.format(lol_squad[i].name, vc2),
                          description="by {}".format(ctx.message.author.name),
                          colour = discord.Colour.purple())
      
    except:
      mbed = discord.Embed(title='Player problem', 
                          description="{} isn't in voice channels.".format(user.name),
                          colour = discord.Colour.red())      
    await ctx.send(embed=mbed)

  

# -------- TEAM COMMANDS -------- #
@bot.command()
async def team(ctx, *args): #When user add more args then 2
    global lol_squad, team1, team2 # containers
    
    server_curr_name = ctx.message.guild.name # name of server 
    # if not serverCheckInDatabase(server_curr_name):
    # AddCurrServerToDatabase(server_curr_name)
   
    # server_content = getDatabaseByServerName(server_curr_name) 
   

    args = list(args) # change zipped args from touple to array / list 
    args[0] = args[0].lower() # nessecery but protect you againts CAPSLOCK
    helpArgs = '''
    *List of command:*
     - **$team showlist** - show list of added users
     - **$team clear** - Clear all list of players
     - **$team add** *<user> <user> ... - add user to the list
     - **$team remove** *<user> <user> ... - remove user from the list
     - **$team rand** - Randomize all teams (team 1, team 2)
     - **$team score** - Show score of team 1 and 2
     - **$team addpoint 1** - add one point to team 1
     - **$team addpoint 2** - add one point to team 2
     - **$team reset** - Clear scores of team 1 and 2
    '''
    try:
      # -------- TEAM COMMANDS - help -------- #
      if args[0] in ["help", "-h", "h"]: # If i need help just type this 
        await ctx.send(helpArgs)

      # -------- TEAM COMMANDS - showlist -------- #
      if args[0] == "showlist": # show list of added users 
        await ctx.send(returnListOfSqad_lol(lol_squad))

      # -------- TEAM COMMANDS - clear -------- #
      if args[0] == "clear": # If i need to clean up list 
        lol_squad = []
        await ctx.send("List is empty.")

      # -------- TEAM COMMANDS - rand -------- #
      if args[0] == "rand": # here is a output of randomized users in each team
        if len(lol_squad) == 10:
          random.shuffle(lol_squad)
          await ctx.send(justify_lead_board(lol_squad))
        else:
          await ctx.send(f"Not enought number of users, wanted: {10 - len(lol_squad)}") # if you have less then 10 users

      # -------- TEAM COMMANDS - score -------- #
      if args[0] == "score":
        await ctx.send(justify_score_board(team1,team2))

      # -------- TEAM COMMANDS - addpoint - 1 -------- #
      if args[0] == "addpoint" and args[1] == "1":
        if team1 < 10:
          team1 += 1
        await ctx.send(justify_score_board(team1,team2)) 

      # -------- TEAM COMMANDS - addpoint - 2 -------- #
      if args[0] == "addpoint" and args[1] == "2":
        if team2 < 11:
          team2 += 1
        await ctx.send(justify_score_board(team1,team2))
      
      # -------- TEAM COMMANDS - reset -------- #
      if args[0] == "reset":
        team2, team1 = 0, 0
        await ctx.send(justify_score_board(team1,team2))

    # -------- TEAM COMMANDS - error -------- #
    except IndexError:
      await ctx.send("Wrong command: type **$team help**") # bad entry
pass

@bot.command()
async def server(ctx):   
  await ctx.message.author.send(voice_channel_list[voiceChannel_1])
   



@bot.command()
@commands.has_permissions(move_members=True)
async def move(ctx, *, channel : discord.VoiceChannel):
    author_ch = ctx.author.voice.channel.mention
    for members in ctx.author.voice.channel.members:
        await members.move_to(channel)
    await ctx.send(f'Moved everyone in {author_ch} to {channel.mention}!')


# -------- QUICK INFORMATION - when mention bot -------- #
@bot.event
async def on_message(message):
  welcomeText = f'''>>>    Hello everyone,
    I am a **{bot.user.name}**
    Installation:
    1. You should give admin permisions to this bot
    2. $setup - it creates 3 channels important for this bot
    3. $help - commands list
    '''
  mention = f'<@!{bot.user.id}>'    
  if mention in message.content:
    await message.channel.send(welcomeText)
  else:
    await bot.process_commands(message)

# -------- FIND CHANNELS -------- #
def fetchVoiceChannels():
  global voiceChannel_1, voiceChannel_2
  global voice_channel_list
  for guild in bot.guilds:
      for channel in guild.voice_channels:
          voice_channel_list.append(channel)

  print("Voice channels list:")
  [print(i, info) for i, info in enumerate(voice_channel_list)]  
 
  for index, vc in enumerate(voice_channel_list):
    if vc.name == "Team_1":
      voiceChannel_1 = index; print("Team_1 found")      
    if vc.name == "Team_2":
      voiceChannel_2 = index; print("Team_2 found")
  



# -------- CREATE CHANNELS -------- #
@bot.command()
async def setup(ctx):
  guild = ctx.guild  
  mbed = discord.Embed(title='Bad permission', description='Can not create a channels.')
  if ctx.author.guild_permissions.manage_channels:
    await guild.create_voice_channel(name='Team_1')
    await guild.create_voice_channel(name='Team_2')
    await guild.create_voice_channel(name='Lobby')
    mbed = discord.Embed(title='Success', description='Voice channels Team 1, Team 2 and Lobby has been created.')
    await ctx.send(embed=mbed)
    fetchVoiceChannels()
  else:     
    await ctx.send("No permissions")

# -------- DELETE CHANNELS -------- #
@bot.command()
async def delete_setup(ctx):
  existing_channel1 = discord.utils.get(ctx.guild.channels, name="Team_1")
  existing_channel2 = discord.utils.get(ctx.guild.channels, name="Team_2")
  existing_channel3 = discord.utils.get(ctx.guild.channels, name="Lobby")
  if existing_channel1 is not None and existing_channel2 is not None and existing_channel3 is not None:
    await existing_channel1.delete()    
    await existing_channel2.delete() 
    await existing_channel3.delete() 
  else:
    await ctx.send(f'No channel was found')

@bot.command(name="members", description="Show the all list of members in this server")
async def members(ctx):
  [print(member) for member in ctx.guild.members]  

# -------- WAKE UP SAMURAI - we have bot to burn -------- #
@bot.event
async def on_ready(): 
  msg = f'''
  BOT NAME     {bot.user.name}
  BOT ID       {bot.user.id}
  DIRECTORY    {os.path.abspath(os.getcwd())}

  ''' 
  print(msg)
  
  fetchVoiceChannels()

  await bot.change_presence(activity=discord.Game(name="$team help or mention"))  

bot.run("Not this time :)")





