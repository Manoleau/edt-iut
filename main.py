from bot import EdtIUTBot
from dotenv import load_dotenv
import os
load_dotenv()

bot = EdtIUTBot()

bot.run(os.getenv("TOKEN_DISCORD_BOT"))