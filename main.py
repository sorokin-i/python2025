import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

from config import TOKEN
from event import events_application_handler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)-30s[%(lineno)5d] - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


async def hello(update: Update, context: ContextTypes):
    user = update.effective_user
    log.info(f"hello func called by {user}")
    await update.message.reply_text(str(update.effective_chat.id))

async def help(update: Update, context: ContextTypes):
    user = update.effective_user
    log.info(f"help func called by {user}")
    text = "\n".join([
        "Привет! Я школьный бот. Я умею выполнять следующие команды:",
        "/start /help - Пришлю все доступные команды",
        "/hello - Поздороваюсь с тобой",
        "/show_keyboard - Пришлю клавиатуру",
    ])
    await update.message.reply_text(text)

async def show_keyboard(update: Update, context: ContextTypes):
    user = update.effective_user
    log.info(f"help func called by {user}")
    text = "Нажми на кнопку!"
    buttons = [[InlineKeyboardButton(text="1", callback_data="one"), InlineKeyboardButton(text="2", callback_data="two")],
               [InlineKeyboardButton(text="3", callback_data="three"), InlineKeyboardButton(text="4", callback_data="four")],
               [InlineKeyboardButton(text="5", callback_data="five"), InlineKeyboardButton(text="6", callback_data="six")]]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(text, reply_markup=keyboard)

bot = ApplicationBuilder().token(TOKEN).build()
bot.add_handler(CommandHandler(["start", "help"], help))
bot.add_handler(CommandHandler("hello", hello))
bot.add_handler(CommandHandler("show_keyboard", show_keyboard))
bot.add_handler(events_application_handler)

bot.run_polling()
