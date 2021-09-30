import discord
import os
import random
from discord.ext import commands, tasks
from discord.ext.commands import check

intents = discord.Intents.default() # Discord policy
intents.members = True # Discord policy
lol_squad = [] # Leageu of legends teams container
voice_channel_list = [] # Fetch all channels from server 
voiceChannel_1, voiceChannel_2 = None, None # Index of voice channel
team1, team2 = 0, 0 # Points
globalPlayers = []

#sanetro

bot = commands.Bot(intents=intents, command_prefix='$', help_command=None) # Client object app name - bot, command always start with '$' before
TOKEN = "ODM2Mzc4NTQ0MzI1MDAxMjM3.YIdIOA.96DQt9PKaMtHuKpkNDoM60pRW4U"

class Player:

  def __init__(self, name, point=0):    
    self.point = point
    self.name = name 

  def add(self):
    self.point = self.point + 1

  def update(self, nameImport, pointImport):
    self.point = pointImport
    self.name = nameImport

  def id(self):
    print(self.name, self.point)
  
  def giveName(self):
    return self.name


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
 
# -------- PLAYERS LIST -------- #
def returnListOfSqad_lol(lol_squad):
  tmp = ">>> \n**Here is your players list**:\n\n"
  for i in range(len(lol_squad)): tmp +=  f"{i+1}\t" + str(lol_squad[i].name) + "\n"
  return tmp 


# -------- RANDOMIZE ALL PLAYERS -------- #
# Description : shuffle and draws teams 
@bot.command(name="rand", description="Shuffle and draws teams ")
async def rand(ctx):  
  teamINFO = ""
  random.shuffle(lol_squad)

  teamINFO += "\n╔═════╬**Team 1**╬═════\n║\n"
  for i in range(0, len(lol_squad), 2): teamINFO += f" ╠ **{lol_squad[i].name}**\n"
  teamINFO += "\n\n╔═════╬**Team 2**╬═════\n║\n"
  for i in range(1, len(lol_squad), 2): teamINFO += f" ╠ **{lol_squad[i].name}**\n" 
  teamINFO += "\n\nGood luck! dont't forget to ban Jhin."

  mbed = discord.Embed(title='Lol Team Custom Randomize', description=teamINFO, colour = discord.Colour.default())  
  await ctx.send(embed=mbed)

# -------- SET PLAYERS -------- #
# Description
# Input users after 'at' (@) symbol. For example: $players @sanetro @someone @etc ... 
@bot.command(name="players", description="Add to list a player to draw for one of the team")
async def players(ctx, *members : discord.Member):  
  global lol_squad 
  for user in members:
    if not user in lol_squad:
      lol_squad.append(user)
      globalPlayers.append(Player(user.name))
    else:
      await ctx.send(f"The **{user.name}** is already on the list.")
  await ctx.send(returnListOfSqad_lol(lol_squad))
#for member in lol_squad: objectsOfPlayers.append(Player(member.name))
# -------- REMOVE PLAYERS -------- #
# Description
# Same function as players() but it removes player from list
@bot.command(name="remove", description="Remove player from list")
async def remove(ctx, *members : discord.Member):  
  global lol_squad 
  for user in members:
    if user in lol_squad:
      lol_squad.remove(user)
    else:
      await ctx.send(f"The **{user.name}** isn't on the list.")

# -------- CLEAR PLAYERS -------- #
@bot.command(name="clear", description="Clear list of squad")
async def clear(ctx):  
  global lol_squad; lol_squad = []; await ctx.send(f"List is empty.")

# -------- MOVE ALL USERS -------- #
# Description
# Most important. This sends members to particular channels ('Team_1'; 'Team_2')
# It sends a embed (something like message, but with better border)
@bot.command(name="start", description="It moves teams to channels. (Start of the game)")
async def start(ctx):  
  global lol_squad
  vc1 = voice_channel_list[voiceChannel_1]
  vc2 = voice_channel_list[voiceChannel_2]
  for i in range(len(lol_squad)):
    try:
      if(i % 2 == 0):
        await lol_squad[i].move_to(vc1)
        mbed = discord.Embed(title='{} moved to {}.'.format(lol_squad[i].name, vc1),
                          description="start by {}".format(ctx.message.author.name),
                          colour = discord.Colour.orange())
      else:
        await lol_squad[i].move_to(vc2)
        mbed = discord.Embed(title='{} moved to {}.'.format(lol_squad[i].name, vc2),
                          description="start by {}".format(ctx.message.author.name),
                          colour = discord.Colour.purple())
      
    except:
      mbed = discord.Embed(title='Player problem', 
                          description="{} isn't in voice channel.".format(lol_squad[i].name),
                          colour = discord.Colour.red())      
    await ctx.send(embed=mbed)

# -------- SHOW - list of squad -------- #
@bot.command(name="show", description="Simple list of players in squad")
async def show(ctx): 
  await ctx.send(returnListOfSqad_lol(lol_squad))


# -------- RESET -------- #
@bot.command(name="reset", description="reset score")
async def reset(ctx): 
  team1, team2 = 0, 0; await ctx.send(justify_score_board(team1,team2))

