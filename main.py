from data import token
import telebot
import datetime

def telegram_bot(key):
    bot = telebot.TeleBot(key)
    btns_names = ['История', 'Очистить', 'F.A.Q.', 'Text']

    def categories_dict(username, chat_id):
        categories = {}
        try:
            with open(f'/home/megaweb/Desktop/Python_projects/pong/userdata/{username}{chat_id}.txt', 'r',
                      encoding='utf-8') as file:
                for line in file.readlines():
                    categories[line.strip('\n').split(' - ')[0]] = int(line.strip('\n').split(' - ')[1])
            return categories
        except:
            with open(f'/home/megaweb/Desktop/Python_projects/pong/userdata/{username}{chat_id}.txt', 'w',
                      encoding='utf-8') as file:
                return categories

    @bot.message_handler(commands=['start'])
    def start_message(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("История")
        btn2 = telebot.types.KeyboardButton("Очистить")
        btn3 = telebot.types.KeyboardButton("F.A.Q.")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Добро пожаловать!')
        bot.send_message(message.chat.id,
                         'Пишите мне свои траты в формате "Категория - Сумма", и я запишу их.'
                         .format(message.from_user), reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def write_message(message):
        if message.text not in btns_names:
            try:
                s = message.text.lower().split(' - ')
                int(s[1]) + 1
            except BaseException :
                print(message.chat.username, message.chat.id, datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), sep='\n', end='\n')
                bot.send_message(message.chat.id, 'Неверный формат данных')
                bot.send_message(message.chat.id,
                                 'Пишите мне свои траты в формате "Категория - Сумма(целое число)", и я запишу их.')
            else:
                categories = categories_dict(message.chat.username, message.chat.id)
                if s[0].strip() not in categories:
                    categories[s[0].lower().strip()] = int(s[1].strip())
                else:
                    categories[s[0].lower().strip()] += int(s[1].strip())
                with open(
                        f'/home/megaweb/Desktop/Python_projects/pong/userdata/{message.chat.username}{message.chat.id}.txt',
                        'w', encoding='utf-8') as file:
                    for i in categories:
                        file.writelines(f'{i} - {categories[i]}\n')
                bot.send_message(message.chat.id,
                                 f'Записал!\nДля вывода информации о ваших тратах, нажмите кнопку "История"'
                                 )
        elif message.text == 'История':
            categories = categories_dict(message.chat.username, message.chat.id)

            history = ''
            count = 0
            for item in categories:
                history += f'{item.title()} - {categories[item]}руб\n'
                count += int(categories[item])
            if history != '':
                history += f'\nВсего: {count}'
                bot.send_message(message.chat.id, history)
            else:
                bot.send_message(message.chat.id, 'Вы пока что ничего не записывали.')

        elif message.text == 'Очистить':
            with open(f'/home/megaweb/Desktop/Python_projects/pong/userdata/{message.chat.username}{message.chat.id}.txt', 'w', encoding='utf-8') as file:
                file.write('')
                bot.send_message(message.chat.id, 'Готово!')
        elif message.text == 'F.A.Q.':
            bot.send_message(message.chat.id, 'Функционал в разработке.')
        elif message.text == 'Text':
            bot.send_message(message.chat.id, 'Хацкеры не пройдут!!1!')

    while True:
        try:
            bot.polling()
        except Exception('Что-то не так..Перезагружусь пожалуй)') as error:
            print(datetime.datetime.now().strftime('%d-%m-%Y %H:%M'), error)

            continue
    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
