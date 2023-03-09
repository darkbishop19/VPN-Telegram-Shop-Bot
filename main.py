import json
import os

from boto3.dynamodb.conditions import Key

import goods_list
import markups
import pay
import text_samples
import vpn_purchase
from database import database
import telebot
import config
from telebot import types

bot = telebot.TeleBot(token=config.bot_token)

def handler(event, context):
    body = json.loads(event['body'])
    update = telebot.types.Update.de_json(body)
    bot.process_new_updates([update])


@bot.message_handler(commands=['start'])
def start(message):
    if check_in_black_list(str(message.from_user.id)) is True:
        return
    markup = show_main_menu(message)
    bot.send_message(message.chat.id, text_samples.hello, reply_markup=markup)

    if message.text != '/start':
        command, referral = message.text.split(' ')
        if referral != message.from_user.id:
            database.add_user_ref(str(message.from_user.id), str(message.from_user.username), message.date,
                                  str(referral))
    else:
        database.add_user_no_ref(str(message.from_user.id), str(message.from_user.username), message.date)

    result = bot.get_chat_member(config.community_id, message.from_user.id)
    if result.status == 'member' or result.status == 'admin' or result.status == 'creator':
        True
    else:
        bot.send_message(message.chat.id, text_samples.subscribe_on_news)


@bot.message_handler(content_types=['text'])
def message(message):
    if message.chat.id == 734434528:
        send_good(message)

    if check_in_black_list(str(message.from_user.id)) is True:
        return
    if message.text == text_samples.about_us:
        bot.send_message(message.chat.id, text_samples.info, parse_mode='HTML')
    if message.text == text_samples.products_about:
        show_good_in_markup(message)
    if message.text == text_samples.main_menu:
        markup = show_main_menu(message)
        bot.send_message(message.chat.id, text_samples.main_menu, reply_markup=markup)
    if message.text == text_samples.support:
        bot.send_message(message.chat.id, text_samples.support_profile)
    if message.text == text_samples.referral_programm:
        bot.send_message(message.chat.id, text_samples.referral_about +
                         f'<b>Ваша ссылка для распространения:</b> <code>https://t.me/VPN_AC_bot?start={message.from_user.id} </code>\n'
                         f'➖➖➖➖➖➖➖➖➖➖\n'
                         f'Ваше количество рефералов:<b>  {database.count_number_referrals(str(message.from_user.id))}\n</b>'
                         f'Ваш заработок на реферальной программе:<b> {database.get_ref_income(str(message.from_user.id))} рублей </b>',
                         parse_mode='HTML')

    if message.text == text_samples.profile:
        show_profile(f'{message.from_user.id}', 1)

    if message.text == text_samples.vpn_good_about:
        bot.send_message(message.chat.id, text_samples.choose_country,
                         reply_markup=show_vpn_goods(message.from_user.id, 1))

    if message.text == text_samples.vps_good_about:
        bot.send_message(message.chat.id, text_samples.choose_server,
                         reply_markup=show_vpn_goods(message.from_user.id, 2))


def show_good_in_markup(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text_samples.vpn_good_about)
    button3 = types.KeyboardButton(text_samples.vps_good_about)
    main_menu_button = types.KeyboardButton(text_samples.main_menu)
    markup.add(button1, button3)
    markup.add(main_menu_button)
    bot.send_message(message.chat.id, 'Выберите заинтересовавший вас товар', reply_markup=markup)


def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(text_samples.about_us)
    button_profile = types.KeyboardButton(text_samples.profile)
    button2 = types.KeyboardButton(text_samples.products_about)
    button3 = types.KeyboardButton(text_samples.referral_programm)
    button_support = types.KeyboardButton(text_samples.support)
    markup.add(button2)
    markup.add(button_profile, button1)
    markup.add(button_support, button3)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def answer(call):

    text, user_id = call.data.split('_')
    if text == 'don':
        show_balance_deposit_menu(call, user_id)
    if text.startswith('r,'):
        method, amount = text.split(',')
        pay.create_bill(call, user_id, amount, 777, 'deposit')
    if text == 'pur':
        vpn_purchase.get_list_orders(user_id, call)


    if text.startswith('py,'):
        myuuid, id_user = user_id.split('.')
        function, type_str = text.split(',')
        type, operation = type_str.split('|')
        pay.pay_check(myuuid, id_user, call, int(type), operation)
    if text == 'mainpr':
        show_profile(user_id, call)
    if text.startswith('servt'):
        operation, country_type = text.split(',')
        mes_text = f'Выберите конфигурацию личного виртуального сервера:'
        markup = goods_list.get_country_markup(user_id,'vps', country_type)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=mes_text,
                              reply_markup=markup)

    if text.startswith('vpn') or text.startswith('vps') or text.startswith('prx'):
        operation, country = text.split(',')
        markup = goods_list.get_country_markup(user_id, operation, country)
        if operation == 'vpn':
            mes_text = f'Выберите на какое время вы хотите приобрести личный {goods_list.get_name_of_good(operation)}:'
        if operation == 'vps':
            mes_text = f'Выберите конфигурацию личного виртуального сервера:'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=mes_text,
                              reply_markup=markup)

    if text.startswith('srv'):
        operation, type = text.split(',')
        markup = goods_list.get_price_by_server(user_id, int(type))
        mes_text = f'Выберите на какое время вы хотите приобрести личный vps:'

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=mes_text,
                              reply_markup=markup)

    if text.startswith('buyv') or text.startswith('buyd'):
        operation, type = text.split(',')
        vpn_purchase.purchase_check(call, user_id, int(type), operation)


    if text.startswith('cf,'):
        order, type_str = text.split(',')
        type, operation = type_str.split('|')

        vpn_purchase.balance_confirm(user_id, int(type), call, operation)

    if text.startswith('flag,'):
        operation, type = text.split(',')
        print(operation)
        print(type)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=text_samples.choose_country,
                              reply_markup=show_vpn_goods(user_id, int(type)))


