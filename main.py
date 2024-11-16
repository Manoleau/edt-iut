from bot import EdtIUTBot
from dotenv import load_dotenv
import services.media as media_service
from models.logger import Logger
import os
import logging
load_dotenv()

media_service.creer_dossier("logs")
logging.basicConfig(filename='logs/log.log', level=logging.INFO)
logger = Logger("main")
logger.ecrire_info('Projet démarré')


bot = EdtIUTBot()
bot.run(os.getenv("TOKEN_DISCORD_BOT"))