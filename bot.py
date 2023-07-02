import telebot
from configs import val, TOKEN
from extensions import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def hello(message: telebot.types.Message):
    text = 'Для начала работы введите данные в формате: \n <Выбранная валюта>, ' \
           '<Валюта, в которую необходимо перевести>. ' \
           'Чтобы увидеть инструкцию еще раз, воспользуйтесь командами /start или /help. ' \
           'Ознакомиться с доступными валютами можно по команде /values.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values', ])
def get_val(message: telebot.types.Message):
    text = 'Доступные валюты для работы:'
    for key in val:
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 2:
            raise APIException('Слишком много значений.'
                                'Чтобы узнать правила пользования ботом, воспользуйтесь командой /help')
        quote, base = values
        total_base = CryptoConverter.get_price(quote, base)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
      bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:

        text = f'Цена валюты {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
