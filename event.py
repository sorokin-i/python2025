import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

from config import TOKEN


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)-30s[%(lineno)5d] - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

WAIT_FOR_DATE, WAIT_FOR_PLACE, WAIT_FOR_EQUIPMENT, WAIT_FOR_PERSON = range(4)

async def ask_date(update: Update, context: ContextTypes) -> int:
    log.info(f"ask_date is triggered by {update.effective_user}")
    text = "Когда будет мероприятие?"
    await update.message.reply_text(text)
    return WAIT_FOR_DATE

async def get_date(update: Update, context: ContextTypes):
    log.info(f"get_date is triggered by {update.effective_user}")
    text = f"Понял, мероприятие будет {update.message.text}"
    await update.message.edit_text(text)
    return await ask_place(update, context)

async def ask_place(update: Update, context: ContextTypes):
    log.info(f"ask_place is triggered by {update.effective_user}")
    text = "Где будет мероприятие?"
    await update.message.edit_text(text)
    return WAIT_FOR_PLACE

async def get_place(update: Update, context: ContextTypes):
    ...

async def ask_equipment(update: Update, context: ContextTypes):
    log.info(f"ask_equipment is triggered by {update.effective_user}")
    text = "Какое оборудование нужно?"
    await update.message.edit_text(text)
    return WAIT_FOR_EQUIPMENT

async def get_equipment(update: Update, context: ContextTypes):
    ...

async def ask_person(update: Update, context: ContextTypes):
    log.info(f"ask_person is triggered by {update.effective_user}")
    text = "Кого бы вы хотели видеть?"
    await update.message.edit_text(text)
    return WAIT_FOR_PERSON

async def get_person(update: Update, context: ContextTypes):
    ...

#async def verify_data(update: Update, context: ContextTypes):
#    log.info(f"ask_date is triggered by {update.effective_user}")

async def register_application(update: Update, context: ContextTypes):
    log.info(f"register_application is triggered by {update.effective_user}")

    return ConversationHandler.END


events_application_handler = ConversationHandler(
    entry_points=[CommandHandler("event", ask_date)],
    states={
        WAIT_FOR_DATE: [],
        WAIT_FOR_PLACE: []
    },
    fallbacks=[]
)

