"""

@title: Kami DDOS Bot
@repo: https://github.com/voipllc/kami
@since: 1/16/23
@author: vZy/Nefarious
@author_github: https://github.com/NefariousTheDev
"""
import discord, pytz
from datetime import datetime

from core.discord import *

from core.auth.users import *

from core.tools import *

prefix = "x"
time = datetime.now(pytz.timezone('EST'))
class Config:
    token = ""
    help_list = {"List of help commands (This)": f"{prefix}help",
    "Infomation of my discord and kami account": f"{prefix}myinfo",
    "Register a kami account": f"{prefix}register",
    "Geo Location": f"{prefix}geo <ip_address>",
    "Port Scanner": f"{prefix}pscan <ip_address>",
    "Domain Up or Down Status": f"{prefix}urlup <url>",
    "Account DB Lookup": f"{prefix}db <username|email|firstname|lastname|phone#>",
    "Stresser": f"{prefix}bbos <ip_address> <port> <time> <method>",
    "List of stresser plans": f"{prefix}prices",
    "About Kami": f"{prefix}kami"}
    

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"[ + ] {self.user} successfully loaded up.....")

    async def on_message(self, message):
        msg = message.content
        msg_args = (message.content).split(" ")

        if message.author == self.user: return
        if msg.startswith(prefix) == False: return

        kami_account = User().find(message.author.id)

        if msg == f"{prefix}help":

            msg = setEmbedInfo("Kami | Help", "List of help commands", Config.help_list)
            await DiscordUtilities.embed(message, msg, False)

        elif msg == f"{prefix}register":

            if kami_account.userid == f"{message.author.id}": return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Register", f"You are already reigstered to kami <@{message.author.id}>!", {}), False)
            
            u = setInfo(f"{message.author.name}", f"{message.author.id}", 0, 0, 0, 0)
            User().add(u)
            return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Register", f"You have succesfully register a kami account! <@{message.author.id}>", {}), False)

        elif msg == f"{prefix}myinfo":

            if kami_account.userid == f"{message.author.id}": # No KAMI Account
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | My Info", "Information of your discord and Kami account!", {"Discord Tag:": f"{message.author}", "Username:": f"{message.author.name}", "UserID:": f"{message.author.id}", "Kami Account": "You are not registered with kami!"}),  False)
            
            return await DiscordUtilities.embed(message, setEmbedInfo("Kami | My Info", "Information of your discord and Kami account!", {"Discord Tag:": f"{message.author}", "Username:": f"{message.author.name}", "UserID:": f"{message.author.id}", "Max Concurrents:": kami_account.max_con, "Max Time:": kami_account.max_time, "Mod Level:": kami_account.mod_level}), False)
        
        elif msg.startswith(f"{prefix}geo"):
            if len(msg_args) != 2: 
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | GeoIP Error", f"[ X ] Error, Invalid arguments provided\r\nUsage: {prefix}geo <ip_address>", {}), False)

            g = GeoIP(msg_args[1])
            if g._errCheck: 
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Geo Error", f"[ X ] Error, Unable to grab geo location on this IP Address ({msg_args[1]})!", {}), False)

            e = setEmbedInfo("Kami | GeoIP", "Location information on an ip address.", {"Status:": g._status, "Country:": g._country, "Country Code:": g._countryCode, "Region:": g._region, "Region Name:": g._regionName, "City:": g._city, "Zip Code:": g._zip, "Latitude/Longitude:": f"{g._lat}/{g._lon}", "Timezone": g._timezone, "ISP:": g._isp, "Org:": g._org, "AS:": g._as, "Querty:": g._query})
            await DiscordUtilities.embed(message, e, True)

        elif msg.startswith(f"{prefix}pscan"):
            if len(msg_args) != 2: 
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | GeoIP Error", f"[ X ] Error, Invalid arguments provided\r\nUsage: {prefix}geo <ip_address>", {}), False)
            
            ports = pScan(msg_args[1])
            await DiscordUtilities.embed(message, setEmbedInfo("Kami | Port Scanner", f"Display open ports to a network", ports), True)
            

        print(f"\x1b[31m[{time.month}/{time.day}/{time.year} % {time.hour}:{time.minute}]\x1b[0m{message.author}: \x1b[33m{msg}\x1b[0m")


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTA2NTE2NzA3MDUyMzgyNjE5OA.GQy_MG.zEg4zuGbJu_2Ggx7L4GPMV0Pg0IlKjeNKxcQC8')