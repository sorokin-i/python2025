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
place_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Зал", callback_data="hall"), InlineKeyboardButton(text="Двор", callback_data="yard")]])

async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f"ask_date is triggered by {update.effective_user}")
    text = "Когда будет мероприятие?"
    await update.message.reply_text(text)
    return WAIT_FOR_DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(f"get_date is triggered by {update.effective_user}")
    day = update.message.text
    context.user_data["day"] = day
    text = f"Понял, мероприятие будет {day}"
    await update.message.reply_text(text)
    return await ask_place(update, context)

async def ask_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f"ask_place is triggered by {update.effective_user}")
    text = "Где будет мероприятие?"
    await update.message.reply_text(text, reply_markup=place_keyboard)
    return WAIT_FOR_PLACE

async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(f"get_place is triggered by {update.effective_user}")
    place = update.callback_query.data
    context.user_data["place"] = place
    text = f"Понял, мероприятие будет в {place}"
    await update.message.reply_text(text)
    return await ask_equipment(update, context)

async def ask_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f"ask_equipment is triggered by {update.effective_user}")
    text = "Какое оборудование требуется?"
    await update.message.reply_text(text)
    return WAIT_FOR_EQUIPMENT

async def get_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(f"get_equipment is triggered by {update.effective_user}")
    equipment = update.message.text
    context.user_data["equipment"] = equipment
    text = f"Понял, нужно {equipment}"
    await update.message.reply_text(text)
    return await ask_person(update, context)

async def ask_person(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f"ask_person is triggered by {update.effective_user}")
    text = "Кого бы вы хотели видеть?"
    await update.message.reply_text(text)
    return WAIT_FOR_PERSON

async def get_person(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(f"get_person is triggered by {update.effective_user}")
    person = update.message.text
    context.user_data["person"] = person
    text = f"Понял, вы хотите чтобы мероприятие сопровождал(а) {person}"
    await update.message.reply_text(text)
    return await register_application(update, context)

#async def verify_data(update: Update, context: ContextTypes):
#    log.info(f"ask_date is triggered by {update.effective_user}")

async def register_application(update: Update, context: ContextTypes):
    log.info(f"register_application is triggered by {update.effective_user}")
    #await bot.send_message()
    context.user_data.clear()
    return ConversationHandler.END


events_application_handler = ConversationHandler(
    entry_points=[CommandHandler("event", ask_date)],
    states={
        WAIT_FOR_DATE: [MessageHandler(filters.TEXT, get_date)],
        WAIT_FOR_PLACE: [CallbackQueryHandler(get_place)],
        WAIT_FOR_EQUIPMENT: [MessageHandler(filters.TEXT, get_equipment)],
        WAIT_FOR_PERSON: [MessageHandler(filters.TEXT, get_person)]
    },
    fallbacks=[]
)

