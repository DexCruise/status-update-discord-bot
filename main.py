import json

import discord
import icmplib
import time
import requests


class Client(discord.Client):
    started = False

    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print("logged in")

    async def on_message(self, message):
        if self.started:
            return
        if "__PING_BOT_INIT" != message.content:
            return
        print(message.content)
        print("sending")
        msg = await message.channel.send("_")
        await message.delete()
        self.started = True
        while 1:
            await msg.edit(content=get_update())
            time.sleep(300)


pinged_addresses = {  # K: address, V: pretty name
    "google.com": "google",
    "beetransit.ca": "beetransit",
}

status_json = {
    "https://discordstatus.com/api/v2/status.json": "discord_api",
    "https://www.cloudflarestatus.com/api/v2/status.json": "cloudflare"
}

def get_update() -> str:
    lines: list[str] = []

    for i in pinged_addresses.keys():
        lines.append(f"{pinged_addresses[i]}={'UP' if icmplib.ping(i, count=1, privileged=False).is_alive else 'DOWN'}")

    for i in status_json.keys():
        s = json.loads(requests.get(i).content)["status"]["description"]
        lines.append(f"{status_json[i]}='{s}'")

    return "```toml\n" + '\n'.join(lines) + "\n```"


t = open("token").read()
Client().run(t)
