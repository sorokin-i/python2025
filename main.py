import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from config import TOKEN


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)-30s[%(lineno)5d] - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


async def hello(update: Update, context: ContextTypes):
    user = update.effective_user
    log.info(f"hello func called by {user.full_name}")
    await update.message.reply_text(f"Привет, {user.full_name}!")


async def echo(update: Update, context: ContextTypes):
    user = update.effective_user
    log.info(f"echo func called by {user.full_name}")
    await update.message.reply_text(update.message.text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("hello", hello))
app.add_handler(MessageHandler(filters.ALL, echo))

app.run_polling()
