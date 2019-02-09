
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    RegexHandler,
    Filters
)

import logging
from os.path import (join, exists, isdir)
from os import listdir
import rpi_motion.snapshot as snap

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SELECT_DATE, SELECT_TIME = range(2)

def error(bot, update, error):
    logger.warning("Update %s caused error '%s'", update, error)

def chatinfo(bot, update):
    msg = "User: {update.effective_user.full_name} is in chat: {update.message.chat_id}".format(update=update)
    print(msg)
    update.message.reply_text(msg)

def snapshot(bot, update, cfg):
    try:
        result = snap.take_snapshot(cfg)
        if result is True:
            update.message.reply_text("Snapshot is on its way!")
        else:
            update.message.reply_text("Cannot take snapshot!")
    except Exception as e:
        logger.warning("Failed to take snapshot: {e}".format(e=e))
        update.message.reply_text("Something went wrong. Cannot take snapshot")

def list_all(bot, update, args, user_data, cfg):
    try:
        if len(args) < 1:
            files = listdir(cfg.image_dir) if isdir(cfg.image_dir) else []
            if len(files) < 1:
                update.message.reply_text("No image directories found!")
                return ConversationHandler.END

            dirs = []
            for f in files:
                dirs.append([f])

            bot.send_message(
                update.message.chat_id,
                "Select a date:",
                reply_markup=ReplyKeyboardMarkup(keyboard=dirs, one_time_keyboard=True))

            return SELECT_DATE
        else:
            dirname = args[0]
            user_data['dirname'] = dirname

            if len(args) > 1:
                tstamp = args[1]
                user_data['tstamp'] = tstamp
                return show_time(bot, update, user_data, cfg)
            else:
                return list_date(bot, update, user_data, cfg)
    except Exception as e:
        logger.warning("Failed to list image dates: {e}".format(e=e))
        update.message.reply_text("Something went wrong. Cannot list image dates.")

    return ConversationHandler.END


def list_date(bot, update, user_data, cfg):
    try:
        dirs = []
        dirname = user_data.get('dirname')
        if not dirname:
            dirname = update.message.text
            if dirname:
                user_data['dirname'] = dirname
            else:
                return ConversationHandler.END

        dirpath = join(cfg.image_dir, dirname)
        files = listdir(dirpath) if isdir(dirpath) else []
        if len(files) < 1:
            update.message.reply_text("No images found for {dirname}".format(dirname=dirname))
            return ConversationHandler.END

        for f in files:
            dirs.append([f])

        bot.send_message(
            update.message.chat_id,
            "Select an image:",
            reply_markup=ReplyKeyboardMarkup(keyboard=dirs, one_time_keyboard=True))

        return SELECT_TIME
    except Exception as e:
        logger.warning("Failed to list images: {e}".format(e=e))
        update.message.reply_text("Something went wrong. Cannot list images.")

    return ConversationHandler.END

def show_time(bot, update, user_data, cfg):
    try:
        tstamp = user_data.get('tstamp')
        if not tstamp:
            tstamp = update.message.text
            if tstamp:
                user_data['tstamp'] = tstamp
            else:
                print("No timestamp selected")
                return ConversationHandler.END

        if tstamp:
            dirname = user_data['dirname']
            basepath = join(cfg.image_dir, dirname, tstamp)
            pic = None
            for f in [basepath, basepath + ".jpg", basepath + ".png"]:
                print("{f} exists? {exists}".format(f=f, exists=exists(f)))
                if exists(f):
                    pic = f
                    break

            if not pic:
                update.message.reply_text("No such timestamp image!")
                return ConversationHandler.END

            with open(pic, 'rb') as f:
                bot.send_photo(update.message.chat_id, f)
        else:
            print("No photo selected.")
    except Exception as e:
        logger.warning("Failed to select image: {e}".format(e))
        update.message.reply_text("Something went wrong. Cannot select image.")

    return ConversationHandler.END

def done(bot, update):
    print("END")
    update.message.reply_text("DONE")
    return ConversationHandler.END

def setup(updater, cfg):
    dispatcher = updater.dispatcher
    dispatcher.add_error_handler(error)

    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler('list',
                                        lambda bot, update, args, user_data: list_all(bot, update, args, user_data, cfg),
                                        pass_args=True, pass_user_data=True)],

            states={
                SELECT_DATE: [MessageHandler(Filters.text,
                                             lambda bot, update, user_data: list_date(bot, update, user_data, cfg),
                                             pass_user_data=True)],
                SELECT_TIME: [MessageHandler(Filters.text,
                                             lambda bot, update, user_data: show_time(bot, update, user_data, cfg),
                                             pass_user_data=True)]
            },

            fallbacks=[RegexHandler('^Cancel$', done)]

        )
    )

    dispatcher.add_handler(
        CommandHandler('snapshot', lambda bot, update: snapshot(bot, update, cfg))
    )
    dispatcher.add_handler(
        CommandHandler('chatinfo', chatinfo)
    )

def listen(cfg, user_sig_handler=None):
    updater = Updater(cfg.token, user_sig_handler=user_sig_handler)
    setup(updater, cfg)

    updater.start_polling()
    updater.idle()

