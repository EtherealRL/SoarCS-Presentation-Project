from os import read
from re import L
import discord
from discord import user
from discord.ext import commands
from discord.utils import get
from discord.ext import tasks
import random as r
import csv
import time
from datetime import datetime, timedelta
import pytz
import asyncio
import json



client = commands.Bot(status=discord.Status.do_not_disturb, activity=discord.Game("SoarCS Leaderboard Bot"), command_prefix = '!')
client.remove_command('help')
filename = 'leaderboard.csv'
user_list = []






# --Exports to file
def write_users(user_list):
    with open(filename, 'w') as f:
        for sublist in user_list:
            line = "{},{},{}\n".format(sublist[0], sublist[1], sublist[2])
            f.write(line)
    


# --Imports the usernames
def read_users():
  user_list = []
  with open(filename, 'r+') as csvfile:
      datareader = csv.reader(csvfile)
      for row in datareader:
        user_list.append(row)
  return user_list



# --Makes the leaderboard
def create_leaderboard(users):
    global ldb
    users.sort(key=lambda a: int(a[2]), reverse=True)
    ldb = map(lambda user: user[1] + " - `" + str(user[2]) + '`', users)








@commands.has_any_role("Moderator", "Admin")
@client.command(aliases = ['r'])
async def register(ctx, user:discord.Member = None):
    try:
      user_exist = False
      user_list = read_users()
      for x in user_list:
          if str(user.id) in x:
              user_exist = True
              await ctx.send(embed = discord.Embed(title = f"Error!", description = f"{user.mention} has already been registered!"))
              break
      if not user_exist:
        username = str(user)[:-5]
        newUser = [f'{user.id}', f'{username}', 0]
        user_list.append(newUser)
        write_users(user_list)
        registered = discord.Embed(title = "User registered:",
                                                      description = f"{user.mention} has been registered!",
                                                      color=discord.Color.blue())
        await ctx.channel.send(embed = registered)
                    

    except Exception as e:
        print(e)


@commands.has_any_role('Moderator', 'Admin')
@client.command(aliases = ['pts'])
async def points(ctx, user:discord.Member = None, points = None):
    try:
        if points != None:
            points = int(points)
            if type(points) == int:
                user_exist = False
                user_list = read_users()
                for x in range(len(user_list)):
                    if str(user.id) == user_list[x][0]:
                        user_exist = True
                        user_list[x][2] = points
                        points_add = discord.Embed(title="Points adjusted for player",
                                  description = str(user.mention) + 'now has ' + str(points) + ' points.',
                                  color=discord.Color.blue())
                        await ctx.channel.send(embed = points_add)
                        write_users(user_list)
                        break
                if not user_exist:
                    await ctx.send("Could not find user!")
    except Exception as e:
        print(e)


@commands.has_any_role('Admin', 'Moderator')
@client.command()
async def nick(ctx, user:discord.Member, nickname = None):
    if user != None and nickname != None:
        user_list = read_users()
        user_exist = False
        name_taken = False
        for x in range(len(user_list)):
            if str(user.id) == user_list[x][0]:
                user_exist = True
            if user_exist:
                for x in range(len(user_list)):
                    if nickname == user_list[x][1]:
                        name_taken = True
                    break
                if not name_taken:
                    user_list[x][1] = nickname
                    nick_changed = discord.Embed(title = f"Nickname changed!", description = str(user.mention) + "\'s nickname was changed to: " + nickname)
                    await ctx.send(embed = nick_changed)
                    write_users(user_list)
                    break
            else:
                await ctx.send("Name is already taken!")
                if not user_exist:
                    await ctx.send("Please register before changing your nickname.")
        if not user_exist:
            await ctx.send("Could not find user.")



@client.command(aliases = ['lb'])
async def leaderboard(ctx):
    try:
        global ldb
        user_list = read_users()
        create_leaderboard(user_list)
        lb_display = discord.Embed(title="Leaderboard:",
                        description = "\n".join(ldb),
                        color=discord.Color.blue())
        await ctx.channel.send(embed = lb_display)
    except Exception as e:
        print(e)


@client.command()
async def whois(ctx, nickname = None):
    if nickname != None:
        user_list = read_users()
        for x in range(len(user_list)):
            if nickname == user_list[x][1]:
                found_person = discord.Embed(title = f"Person found!", description = nickname + " is: <@" + str(user_list[x][0]) + ">")
                await ctx.send(embed = found_person)


@client.command()
async def profile(ctx, user:discord.Member = None):
    try:
        if user != None:
            user_exist = False
            user_list = read_users()
            for x in range(len(user_list)):
                if str(user.id) == user_list[x][0]:
                    user_exist = True
                    profile_embed = discord.Embed(title="Player found!",
                                description = str(user.mention) + ' has ' + user_list[x][2] + ' points.',
                                color=discord.Color.blue())
                    await ctx.channel.send(embed = profile_embed)
                    write_users(user_list)
                    break
            if not user_exist:
                await ctx.send("Could not find user!")
        else:
            user_exist = False
            user_list = read_users()
            for x in range(len(user_list)):
                if str(ctx.author.id) == user_list[x][0]:
                    user_exist = True
                    profile_embed = discord.Embed(title="Player found!",
                                description = str(ctx.author.mention) + ' has ' + user_list[x][2] + ' points.',
                                color=discord.Color.blue())
                    await ctx.channel.send(embed = profile_embed)
                    write_users(user_list)
                    break
            if not user_exist:
                await ctx.send("Could not find user!")
    except Exception as e:
        print(e)

        



@client.event
async def on_ready():
    print("Bot is ready.")



token = open('token.txt', 'r')
client.run(token.read())
