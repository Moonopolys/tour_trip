from telebot import TeleBot

from config import TOKEN
from database.dbase import Database

bot = TeleBot(TOKEN)
db = Database()