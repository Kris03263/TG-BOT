import telebot
import random
from telebot  import types
import json

bot_token = '6363163497:AAFMqaqmqTfhaR4NtAgxuB6hmDIBcWaaizQ'
bot = telebot.TeleBot(bot_token)
keyboard = types.InlineKeyboardMarkup()
callbackList = []


@bot.message_handler(commands=['hello'])
def returnHelloForUser(message):
    bot.reply_to(message , 'Hello!')

@bot.message_handler(commands=["addFood"])
def addFood(message):
    a = message.text.split()
    input = a[1]
    with open("TelegramBot\someFoods.json","r",encoding='utf-8') as f:
        data = json.load(f)
        for i in data["food"]:
            if i == input:
                bot.reply_to(message,"有相同資料!")
                return
        data["food"].append(str(input))  
    with open("TelegramBot\someFoods.json","w",encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False,indent=4)
    bot.reply_to(message,str(input) + " Load already!")

@bot.message_handler(commands=['deleteFood'])
def deleteFood(message):
    a = message.text.split()
    input = a[1]
    info = False
    with open("TelegramBot\someFoods.json","r",encoding='utf-8') as f:
        data = json.load(f)
        for i in data["food"]:
            if i == input:
                data["food"].remove(input)
                with open("TelegramBot\someFoods.json","w",encoding='utf-8') as g:
                    json.dump(data, g, ensure_ascii=False,indent=4)
                    info = True
                break
        if info:
            bot.reply_to(message,input + " have deleted already!")
        else:
            bot.reply_to(message,"No data!")

@bot.message_handler(commands=["randomFood"])
def randomFood(message):
    with open("TelegramBot\someFoods.json","r",encoding='utf-8') as f:
        data = json.load(f)
        a = random.randint(0,len(data["food"])-1)
        choose = data["food"][a]
        bot.reply_to(message,"今天吃 " + choose + " 啦!" )
            

@bot.message_handler(commands=["listFood"])
def getAllFood(message):
    with open("TelegramBot\someFoods.json","r",encoding='utf-8') as f:
        data = json.load(f)
    a = ''
    for i in data["food"]:
        food = types.InlineKeyboardButton(str(i),callback_data=str(i))
        keyboard.add(food)
        callbackList.append(i)
        a = a+i + " "
    bot.send_message(message.chat.id,"choose your food",reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: call.data in callbackList)
def callback_handler(call):

    cid = call.message.chat.id
    mid = call.message.message_id
    answer = call.data
    try:
        bot.reply_to(call.message,"HI")
        bot.edit_message_text("You voted: " + answer, cid, mid, reply_markup=keyboard)
    except:
        pass
    
@bot.message_handler(func=lambda msg: True)
def echoMessage(message):
    bot.reply_to(message,message.text)

bot.infinity_polling()