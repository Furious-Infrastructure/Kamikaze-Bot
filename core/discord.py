import random, discord

class EmbedInfo:
    title: str
    description: str
    fields: dict

def setEmbedInfo(t: str, d: str, f: dict) -> EmbedInfo:
    e = EmbedInfo
    e.title = t
    e.description = d
    e.fields = f
    return e

class DiscordUtilities:
    async def embed(message, info: EmbedInfo, iln: bool) -> None:
        embedVar = discord.Embed(title=info.title, description=info.description, color=0xff0000)
        
        if info:
            for key in info.fields:
                val = info.fields[key]
                embedVar.add_field(name=f"{key}", value=f"{val}", inline=iln)

        await message.channel.send(embed=embedVar)