from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def phone_button(name):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(name, request_contact=True)
    markup.add(btn)
    return markup


def make_buttons(names: list, row_width: int = 2, lang: str = "uz", back: bool = False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    buttons = []
    for name in names:
        btn = KeyboardButton(name)
        buttons.append(btn)
    markup.add(*buttons)

    if back:
        if lang:
            if lang == "ru":
                text = "⬅️Назад"
            elif lang == "en":
                text = "⬅️Back"
            else:
                text = "⬅️Ortga"
            btn = KeyboardButton(text)
            markup.add(btn)

    return markup


def settings_button(names: list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = []
    for name in names:
        btn = KeyboardButton(name)
        buttons.append(btn)
    markup.add(*buttons)
    return markup