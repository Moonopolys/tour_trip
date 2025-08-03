from telebot.types import CallbackQuery, Message
from data.loader import bot, db
from config import TEXTS
from keyboards.default import phone_button, make_buttons
from keyboards.inline import travels_buttons, travel_pagination_buttons

REGISTER = {}


@bot.callback_query_handler(func=lambda call: call.data in ["uz", "ru", "en"])
def reaction_to_lang(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = call.data
    db.update_lang(lang, from_user_id)
    bot.delete_message(chat_id, call.message.message_id)
    if None in db.get_user(from_user_id):
        text = TEXTS[lang][1]
        msg = bot.send_message(chat_id, text)
        bot.register_next_step_handler(msg, get_name)
    else:
        text_buttons = TEXTS[lang][101]
        text = TEXTS[lang][5]
        bot.send_message(chat_id, text, reply_markup=make_buttons(text_buttons))


def get_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    text = TEXTS[lang][1]
    if message.text:
        REGISTER[from_user_id] = {
            "full_name": message.text
        }
        msg = bot.send_message(chat_id, TEXTS[lang][2], reply_markup=phone_button(TEXTS[lang][100]))
        bot.register_next_step_handler(msg, get_phone)
    else:
        msg = bot.send_message(chat_id, text)
        bot.register_next_step_handler(msg, get_name)


def get_phone(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    lang = db.get_lang(from_user_id)
    if message.contact:
        phone_number = message.contact.phone_number
        full_name = REGISTER[from_user_id]["full_name"]
        db.save_phone_number_and_full_name(full_name, phone_number, from_user_id)
        names_buttons = TEXTS[lang][101]
        bot.send_message(chat_id, TEXTS[lang][4], reply_markup=make_buttons(names_buttons))

    else:
        msg = bot.send_message(chat_id, TEXTS[lang][2], reply_markup=phone_button(TEXTS[lang][1]))
        bot.register_next_step_handler(msg, get_phone)

@bot.callback_query_handler(func=lambda call: "travel_" in call.data)
def reaction_to_travel_(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.get_lang(from_user_id)
    travel_id = int(call.data.split("_")[-1])
    bot.delete_message(chat_id, call.message.message_id)
    image, markup = travel_pagination_buttons(travel_id)
    bot.send_photo(chat_id, image, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: "next_image_" in call.data)
def reaction_to_next_image(call: CallbackQuery):
    chat_id = call.message.chat.id
    travel_id = int(call.data.split("_")[-1])
    buttons = call.message.reply_markup.keyboard[0]
    for button in buttons:
        if button.callback_data == "current_page":
            page = int(button.text.split("/")[0])

    bot.delete_message(chat_id, call.message.message_id)
    image, markup = travel_pagination_buttons(travel_id, page+1)
    bot.send_photo(chat_id, image, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: "prev_image_" in call.data)
def reaction_to_prev_image(call: CallbackQuery):
    chat_id = call.message.chat.id
    travel_id = int(call.data.split("_")[-1])
    buttons = call.message.reply_markup.keyboard[0]
    for button in buttons:
        if button.callback_data == "current_page":
            page = int(button.text.split("/")[0])

    bot.delete_message(chat_id, call.message.message_id)
    image, markup = travel_pagination_buttons(travel_id, page-1)
    bot.send_photo(chat_id, image, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: "info_" in call.data)
def reaction_to_prev_image(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    lang = db.get_lang(from_user_id)
    bot.delete_message(chat_id, call.message.message_id)
    travel_id = int(call.data.split("_")[-1])
    name, price, days = db.select_travel_text(travel_id, lang)
    text = f'''
<b>Nomi:</b> {name},
<b>Narxi:</b> {price} so'm,
<b>Davomiyligi:</b> {days} kun.
    '''
    buttons = call.message.reply_markup.keyboard[0]
    for button in buttons:
        if button.callback_data == "current_page":
            page = int(button.text.split("/")[0])

    image, markup = travel_pagination_buttons(travel_id, page)
    bot.send_photo(chat_id, image, caption=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: "back_to_" in call.data)
def reaction_to_prev_image(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    from_user_id = call.from_user.id
    lang = db.get_lang(from_user_id)
    travels_list = db.view_travels(lang)
    bot.send_message(chat_id, "---------------------------------------",
                     reply_markup=travels_buttons(travels_list))