import json
from PIL import Image
import requests
from io import BytesIO
from nudenet import NudeDetector
from nudenet import NudeClassifier
import server.censoring as cen
import discord
from discord.ext import commands


class BotRequest(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_request(self):
        # server url
        url = 'https://endless-orb-325023.ue.r.appspot.com/nude-net'
        res = requests.get(url)
        res_content = json.loads(res.content)
        return res_content

    @commands.command(name='info', aliases=['pp', 'pipo'])
    async def info(self, ctx):
        async with ctx.typing():
            a = self.get_request()
        await ctx.send(a)

    @commands.command(name='ppp')
    async def ppp(self, ctx):
        await ctx.channel.purge(limit=1)
        async with ctx.typing():
            url = ctx.message.attachments[0].url
            #print(url)
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            imagePath = "nsfw.png"
            img.save(imagePath)

            detector = NudeDetector()  # detector = NudeDetector('base') for the "base" version of detector.
            detector = detector.detect(imagePath)
            #classifier = NudeClassifier()
            #print(1)
            #pokemon = classifier.classify(imagePath)
            sfw_path = cen.censorImage(detector, imagePath, "")
            with open(sfw_path, "rb") as fh:
                f = discord.File(fh, filename=sfw_path)
            await ctx.send(file=f)

