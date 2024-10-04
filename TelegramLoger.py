import logging
from logging.handlers import RotatingFileHandler
import telebot

class TelegramHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.bot = telebot.TeleBot(token)
        self.chat_id = chat_id

    def emit(self, record):
        try:
            log_entry = self.format(record)
            self.bot.send_message(chat_id=self.chat_id, text=log_entry)
        except Exception as e:
            # Handle errors when sending messages to Telegram
            print(f"Failed to send log to Telegram: {e}")

class TelegramLogger:
    def __init__(self, token, target_chat_id, log_file='bot_log.txt'):
        self.bot = telebot.TeleBot(token)
        self.target_chat_id = target_chat_id

        # Set up rotating file handler for logging to a file
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2)  # 5 MB file limit
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

        # Create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

        # Telegram Handler
        telegram_handler = TelegramHandler(token, target_chat_id)
        telegram_handler.setLevel(logging.ERROR)  # Send only error messages to Telegram
        telegram_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

        self.logger.addHandler(telegram_handler)

    def log_info(self, message):
        """Log informational messages."""
        self.logger.info(message)

    def log_error(self, message, user_tag='@BelyiOlexii'):
        """Log error messages with an optional user tag."""
        self.logger.error(f"{user_tag} {message}")

    def log_warning(self, message):
        """Log warning messages."""
        self.logger.warning(message)
