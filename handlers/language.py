from config import *

def menu5():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    a = types.InlineKeyboardButton(text="English - EN", callback_data="en")
    b = types.InlineKeyboardButton(text=translator.translate("Amharic - AM", "am"), callback_data="am")
    keyboard.add(a,b)
    return keyboard


@bot.message_handler(regexp="^Language")
def startRef(msg):
    bot.reply_to(
        msg,
        translator.translate("<b>Pick Your Preferred Language ?</b>", LANGUAGE),
        parse_mode=telegram.ParseMode.HTML,
        reply_markup=menu5()
    )




# Callback Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_answer(call):
    """
    Button Response
    """

    if call.data == "en":
        user.language = "en"

    elif call.data == "am":
        user.language = "am"

    else:
        pass