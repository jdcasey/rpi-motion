
from os.path import (join, exists)
from telegram import Bot
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def send(cfg, img):
    imagefile = join(cfg.image_dir, img)
    if not exists(imagefile):
        logger.warning("Image does not exist: {imagefile}".format(imagefile=imagefile))
    elif not cfg.send_to_chats or len(cfg.send_to_chats) < 1:
        logger.warning("No chats configured for send: '{cfg.send_to_chats}'".format(cfg=cfg))
    else:
        bot = Bot(cfg.token)
        for c in cfg.send_to_chats:
            print("Sending: {imagefile} to chat: {c}".format(imagefile=imagefile, c=c))
            with open(imagefile, 'rb') as f:
                bot.send_photo(c, f)
