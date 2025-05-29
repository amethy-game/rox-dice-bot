import discord
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Google Sheets API 認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = base64.b64decode(os.getenv("GOOGLE_CREDENTIALS_BASE64")).decode("utf-8")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gc = gspread.authorize(creds)
sheet = gc.open("RoxDiceData").worksheet("RoxDiceData")  

@bot.command()
async def roll(ctx, distance: int, result: int):
    if not (1 <= result <= 6):
        await ctx.send("出目は1〜6の整数でお願いします！")
        return

    now = datetime.utcnow().isoformat()
    user = ctx.author.name
    row = [now, user, distance, result]
    sheet.append_row(row)
    await ctx.send(f"記録しました！距離:{distance}, 出目:{result}")

bot.run(os.getenv("DISCORD_TOKEN"))
