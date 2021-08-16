# Version: 1.0.7

import discord 
import os
import random
import json
from keep_alive import keep_alive
from discord.ext import commands, tasks


#Leageu of legends teams container
lol_squad = []
team1, team2 = 0, 0


#Client object app name - bot 
#Command always start with '$' before
bot = commands.Bot(command_prefix='$')

# Function return entire board with seperate teams
def justify_lead_board(lol_squad):
  border = "="*34; tabs = "\t"*3
  tmp2 = f'''```json
  "{border}"\n  "{tabs}Team 1{tabs}\t"\n  "{border}"```'''
  tmp3 = f'''```ini
  [{border}]\n  [{tabs}Team 2{tabs}\t]\n  [{border}]```'''
  result = tmp2; i = 0
  for user in lol_squad:
    if i % 2 == 0:
      result += "\t\t\t>>> - " + user + "\n"
    i+=1 
  result += tmp3; i = 0
  for user in lol_squad:
    if i % 2 != 0:
      result += "\t\t\t>>> - " + user + "\n"
    i+=1 
  return result

def justify_score_board(team1,team2):
  tmp = f'```diff\n\n+\t\tTeam 1\t\tTeam 2\n-\t\t  {team1}\t\t:\t  {team2}\n\n```'
  tmp = f'''
  ```diff
   ______________________________________________________
  (__   __________________   ________________________   _)
    | |                   | |                        | |
  \t\t\tTEAM 1\t\t\t\t  TEAM 2                         
  \t\t\t  {team1}\t\t\t\t\t\t{team2}                   
   _| |___________________| |________________________| |
  (_____________________________________________________) 
  ```'''
  return tmp

def returnListOfSqad_lol(lol_squad):
  tmp = "Here is your users list:\n"
  for user in lol_squad:
    tmp +=  "\t- " + user + "\n"
  return tmp 

def getDatabaseTamplate():  
  with open("db_temp.json") as file:
    data = json.load(file)
  return data


def serverCheckInDatabase(name):
  return True

def getDatabaseByServerName(name):
  pass


@bot.command()
async def team(ctx, *args): #When user add more args then 2
    global lol_squad, team1, team2 # containers
    
    server_curr_name = ctx.message.guild.name # name of server 
    #if not serverCheckInDatabase(server_curr_name):
    #AddCurrServerToDatabase(server_curr_name)
    template = getDatabaseTamplate()
    #server_content = getDatabaseByServerName(server_curr_name) 
   

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
      if args[0] in ["help", "-h", "h"]: # If i need help just type this 
        await ctx.send(helpArgs)

      if args[0] == "showlist": # show list of added users 
        await ctx.send(returnListOfSqad_lol(lol_squad))

      if args[0] == "clear": # If i need to clean up list 
        lol_squad = []
        await ctx.send("List is empty.")

      if args[0] == "add": # If i need to add user to list 
        print(len(args) + len(lol_squad))
        if len(args) + len(lol_squad) > 11: # you can't do it if users are more then 10
          await ctx.send(f"I can't add user/users! Type only: {10 - len(lol_squad)} user/s")
        else:
          for i in range(1, len(args)): # add args to list till the end
            lol_squad.append(args[i])
          await ctx.send(f"Added: {args[1:]}\n") # inform me if you added

      if args[0].lower() == "remove":  # delete every user name from list 
        for i in range(1, len(args)):
          try: 
            lol_squad.remove(args[i]) # deleted: in list 
            await ctx.send(f"Removed: {args[i]}\n") # deleted: message
          except:
            await ctx.send(f"Can't remove or doesn't exist: {args[i]}\n") # when user aren't in list

      if args[0] == "rand": # here is a output of randomized users in each team
        if len(lol_squad) == 10:
          random.shuffle(lol_squad)
          await ctx.send(justify_lead_board(lol_squad))
        else:
          await ctx.send(f"Not enought number of users, wanted: {10 - len(lol_squad)}") # if you have less then 10 users

      if args[0] == "score":
        await ctx.send(justify_score_board(team1,team2))
      if args[0] == "addpoint" and args[1] == "1":
        if team1 < 10:
          team1 += 1
        await ctx.send(justify_score_board(team1,team2))      
      if args[0] == "addpoint" and args[1] == "2":
        if team2 < 11:
          team2 += 1
        await ctx.send(justify_score_board(team1,team2))
      if args[0] == "reset":
        team2, team1 = 0, 0
        await ctx.send(justify_score_board(team1,team2))
    except IndexError:
      await ctx.send("Wrong command: type **$team help**") # bad entry
pass

@bot.command()
async def serwer(ctx):
    # {ctx.message.channel.mention}
    # ctx.message.author.send(ctx.message.guild.name)
    await ctx.send(ctx.message.guild.name)

@bot.event
async def on_message(message):
    mention = f'<@!{bot.user.id}>'
    welcomeText = f'''
    Hello @everyone,

    I am a **{bot.user.name}** bot who can set teams in League of Legends. 
    Only applies to custom matches. I was created so that people would not unnecessarily go to some team draw web pages.
    To use me please write:"*$team help*" to learn the commands. For example:

    *$team add* Apple Bannana Chair ...

    (You should fill up to 10 slots), then:

    *$team rand*

    and voilà... contact: **sanetro26@gmai.com**
    '''
    if mention in message.content:
      await message.channel.send(welcomeText)
    else:
      await bot.process_commands(message)

@bot.command()
async def createchannel(ctx, channelName):
  guild = ctx.guild
  mbed = discord.Embed(title='Success', description='{} has been created.'.format(channelName))
  # if ctx.author.guild_permissions.manage_channels:
  await guild.create_text_channel(name='{}'.format(channelName))
  await ctx.send(embed=mbed)


@bot.event
async def on_ready():
  
  print("STATUS MOD\tSTART")
  print(f"BOT NAME\t{bot.user.name}")
  print(f"BOT ID\t\t{bot.user.id}")
  print(f"DIRECTORY\tP{os.path.abspath(os.getcwd())}")
  await bot.change_presence(activity=discord.Game(name="Type: '$team help' or mention me "))
  # bot.change_presence(activity=discord.Game("Type: '$team help'")
  '''
  for guild in bot.guilds: # guild stands for server
      for channel in guild.channels:
          if isinstance(channel, discord.TextChannel): # Check if channel is a text channel
              await channel.send("Proszę szybko mnie usunąć. Może dojść do niepotrzebnych duplikowania się kanałów. Please remove me quickly. There may be unnecessary duplication of channels.")
  '''
    

keep_alive() # Flask serwer to keep bot alive 24/7
bot.run(os.getenv("TOKEN2")) # My key to bot
