from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from services import get_workers


ASK_DATE_TEXT = "Когда будет мероприятие?"
GET_DATE_TEXT = "Понял, мероприятие будет"

ASK_PLACE_TEXT = "Где будет мероприятие?"
GET_PLACE_TEXT = "Понял, мероприятие будет в:"

ASK_EQUIPMENT_TEXT = "Какое оборудование требуется?"
GET_EQUIPMENT_TEXT = "Понял, нужно:"

ASK_PERSON_TEXT = "Вы бы хотели, чтобы кто сопровождал мероприятие?"
GET_PERSON_TEXT = "Понял, вы хотите чтобы мероприятие сопровождал(а)"


PLACE_KB = InlineKeyboardMarkup([[InlineKeyboardButton(text="Зал", callback_data="Зал")],
                                 [InlineKeyboardButton(text="Двор", callback_data="Двор")],
                                 [InlineKeyboardButton(text="Другое", callback_data="other")]])

workers = [[InlineKeyboardButton(text="Любой", callback_data="Любой")]]
for worker in get_workers():
    workers.append([InlineKeyboardButton(text=worker.name, callback_data=worker.name)])
PERSON_KB = InlineKeyboardMarkup(workers)

