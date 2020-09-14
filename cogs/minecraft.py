import discord
from discord.ext import commands
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import asyncio
from chromedriver_py import binary_path

USER = ''
PASSWORD = ''
URL = "https://aternos.org/go/"

class Minecraft(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.connected = False

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125")

        self.driver = webdriver.Chrome(options=self.options, executable_path=binary_path)

    def is_online(self):
        data = requests.get("https://mcapi.xdefcon.com/server/vismaypikachu2.aternos.me/full/json").json()
        return data["version"] != '\u00a74\u25cf Offline'
    
    async def connect_account(self):
        self.driver.get(URL)
        element = self.driver.find_element_by_xpath('//*[@id="user"]')
        element.send_keys(USER)
        element = self.driver.find_element_by_xpath('//*[@id="password"]')
        element.send_keys(PASSWORD)
        element = self.driver.find_element_by_xpath('//*[@id="login"]')
        element.click()
        self.connected = True
        print("connected!")
        await asyncio.sleep(10)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Minecraft cog is online")
    
    @commands.command()
    async def online(self, ctx):
        if not self.is_online():
            embed = discord.Embed(description="The server is offline!", color=0xff0000)
        else:
            embed = discord.Embed(description="The server is online!", color=0x00ff00)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def start(self, ctx):
        if self.is_online():
            embed = discord.Embed(description="The server is already online!", color=0x00ff00)
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(description="Starting server...", color=0x00ff00)
        await ctx.send(embed=embed)

        if not self.connected:
            await self.connect_account()
        await asyncio.sleep(5)
        element = self.driver.find_element_by_xpath("/html/body/div/main/section/div/div[2]/div[1]/div[1]")
        element.click()
        await asyncio.sleep(3)
        element = self.driver.find_element_by_xpath('//*[@id="start"]')
        element.click()
        self.driver.close()
        print("done")
    
    @commands.command()
    async def players(self, ctx):
        if not self.is_online():
            embed = discord.Embed(description="The server is offline!", color=0xff0000)
            await ctx.send(embed=embed)
            return
        data = requests.get("https://mcapi.xdefcon.com/server/vismaypikachu2.aternos.me/players/json").json()
        embed = discord.Embed(description=f"There are currently {data['players']} player(s) online.", color=0xdcdcdc)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Minecraft(client))
