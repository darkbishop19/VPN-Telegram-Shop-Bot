import uuid
from datetime import datetime

import pay
from database import database
import requests
import telebot
from boto3.dynamodb.conditions import Key
from telebot import types

import config

import goods_list
import text_samples

bot = telebot.TeleBot(token=config.bot_token)


def purchase_check(call, user_id, type, operation):
    match operation:
        case ('buyv'):
            price = goods_list.value_vpn(type)
            normal_name = goods_list.normal_name_vpn(type)
        case ('buyd'):
            price = goods_list.value_vps(type)
            normal_name = goods_list.normal_name_vps(type)
    balance = database.get_balance(user_id)

    if balance < price:
        amount = price - balance
        pay.create_bill(call, user_id, amount, type, operation)
    else:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Подтвердить оплату', callback_data=f'cf,{type}|{operation}_{user_id}')
        markup.add(button1)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'{normal_name}\n'
                                   'Для подтверждения оплаты вашего товара нажмите "Подтвердить оплату"\n'
                                   'Средства спишутся с баланса вашего аккаунта в нашем shop-боте',
                              reply_markup=markup)


def balance_confirm(user_id, type, call, operation):
    match operation:
        case 'buyv':
            good = goods_list.good_vpn(type)
            price = goods_list.value_vpn(type)
        case 'buyd':
            good = goods_list.good_vps(type)
    price = goods_list.value_vps(type)

    response = database.bot_users_table.query(KeyConditionExpression=Key('id_user').eq(user_id))
    last_item = response['Items'][-1]
    balance = last_item['balance']

    new_balance = balance - price
    response1 = database.bot_users_table.update_item(Key={'id_user': user_id},
                                                     UpdateExpression="SET balance= :b",
                                                     ExpressionAttributeValues={
                                                         ':b': new_balance})

    response13 = database.profile_users.query(KeyConditionExpression=Key('id_user').eq(user_id))
    last_prof_item = response13['Items'][-1]
    num_order = last_prof_item['number-orders']
    num_process = last_prof_item['number-process']

    response11 = database.profile_users.update_item(Key={'id_user': user_id},
                                                    UpdateExpression='SET number-process = :p, number-orders = :o',
                                                    ExpressionAttributeValues={':p': num_process + 1,
                                                                               ':o': num_order + 1})
    number_of_orders = database.get_number_of_purchases()
    date = database.get_moscow_time(call.message.date)
    response15 = database.purchase_table.put_item(
        Item={
            'id_user': user_id,
            'number': f'{number_of_orders + 1}',
            'date': date,
            'name': good
        }
    )

    match operation:
        case 'buyv':
            normal_name = goods_list.normal_name_vpn(type)
            instruction = text_samples.vpn_instruction_warning
        case 'buyd':
            normal_name = goods_list.normal_name_vps(type)
            instruction = text_samples.vps_instruction_warning
    bot.edit_message_text(chat_id=int(user_id), message_id=call.message.id, text=f'Поздравляем! Вы приобрели {normal_name}\n'
                                                                                 f'{instruction}',
                          parse_mode='HTML')
    bot.send_message(chat_id=734434528, text=f'{user_id}, {normal_name}')


def get_list_orders(user_id, call):
    try:
        response = database.purchase_table.query(KeyConditionExpression=Key('id_user').eq(user_id))
        last_item = response['Items'][-1]
        i = 1
        order = ''
        for each in response['Items']:
            good, type = each["name"].split(",")
            if each["name"].startswith('vpn'):
                name = goods_list.normal_name_vpn(int(type))
            else:
                name = goods_list.short_name_vps(int(type))

            order += f'📍 {i}: {name}, дата покупки: {each["date"]}\n'
            i += 1
    except:
        order = 'Пока история ваших заказов пуста 🌫'
    markup = types.InlineKeyboardMarkup()
    button_back = types.InlineKeyboardButton('⬅Назад', callback_data=f'mainpr_{user_id}')
    markup.add(button_back)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=order, reply_markup=markup,
                          parse_mode='HTML')
