import logging

from telegram.ext import ApplicationBuilder

from config import TOKEN
from event import events_application_handler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)-30s[%(lineno)5d] - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


bot = ApplicationBuilder().token(TOKEN).build()
bot.add_handler(events_application_handler)

bot.run_polling()
