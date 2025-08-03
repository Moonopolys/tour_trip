from pyexpat.errors import messages
from telebot.types import Message, ReplyKeyboardRemove

from data.loader import bot, db
from keyboards.default import make_buttons
from config import ADMINS, TEXTS

admin_buttons_name = [
        "➕ Sayohatlar qo'shihs",
        "➕ Mashhur joylar qo'shihs",
        "➕ Ekskursiya jadvali qo'shish",
        "➕ Yaqin joylar qo'shish",
    ]

TRAVEL = {}

@bot.message_handler(func=lambda message: message.text == "️👮‍♂️Admin buyruqlari")
def reaction_to_admin_commands(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "️👮‍♂️Admin buyruqlari",
                         reply_markup=make_buttons(admin_buttons_name, back=True))


@bot.message_handler(func=lambda message: message.text == "➕ Sayohatlar qo'shihs")
def reaction_to_admin_commands(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Sayohat nomini o'zbek tilida kiriting:",
                               reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_name_uz_travel)

def get_name_uz_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id] = {
        "name_uz": message.text
    }
    msg = bot.send_message(chat_id, "Sayohat nomini rus tilida kiriting:")
    bot.register_next_step_handler(msg, get_name_ru_travel)

def get_name_ru_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]["name_ru"] = message.text
    msg = bot.send_message(chat_id, "Sayohat nomini ingiliz tilida kiriting:")
    bot.register_next_step_handler(msg, get_name_en_travel)


def get_name_en_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]["name_en"] = message.text
    msg = bot.send_message(chat_id, "Sayoxat narxini kiriting:")
    bot.register_next_step_handler(msg, get_name_price)


def get_name_price(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]["price"] = message.text
    msg = bot.send_message(chat_id, "Sayoxat davomiligini(kun) kiriting")
    bot.register_next_step_handler(msg, get_name_days)


def get_name_days(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    TRAVEL[from_user_id]['days'] = message.text
    msg = bot.send_message(chat_id, "Sayohat rasmini linkini jonating:")
    bot.register_next_step_handler(msg, get_image_travel)


def get_image_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if not TRAVEL[from_user_id].get("images"):
        TRAVEL[from_user_id]['images'] = [message.text]
    else:
        TRAVEL[from_user_id]['images'].append(message.text)
    msg = bot.send_message(chat_id, "yana rasm qo'shasizmi?", reply_markup=make_buttons(["Yes", "No"]))
    bot.register_next_step_handler(msg, save_travel)


def save_travel(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.text == "No":
        name_uz = TRAVEL[from_user_id]["name_uz"]
        name_ru = TRAVEL[from_user_id]["name_ru"]
        name_en = TRAVEL[from_user_id]["name_en"]
        price = int(TRAVEL[from_user_id]["price"])
        days = int(TRAVEL[from_user_id]['days'])
        images = TRAVEL[from_user_id]['images']
        travel_id = db.insert_travel(name_uz, name_ru, name_en, price, days)
        del TRAVEL[from_user_id]
        for image in images:
            db.insert_image(image, travel_id)
        bot.send_message(chat_id, "Sayoxat saqlandi!",
                         reply_markup=make_buttons(admin_buttons_name, back=True))
    else:
        msg = bot.send_message(chat_id, "Sayohat rasmini linkini jonating:",
                               reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_image_travel)


@bot.message_handler(func=lambda message: message.text == "⬅️Ortga")
def reaction_to_back(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    btn_names = TEXTS[lang][101]
    text = TEXTS[lang][4]
    bot.send_message(chat_id, text, reply_markup=make_buttons(btn_names))