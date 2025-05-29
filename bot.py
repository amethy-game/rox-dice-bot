import discord
import os
import gspread
import json
import base64
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

# 苦肉の策（ポートを開いておかないと落ちる）
def keep_alive():
    def run():
        server = HTTPServer(("0.0.0.0", 8080), SimpleHTTPRequestHandler)
        server.serve_forever()
    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()

intents = discord.Intents.default()
intents.message_content = True
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

keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
