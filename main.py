import msvcrt
import nextcord
from nextcord.ext import commands
import os
import json
from time import sleep
from colorama import Fore as color_fg
from colorama import Style as color_style
from colorama import Back as color_bg
from colorama import init as color_init

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(
    activity=nextcord.Activity(
        name="grass grow", type=nextcord.ActivityType.watching
    ),
    intents=intents,
)

with open("settings.json") as f:
    settings = json.loads(f.read())

color_init(True)

servers = []
for i in os.listdir("./Servers/"):
    if i.endswith(".dcsrv"):
        servers.append(i)

current_server = 0

class dcsrv():
    name = "Default"
    desc = "Default"

    category_start = ""
    category_end = ""

    channel_start = ""
    last_channel_start = ""

    channels = {
    #    "Info": [
    #        ["Rules","text"],
    #        ["Random","vc",0]
    #        ["Limited","vc",6]
    #    ]
    }


def interpret_file(filename):
    with open(filename,"r",encoding="utf-8") as f:
        file = f.read()
    whereami = ""
    category = ""
    srv = dcsrv()
    
    for line in file.split("\n"):
        # Category
        if line.startswith("=="):
            whereami = (line + " ")[3:-1]
        elif line != "":
            # Contents
            if whereami == "DATA":
                what = line.split("=")[0]
                value = line.split("=")[1]

                if what == "NAME":
                    srv.name = value
                if what == "DESC":
                    srv.desc = value

            if whereami == "DECORATION":
                what = line.split("=")[0]
                value = line.split("=")[1]

                if what == "CATEGORY_START":
                    srv.category_start = value
                if what == "CATEGORY_END":
                    srv.category_end = value
                if what == "CHANNEL_START":
                    srv.channel_start = value
                if what == "LAST_CHANNEL_START":
                    srv.last_channel_start = value

            if whereami == "CHANNELS":
                if line[0] == "#":
                    category = (line + " ")[2:-1]
                if not category in list(srv.channels.keys()):
                    srv.channels[category] = []
                if line[0] == "-":
                    srv.channels[category].append([(line + " ")[2:-1],"text"])
                if line[0] == "+":
                    the = line.split("+") # I apologize to the person reading over my code, i have no idea what to name any of my variables.
                    #srv.channels[category].append([(line + " ")[2:-1],"vc"])
                    srv.channels[category].append([(the[2] + " ")[1:-1],"vc",int(the[1][2:-2])])
    return srv

created_srv = None

def select_server(e):
    global created_srv
    os.system("cls")
    global current_server
    if len(servers) > current_server+e and current_server+e >= 0:
        current_server += e
    print("Select a server.\nPress [W] or [S] to scroll\nPress [E] to select:")
    for servfile in servers:
        serv = servfile.split(".")[0]
        if servers[current_server] == servfile:
            print(color_fg.CYAN + serv + " <")
        else:
            print(color_fg.BLUE + serv)
    char = str(msvcrt.getch())[2:-1]
    if char == "s":
        select_server(1)
    elif char == "w":
        select_server(-1)
    elif char == "e":
        print("Processing...")
        created_srv = interpret_file("./Servers/" + servers[current_server])
    else:
        select_server(0)    

select_server(0)
print("Starting bot...")

@bot.event
async def on_ready():
    print("Waiting...")
    sleep(5)
    print("Fetching server...")
    actualsrv: nextcord.Guild = await bot.fetch_guild(settings["channel_id"])
    print("Building server...")
    count = 0
    for category_name in created_srv.channels.keys():
        channels = created_srv.channels[category_name]
        category: nextcord.CategoryChannel = await actualsrv.create_category(created_srv.category_start + category_name + created_srv.category_end)
        for channel_name in channels:
            count += 1

            name = created_srv.channel_start + channel_name[0]
            if channels[-1] == channel_name:
                name = created_srv.last_channel_start + channel_name[0]

            if channel_name[1] == "vc":
                channel: nextcord.VoiceChannel = await category.create_voice_channel(name)
                channel.user_limit = channel_name[2]
            elif channel_name[1] == "text":
                channel: nextcord.TextChannel = await category.create_text_channel(name)

            print(f"{category.id} ~ {channel.id}\n{category.name} ~ {channel.name}\n\n")
            if count%settings["limit_between_rests"] == 0:
                sleep(settings["rest_length_seconds"])
    print("Done! Feel free to CTRL+C this.")

bot.run(settings["bot_key"])