from config import *

@bot.message_handler(commands=['start'])
def startbot(msg):
    # import pdb; pdb.set_trace()
    user.id = msg.from_user.id
    "Ignites the bot application to take action"

    bot.reply_to(
        msg,
        "Welcome To Token Transaction Update Bot, Your Bot Session Is Live And Running"
    )

