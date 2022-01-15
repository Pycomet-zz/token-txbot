import logging
import os
import re
from flask import Flask, request
from datetime import date
import telegram
import telebot
from telebot import types
import goslate
from dotenv import load_dotenv
load_dotenv()

from models import User

user = User
LANGUAGE = user.language

# # Language setup
# os.environ["LANGUAGE"] = "en"
# LANGUAGE = os.getenv("LANGUAGE")
translator = goslate.Goslate()

# Logging Setup
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.WARNING
)

TOKEN = os.getenv('TOKEN')

DEBUG = True
SERVER_URL = os.getenv("SERVER_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