def check_in_black_list(id_user):
    user_1 = '585863368'
    black_list = [user_1]
    if id_user in black_list:
        bot.send_message(int(id_user), text_samples.ban_message)
        return True
    return False


def show_balance_deposit_menu(call, user_id):
    markup = types.InlineKeyboardMarkup()
    button_50 = types.InlineKeyboardButton('Пополнить на 50 рублей', callback_data=f'r,50_{user_id}')
    button_100 = types.InlineKeyboardButton('Пополнить на 100 рублей', callback_data=f'r,100_{user_id}')
    button_200 = types.InlineKeyboardButton('Пополнить на 200 рублей', callback_data=f'r,200_{user_id}')
    button_300 = types.InlineKeyboardButton('Пополнить на 300 рублей', callback_data=f'r,300_{user_id}')
    button_500 = types.InlineKeyboardButton('Пополнить на 500 рублей', callback_data=f'r,500_{user_id}')
    button_1000 = types.InlineKeyboardButton('Пополнить на 1000 рублей', callback_data=f'r,1000_{user_id}')
    button_5000 = types.InlineKeyboardButton('Пополнить на 5000 рублей', callback_data=f'r,5000_{user_id}')
    button_back = types.InlineKeyboardButton('⬅Назад', callback_data=f'mainpr_{user_id}')
    markup.add(button_50)
    markup.add(button_100)
    markup.add(button_200)
    markup.add(button_300)
    markup.add(button_500)
    markup.add(button_1000)
    markup.add(button_5000)
    markup.add(button_back)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=markup)


def show_vpn_goods(user_id, pick):
    text = ''
    match pick:
        case 1:
            text = 'vpn'
        case 2:
            text = 'vps'

    markup = types.InlineKeyboardMarkup()
    german_button = types.InlineKeyboardButton(text=text_samples.german_vpn,
                                               callback_data=f'{text},1_{user_id}')  # выбор страны впн
    markup.add(german_button)
    return markup


def send_good(message):
    text_mes = message.text
    id, text = text_mes.split('_XTIME_')
    chat_id = int(id)
    response = database.profile_users.query(KeyConditionExpression=Key('id_user').eq(id))
    last_item = response['Items'][-1]
    num_process = last_item['number-process	']
    num_active = last_item['number-active']
    response1 = database.profile_users.update_item(Key={'id_user': id},
                                                   UpdateExpression='SET number-process = :p, number-active = :a',
                                                   ExpressionAttributeValues={':p': num_process - 1,
                                                                              ':a': num_active + 1})
    bot.send_message(chat_id=chat_id, text=text)


def show_profile(user_id, call):
    table = database.profile_users
    response3 = table.query(KeyConditionExpression=Key('id_user').eq(user_id))
    last_item = response3['Items'][-1]
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text_samples.donate_button,
                                         callback_data=f'don_{user_id}')
    button2 = types.InlineKeyboardButton(text_samples.your_purchases,
                                         callback_data=f'pur_{user_id}')
    markup.add(button1)
    markup.add(button2)
    if call == 1:
        bot.send_message(chat_id=int(user_id), text=f'Ваш ID профиля:<b> {user_id}</b>\n'
                                                    f'➖➖➖➖➖➖➖➖➖➖\n'
                                                    f'Ваш баланс:<b> {database.get_balance(user_id)} рублей</b>\n'
                                                    f'Активных заказов:<b> {last_item["number-active"]}</b> \n'
                                                    f'Заказов в обработке:<b> {last_item["number-process"]}</b>\n'
                                                    f'➖➖➖➖➖➖➖➖➖➖\n'
                                                    f'Всего заказов:<b> {last_item["number-orders"]}</b>\n'
                                                    f'Всего пополнений за все время:<b> {last_item["deposits"]} рублей</b>',
                         reply_markup=markup,
                         parse_mode='HTML')
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Ваш ID профиля:<b> {user_id}</b>\n'
                                   f'➖➖➖➖➖➖➖➖➖➖\n'
                                   f'Ваш баланс:<b> {database.get_balance(user_id)} рублей</b>\n'
                                   f'Активных заказов:<b> {last_item["number-active"]}</b> \n'
                                   f'Заказов в обработке:<b> {last_item["number-process"]}</b>\n'
                                   f'➖➖➖➖➖➖➖➖➖➖\n'
                                   f'Всего заказов:<b> {last_item["number-orders"]}</b>\n'
                                   f'Всего пополнений за все время:<b> {last_item["deposits"]} рублей</b>',
                              reply_markup=markup,
                              parse_mode='HTML')


bot.infinity_polling()
