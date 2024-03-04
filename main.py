import requests
import telebot
from http.cookies import SimpleCookie

API_TOKEN = '6930907531:AAF5NHV7TdD-37tU5mhJfbfMt-QLYzqXXk0'

bot = telebot.TeleBot(API_TOKEN)

_headers = {"Referer": f"https://rentry.co/DSLWP/edit", 'User-Agent': 'Mozilla/5.0'}

def main(name:str,title:str,link:str):
    edit_code = 'dsle'
    with requests.Session() as session:
        req = session.get('https://rentry.co/DSLWP/raw', headers=_headers).text
        with open("my.txt", 'w') as file: 
            file.write(req + f"\n{name} | {title} | {link}")

        contents = open("my.txt", 'r').read()
        url = "DSLWP"
        response = session.get("https://rentry.co/")
        cookie = SimpleCookie(response.headers['Set-Cookie'])
        csrftoken = cookie['csrftoken'].value
        payload = {
            'csrfmiddlewaretoken': csrftoken,
            'text': contents,
            'edit_code': edit_code
        }
        res = session.post(f"https://rentry.co/api/edit/{url}", data=payload, headers=_headers)
        print(res.status_code)

@bot.message_handler(commands=['start'])
def send_welcome(message):
  username = message.from_user.username
  
  textw = f"YO! @<b>{username}</b>, I am Alive!, only auth users can use me"
  bot.reply_to(message, textw,parse_mode='HTML')

@bot.message_handler(commands=['up'])
def process_name(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Please enter Name:')
    bot.register_next_step_handler(message, process_title)

def process_title(message):
    chat_id = message.chat.id
    title = message.text
    bot.send_message(chat_id, 'Please enter Title:')
    bot.register_next_step_handler(message, process_link, title)

def process_link(message, title):
    chat_id = message.chat.id
    link = message.text
    bot.send_message(chat_id, 'Please enter Link:')
    bot.register_next_step_handler(message, process_sub, title, link)

def process_sub(message, title, link):
    chat_id = message.chat.id
    sub = message.text
    # Once you have collected all the necessary information, you can call your main function here
    main(title, link, sub)
    bot.send_message(chat_id, 'Your data has been Updated.\n https://rentry.co/DSLWP')

bot.polling()
