from config import *


def start_menu(msg):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    
    a = types.KeyboardButton(translator.translate("I Am A Passenger?", LANGUAGE))
    b = types.KeyboardButton(translator.translate("I Am A Bus Operator?", LANGUAGE))
    c = types.KeyboardButton(translator.translate("Referral Link", LANGUAGE))
    d = types.KeyboardButton(translator.translate("About Us", LANGUAGE))
    e = types.KeyboardButton(translator.translate("Rules & Regulations", LANGUAGE))
    f = types.KeyboardButton("Language Switcher")
    g = types.KeyboardButton("Contact Us")

    keyboard.add(a,b,c,d,e,f,g)
    return keyboard
 

@bot.message_handler(commands=['start'])
def startbot(msg):
    # import pdb; pdb.set_trace()
    user.id = msg.from_user.id
    "Ignites the bot application to take action"

    bot.reply_to(
        msg,
        translator.translate("Welcome, This Bot allows you to reserve , book or buy long distance city Bus Tickets in Ethiopia and make payments using your TeleBirr, HelloCash , Mobile Banking, or Bank Deposit through any bank in your area and many more.", LANGUAGE),
        reply_markup=start_menu(msg)
    )

    

@bot.message_handler(regexp="^Back")
def startbotn(msg):
    startbot(msg)


