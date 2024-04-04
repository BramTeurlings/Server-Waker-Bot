# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
import discord
from wakeonlan import send_magic_packet
import os
import time as baseTime
from datetime import datetime, time

TOKEN = ""
with open('token.txt') as f:
    TOKEN = f.readline().strip('\n')
    
MAC = ""
with open('mac.txt') as f:
    TOKEN = f.readline().strip('\n')
    
IP = ""
with open('ip.txt') as f:
    TOKEN = f.readline().strip('\n')

QUOTES_CHANNEL = ""
with open('quotes.txt') as f:
    TOKEN = f.readline().strip('\n')

startHour = 23
startMinute = 50
endHour = 8
endMinute = 0

connectionFailed = True

timeArray = [str(startHour), str(startMinute), str(endHour), str(endMinute)]


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def timeFormatter(time):
    # Formats the server's closed times to look pretty and always have 4 digits total.
    formattedTime = ""

    if len(time) < 2:
        formattedTime += "0" + str(time)
    else:
        formattedTime = time

    return formattedTime


while connectionFailed:
    try:
        client = discord.Client()
        connectionFailed = False
    except:
        print("An error occurred while connecting to Discord. Trying again in 10 seconds...")

    baseTime.sleep(10)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/wake'):
        if is_time_between(time(startHour, startMinute), time(endHour, endMinute)):
            for idx, val in enumerate(timeArray):
                timeArray[idx] = timeFormatter(val)

            serverClosedMessage = "Server is closed between " + str(timeArray[0]) + ":" + str(timeArray[1]) + " and " + str(timeArray[2]) + ":" + str(timeArray[3]) + ". Please try again later."
            await message.channel.send(serverClosedMessage)
        else:
            send_magic_packet(MAC, ip_address=IP, port=9)
            await message.channel.send('Waking server up... Please wait a few minutes.')
    if message.content.startswith('/quote'):
        message.channel.send(random_message(QUOTES_CHANNEL))
client.run(TOKEN)

async def random_message(channel_id: int):
    try:
        messages = await channel_id.history(limit=100).flatten()
        random_message = random.choice(messages)
        return(random_message)
    except discord.Forbidden:
        return("I don't have permission to read messages in that channel")
 


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
