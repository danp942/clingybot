import discord
import responses
import datetime 
import time

#not able to take multiple, needs to be hosted somewhere
month_day_calendar = ['skip',30,28,3]
# import os
#rhi,monday, 4:30pm
#rhi,1/5/24, 2pm
async def send_message(message, user_message, guilds, is_private):
    # try:
    for guild in guilds: 
        if guild.name == 'King DeedleP\'s server':
            user_message = user_message.lower()
            msgList = user_message.split(',')
            acc_mesage = msgList[0][msgList[0].find('r')+1:]
            print(acc_mesage)
            now = datetime.datetime.now()
            #1/5/24, 4:30pm
            #mon, 4pm
            date = msgList[1]
            timeofday = msgList[2]
            hour,min = hour_parse(timeofday)
            await message.channel.send(f'{message.author.mention} set a reminder to do {acc_mesage} at {timeofday}')
            
            if '/' in date:
                
                date = date.split('/')
                month = int(date[0])
                day = int(date[1])
                year = int(date[2]) + 2000
                
                later = datetime.datetime(year,month,day,hour,min)
                
            else:
                if date == 'mon':
                    daynum = 0
                if date == 'tue':
                    daynum = 1
                if date == 'wed':
                    daynum = 2
                if date == 'thu':
                    daynum = 3
                if date == 'fri':
                    daynum = 4
                if date == 'sat':
                   daynum = 5
                if date == 'sun':
                    daynum = 6
                    
                if daynum < now.weekday():
                    daynum += 7
                daydiff = daynum-now.weekday()
                daylater = now.day + daydiff
                later = datetime.datetime(now.year,now.month,daylater,hour,min)
                #got seconds for how many days
                #got how many hours until
                
            
                
                
                
            #message
            difference = later - now
            
            #need to get months...
            seconds = int(difference.total_seconds())
            
            
            text_log = await guild.fetch_channel(1247378604321538129)    
            textLogMsg = f'{message.author.mention} / {message.author} set up a reminder to {acc_mesage}'
            await text_log.send(textLogMsg)
            
            response = responses.handle_response(acc_mesage, message.author, msgList[1], msgList[2])

            if seconds > 604800:
                sleeptime = seconds-604800
                time.sleep(sleeptime)
                seconds -= sleeptime
                await message.author.send(f'{message.author.mention} Hey, 1 week until you need to do {acc_mesage}...remember, it\'s at {timeofday}')
            
            if seconds > 172800:
                sleeptime = seconds-300
                time.sleep(sleeptime)
                seconds -= sleeptime
                await message.author.send(f'{message.author.mention} Hey, 2 days until you need to do {acc_mesage}...remember, it\'s at {timeofday}')
            
            if seconds > 86400:
                sleeptime = seconds-86400
                time.sleep(sleeptime)
                seconds -= sleeptime
                await message.author.send(f'{message.author.mention} Hey, 1 day until you need to do {acc_mesage}...remember, it\'s at {timeofday}')
            
            if seconds > 18000:
                sleeptime = seconds-18000
                time.sleep(sleeptime)
                seconds -= sleeptime
                await message.author.send(f'{message.author.mention} Hey, 5 hours until you need to do {acc_mesage}...remember, it\'s at {timeofday}')
            
            if seconds > 7200:
                sleeptime = seconds-7200 
                time.sleep(sleeptime)
                seconds -= sleeptime
                await message.author.send(f'{message.author.mention} Hey, 2 hours until you need to do {acc_mesage}...remember, it\'s at {timeofday}')
            
            if seconds > 3600:
                sleeptime = seconds-3600
                time.sleep(sleeptime)
                seconds -= sleeptime
                await message.author.send(f'{message.author.mention} Hey, 1 hour until you need to do {acc_mesage}...remember, it\'s at {timeofday}')
            
            if seconds > 300:
                sleeptime = seconds-300
                time.sleep(sleeptime)
                seconds -= sleeptime
                await message.author.send(f'{message.author.mention} Hey, 5 minutes until you need to do {acc_mesage}...remember, it\'s at {timeofday}')
            if seconds > 60:
                sleeptime = seconds-60
                time.sleep(sleeptime)
                seconds -= sleeptime
                await message.author.send(f'{message.author.mention} Hey, one minute until you need to do {acc_mesage}...remember, it\'s at {timeofday}')
            
            if seconds > 5:
                sleeptime = seconds-5
                time.sleep(sleeptime)
                seconds -= sleeptime
                for i in range(20):
                    await message.author.send(f'{message.author.mention} Hey, it\'s happening RIGHT NOW! You need to do {acc_mesage.upper()} right NOW at{timeofday}!!!!')
                    time.sleep(.5)
                    
    # except Exception as e:
    #     print(e, 1)

    

def hour_parse(rawtime):
    #4:30pm
    #4pm
    #430pm
    isam,ispm = False, False
    rawtime = rawtime.strip()
    if ':' in rawtime:
        rawtime = rawtime[:rawtime.find(':')] + rawtime[rawtime.find(':')+1:]
    if 'am' in rawtime:
        isam = True
        rawtime = rawtime[:rawtime.find('am')]
    elif 'pm' in rawtime:
        ispm = True
        rawtime = rawtime[:rawtime.find('pm')]

    if len(rawtime) == 4:
        hour = int(rawtime[:2])
        min = int(rawtime[2:])
    if len(rawtime) == 3:
        hour = int(rawtime[:1])
        min = int(rawtime[1:])
    if len(rawtime) == 1 or len(rawtime) == 2:
        hour = int(rawtime)
        min = 0
    
    if isam != True and ispm != True:  #operating on the assumption that if i say 7, it's likely 7pm
        ispm = True
    
    if ispm:
        hour += 12
    
    return hour, min


def run_discord_bot():
    intents=discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    #token goes here, dm me if you want it    
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
    
    @client.event
    async def on_message(message):
        if message.author != client.user: #client.user is the FUCKING BOT bruh
            username = str(message.author)
            user_message = str(message.content).lower()
            channel = str(message.channel)
            split = user_message.split()
            if split[0][0] == 'r':
                user_message = user_message[1:]
                await send_message(message, user_message, client.guilds, is_private=True)
                
                
                
                
    client.run(TOKEN)        
                