# -------- SCORE -------- #
@bot.command(name="score", description="Shows score of team one and team two")
async def score(ctx): 
  await ctx.send(justify_score_board(team1,team2))



# -------- TOP -------- #
@bot.command(name="top", description="Shows top list")
async def top(ctx): 
  objectsOfPlayers = []
  with open("Toplist.txt", "r") as file:
    for index, line in enumerate(file):
      record = line.split()
      objectsOfPlayers.append(Player(record[0], int(record[1]))) # 0 - name; 1 - points
  file.close()

  playersList = "\n\n"
  sortedList = sorted(objectsOfPlayers, key=lambda x: x.point, reverse=True)    
  
  for index in range(len(sortedList)-1):
      if index == 0:
        playersList += f"\n{index+1}                         ✨👑 **{sortedList[index].name}** 👑✨ ({sortedList[index].point})\n\n"
      elif index == 1:
        playersList += f"{index+1}                                ✨ **{sortedList[index].name}** ✨ ({sortedList[index].point})\n\n"
      elif index == 2:
        playersList += f"{index+1}                                🔥 **{sortedList[index].name}** 🔥 ({sortedList[index].point})\n\n"
        playersList += "════════════════════════════\n"
      else:
        playersList += f"{index+1} **{sortedList[index].name}** ({sortedList[index].point})\n"
      
  mbed = discord.Embed(title='═════LIST OF BEST PLAYERS═════',
                          description=playersList,
                          colour = discord.Colour.gold())
  await ctx.send(embed=mbed)

# -------- addpoint - team 1 - team 2 -------- #
@bot.command(name="addpoint", description="Give one point to team. $team 1 - gives one point to first team. $team 2 - gives one point to second team")
async def addpoint(ctx, index): 
  global team1, team2
  objectsOfPlayers = []

  with open("Toplist.txt", "r") as file:
    for line in file:
      record = line.split()
      print(record[0], int(record[1]), type(record[0]), type(int(record[1])))
      objectsOfPlayers.append(Player(record[0], int(record[1]))) # 0 - name; 1 - points
  file.close()

  for user in globalPlayers:
    if not user in objectsOfPlayers:
       objectsOfPlayers.append(Player(user.name, 0))

  with open("Toplist.txt", "w") as file:
    for user in objectsOfPlayers:
      file.write(f"{user.name} {str(user.point)}\n")
  file.close()
        
  #TODO I must solve what happens to user.name, I need string not object 

  if index == "1": 
    team1 += 1
    for i in range(0, len(objectsOfPlayers), 2): objectsOfPlayers[i].add()
  elif index == "2": 
    team2 += 1
    for i in range(1, len(objectsOfPlayers), 2): objectsOfPlayers[i].add()
  else: 
    await ctx.send("Please choose between 1 and 2. Thanks.", index)
  if index == "1" or index == "2": await ctx.send(justify_score_board(team1, team2)) 


@bot.command(name="about", description="All you need to know about me and bot.")
async def about(ctx):   
  await ctx.message.author.send(voice_channel_list[voiceChannel_1])


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
@bot.command(name="setenv", description="Create environment for bot to set up your homies in voice channels. (TYPE THIS COMMAND FIRST)")
async def setenv(ctx):
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

# -------- DELETE CHANNELS OF ENV -------- #
@bot.command(name="delete_env", description="Show the all list of members in this server")
async def delete_env(ctx):
  existing_channel1 = discord.utils.get(ctx.guild.channels, name="Team_1")
  existing_channel2 = discord.utils.get(ctx.guild.channels, name="Team_2")
  existing_channel3 = discord.utils.get(ctx.guild.channels, name="Lobby")
  if existing_channel1 is not None and existing_channel2 is not None and existing_channel3 is not None:
    await existing_channel1.delete()    
    await existing_channel2.delete() 
    await existing_channel3.delete() 
  else:
    await ctx.send(f'No channel was found')

@bot.command()
async def help(ctx):
  helpMessage = """>>> \n**List of commands**\n
  **delete_env**                Show the all list of members in this server

  **setenv**                        Create environment for bot to set up your
                                       homies in voice channels. (TYPE THIS FIRST)

  **addpoint**                    Give one point to team:
                                       $addpoint 1 - gives one point to first team
                                       $addpoint 2 - gives one point to second team

  **about**                         All you need to know about me and bot      

  **score**                          Shows score of team one and team two

  **start**                           It moves teams to channels. (Start of the game)

  **clear**                           Clear list of squad

  **remove**                       Remove player from list

  **players**                      Add to list a player to draw for one of the team

  **rand**                           Shuffle and draws teams

  **reset**                         Reset score

  **show**                           Show score

  **top**                              Show list of players who got many wins (TOP of)
  """ 

  await ctx.send(helpMessage)
# -------- WAKE UP BOT - we have a world to burn -------- #
@bot.event
async def on_ready(): 
  msg = f'''
  BOT NAME     {bot.user.name}
  BOT ID       {bot.user.id}
  DIRECTORY    {os.path.abspath(os.getcwd())}
  '''
  print(msg)  
  fetchVoiceChannels()
  await bot.change_presence(activity=discord.Game(name="$help or mention"))

  

bot.run(TOKEN)





