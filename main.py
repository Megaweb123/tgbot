import requests
import telebot
from auth_data import token
from bs4 import BeautifulSoup
from datetime import datetime


def telegram_bot(key):
    bot = telebot.TeleBot(key)
    questions = ['кто пидор?', 'кто пидор ?', 'кто пидр?', 'кто пидр ?', 'кто пидор', 'кто пидр']
    questions2 = ['почему я пидор?', 'почему я?', 'почему я пидор ?', 'почему я ?']
    questions3 = ['может не я?']

    def pre_pars(message, url):
        bot.send_message(message.chat.id, 'Секунду, ищу информацию...')
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        return soup

    def logs(data, id_chat):
        with open('logs.txt', 'a', encoding='utf-8') as file:
            file.write(f'{id_chat}:{data}\n')

    @bot.message_handler(commands=['start'])
    def start_message(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("/крипта")
        btn2 = telebot.types.KeyboardButton("/валюта")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Добро пожаловать!')
        bot.send_message(message.chat.id, 'Нажми "/крипта" чтобы узнать курс BTC, BNB и EFM.\nИли "/валюта", чтобы узнать курс USD, EUR, GPB и UAH.'.format(message.from_user), reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def send_message(message):
        if message.text.lower() == '/крипта':
            soup = pre_pars(message, 'https://billium.com/ru/?utm_source=yandex&utm_medium=cpc&utm_campaign=yd_concurent_poisk_rf_79375165&utm_term=---autotargeting&utm_content=id%7C41908294590_41908294590%7Ccid%7C79375165%7Cgid%7C5049300042%7Caid%7C12882571906_12882571906%7Cadp%7Cno%7Cpos%7Cpremium2%7Csrc%7Csearch_none%7Cdvc%7Cdesktop%7Cgeo%7C%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0_213&_openstat=ZGlyZWN0LnlhbmRleC5ydTs3OTM3NTE2NTsxMjg4MjU3MTkwNjt5YW5kZXgucnU6cHJlbWl1bQ&yclid=12145745733291606015')
            data = soup.find_all('div', class_="currency-quotes-row d-flex align-items-center", limit=3)
            items = []
            for item in data:
                name = item.find('div', class_="currency-quotes-name").text.strip()
                price = item.find('span', class_="field-last-price").text.strip()
                last_24h = item.find('div',
                                     class_="currency-quotes-field currency-quotes-field-last-24h currency-quotes-field-mh").text.strip()
                items.append(f'{name}: {price}$ ({last_24h})')
            bot.send_message(message.chat.id, f'{str(datetime.now())[:-10]}\n{items[0]}\n{items[1]}\n{items[2]}')
            logs(message.text, message.chat.id)
        elif message.text.lower() == '/валюта':
            items = []
            soup = pre_pars(message, 'https://finance.rambler.ru/currencies/')
            countries = ['Доллар США', 'Евро', 'Фунт стерлингов', 'Украинских гривен']
            for i in countries:
                data = soup.find('a', class_="finance-currency-table__tr", title=i)
                price = data.find('div',
                                  class_="finance-currency-table__cell finance-currency-table__cell--value").text.strip()
                change = [x for x in data.find_all('div')[-1]][0].strip()
                if i != 'Украинских гривен':
                    items.append(f'{i}: {price[:5]}₽ ({change})')
                else:
                    items.append(f'10 {i}: {price[:5]}₽ ({change})')
            bot.send_message(message.chat.id, f'{str(datetime.now())[:-10]}\n{items[0]}\n{items[1]}\n{items[2]}\n{items[3]}')
            logs(message.text, message.chat.id)
        elif message.text.lower() in questions:
            bot.send_message(message.chat.id, 'Ты. Весь в отца...')
        elif message.text.lower() in questions2:
            bot.send_message(message.chat.id, 'Так сложилось.')
        elif message.text.lower() in questions3:
            bot.send_message(message.chat.id, 'Хотелось бы усомниться, но не выходит.')
        elif 'пидор' in message.text.lower():
            bot.send_message(message.chat.id, 'Я подумаю над вашем сообщением.')
            with open('pidor.txt', 'a', encoding='utf-8') as file:
                file.write(message.text.lower() + '\n')

    while True:
        try:
            bot.polling()
        except BaseException('Что-то не так..Перезагружусь пожалуй)'):
            continue

    bot.polling()
