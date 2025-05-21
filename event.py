import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ParseMode

from config import GROUP_ID
from services import get_workers
from ui import *


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)-30s[%(lineno)5d] - %(message)s"
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


WAIT_FOR_DATE, WAIT_FOR_PLACE, WAIT_FOR_EQUIPMENT, WAIT_FOR_PERSON = range(4)

async def ask_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f"ask_date is triggered by {update.effective_user}")
    await update.message.reply_text(ASK_DATE_TEXT)
    return WAIT_FOR_DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(f"get_date is triggered by {update.effective_user}")
    day = update.message.text
    context.user_data["day"] = day
    text = f"{GET_DATE_TEXT} {day}"
    await update.message.reply_text(text)
    return await ask_place(update, context)

async def ask_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f"ask_place is triggered by {update.effective_user}")
    await update.message.reply_text(ASK_PLACE_TEXT, reply_markup=PLACE_KB)
    return WAIT_FOR_PLACE

async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(f"get_place is triggered by {update.effective_user}")
    place = update.callback_query.data
    #if place == "other":
        #place = get_another_place(update, context)
    context.user_data["place"] = place
    text = f"{GET_PLACE_TEXT} {place}"
    await context.bot.send_message(chat_id=update.effective_user.id, text=text)
    return await ask_equipment(update, context)

#async def get_another_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #await context.bot.send_message(chat_id=update.effective_user.id, text=GET_ANOTHER_PLACE_TEXT)


async def ask_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f"ask_equipment is triggered by {update.effective_user}")
    await context.bot.send_message(chat_id=update.effective_user.id, text=ASK_EQUIPMENT_TEXT)
    return WAIT_FOR_EQUIPMENT

async def get_equipment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(f"get_equipment is triggered by {update.effective_user}")
    equipment = update.message.text
    context.user_data["equipment"] = equipment
    text = f"{GET_EQUIPMENT_TEXT} {equipment}"
    await update.message.reply_text(text)
    return await ask_person(update, context)

async def ask_person(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.info(f"ask_person is triggered by {update.effective_user}")
    await update.message.reply_text(ASK_PERSON_TEXT, reply_markup=PERSON_KB)
    return WAIT_FOR_PERSON

async def get_person(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(f"get_person is triggered by {update.effective_user}")
    person = update.callback_query.data
    context.user_data["person"] = person
    text = f"{GET_PERSON_TEXT} {person}"
    await context.bot.send_message(chat_id=update.effective_user.id, text=text)
    return await register_application(update, context)

#async def verify_data(update: Update, context: ContextTypes):
#    log.info(f"ask_date is triggered by {update.effective_user}")

async def register_application(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log.info(f"register_application is triggered by {update.effective_user}")
    USER_APPLICATION_TEXT = [f"Заявка принята!",
                             f"Скоро с вами свяжутся.\n",
                             f"Ваши данные:",
                             f"Дата: {context.user_data['day']}",
                             f"Место: {context.user_data['place']}",
                             f"Оборудование: {context.user_data['equipment']}",
                             f"Работник: {context.user_data['person']}\n"]

    GROUP_APPLICATION_TEXT = [f"Новая заявка!\n",
                              f"Дата: {context.user_data['day']}",
                              f"Место: {context.user_data['place']}",
                              f"Оборудование: {context.user_data['equipment']}",
                              f"Работник: {context.user_data['person']}\n"]
    await context.bot.send_message(chat_id=update.effective_user.id, text="\n".join(USER_APPLICATION_TEXT))
    await context.bot.send_message(chat_id=GROUP_ID, text="\n".join(GROUP_APPLICATION_TEXT))
    context.user_data.clear()
    return ConversationHandler.END


events_application_handler = ConversationHandler(
    entry_points=[CommandHandler("event", ask_date)],
    states={
        WAIT_FOR_DATE: [MessageHandler(filters.TEXT, get_date)],
        WAIT_FOR_PLACE: [CallbackQueryHandler(get_place)],
        WAIT_FOR_EQUIPMENT: [MessageHandler(filters.TEXT, get_equipment)],
        WAIT_FOR_PERSON: [CallbackQueryHandler(get_person)]
    },
    fallbacks=[]
)

