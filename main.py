import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

from config import TOKEN


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)-30s[%(lineno)5d] - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


async def hello(update: Update, context: ContextTypes):
    user = update.effective_user
    log.info(f"hello func called by {user}")
    await update.message.reply_text(f"<b>Привет,</b> {user.full_name}!", parse_mode=ParseMode.HTML)

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
    buttons = []
    keyboard = InlineKeyboardMarkup([InlineKeyboardButton("OooooO")])
    await update.message.reply_text(text, reply_markup=keyboard)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler(["start", "help"], help))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("show_keyboard", show_keyboard))

app.run_polling()
