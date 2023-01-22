import logging
from datetime import datetime, timedelta
from subprocess import Popen

from environs import Env
from telegram import TelegramError, Update
from telegram.ext import Updater, CommandHandler, CallbackContext


def change_host(update: Update, context: CallbackContext) -> None:
    """Run another script."""

    previous_changed_at = context.bot_data.get('changed_at')
    now = datetime.now()
    if previous_changed_at and now - previous_changed_at < timedelta(seconds=10):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Почему так часто меняешь?',
        )
        return None
    context.bot_data['changed_at'] = now
    logging.info(f'changed_at: {now}, starting process')
    process = Popen(
        ['/usr/bin/python3', '/root/host_picker/host_picker.py'],
    )
    logging.info(f'Subprocess exit code: {process.returncode}')


def main() -> None:
    """Configures and launches the bot."""
    logging.basicConfig(
        format='%(asctime)s %(message)s',
        filename='/root/host_picker/logs_changer.txt',
        level=logging.DEBUG,
    )
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    chat_id = env('GROUP_CHAT_ID')
    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('change', change_host))

    while True:
        try:
            logging.info('Бот запускается.')
            updater.start_polling()
            updater.idle()
        except TelegramError:
            logging.exception('А у бота ошибка!')


if __name__ == '__main__':
    main()
