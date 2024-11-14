from setup.bdd import creer_tables, remplir_tables
from bot import EdtIUTBot
from dotenv import load_dotenv
import os
load_dotenv()

creer_tables()
remplir_tables()

bot = EdtIUTBot()

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN_DISCORD_BOT"))