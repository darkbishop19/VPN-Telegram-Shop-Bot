import json
import uuid
from datetime import datetime

import requests
import telebot
from boto3.dynamodb.conditions import Key
from telebot import types

import goods_list
import vpn_purchase
from database import database
import config
import text_samples

bot = telebot.TeleBot(token=config.bot_token)


def create_bill(call, user_id, amount, type, operation):
    value = float(amount)
    myuuid = uuid.uuid4()
    unix_time = call.message.date + 3 * 60 * 60
    date = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S+00:00')

    url = f'https://api.qiwi.com/partner/bill/v1/bills/{myuuid}'
    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {config.qiwi_secret_key}',
        'accept': 'application/json',
    }

    data = {
        "amount": {
            "currency": "RUB",
            "value": f'{value}'
        },
        "comment": f"VPN Shop balance: {user_id}",
        "expirationDateTime": date,
        "customFields": {
            "paySourcesFilter": "qw,card",
            "themeCode": "Artem-ChdsBNa2DbK"
        },
    }

    response = requests.put(url=url, headers=headers, json=data)
    bill = response.json()
    url = bill['payUrl']
    begin, invoice_uid = url.split('invoice_uid=')
    pay_url = 'https://artcheroplata.online/qiwi/p2p/' + invoice_uid
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton('Оплатить', url=pay_url)

    if type == 777:
        button2 = types.InlineKeyboardButton(text='Проверить статус платежа', callback_data=f'py_{myuuid}.{user_id}')
        markup.add(button1)
        markup.add(button2)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Платеж на сумму: {amount} рублей\n'
                                   f'После пополнения нажмите на кнопку: "Проверить статус платежа"\n'
                                   f'Если платеж прошел успешно, вам придет сообщение о пополнении баланса',
                              reply_markup=markup)

    else:
        button2 = types.InlineKeyboardButton(text='Проверить статус платежа',
                                             callback_data=f'py,{type}|{operation}_{myuuid}.{user_id}')
        markup.add(button1)
        markup.add(button2)
        match operation:
            case ('buyv'):
                normal_name = goods_list.normal_name_vpn(type)
            case ('buyd'):
                normal_name = goods_list.normal_name_vps(type)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Платеж на сумму:<b> {amount} рублей</b>\n'
                                   f'{normal_name}\n'
                                   f'После оплаты нажмите на кнопку: "Проверить статус платежа"\n'
                                   f'Если платеж прошел успешно, вам придет сообщение о покупке товара',
                              reply_markup=markup, parse_mode='HTML')
    return pay_url


def pay_check(myuuid, id_user, call, type, operation):
    url = f'https://api.qiwi.com/partner/bill/v1/bills/{myuuid}'
    headers = {
        'content-type': 'application/json',
        'authorization': f'Bearer {config.qiwi_secret_key}',
        'accept': 'application/json',
    }
    response = requests.get(url=url, headers=headers)

    item = response.json()
    value = item['amount']['value']
    status = item['status']['value']
    if status == 'PAID':
        response = database.bot_users_table.query(KeyConditionExpression=Key('id_user').eq(id_user))
        last_item = response['Items'][-1]
        balance = last_item['balance']
        new_balance = balance + int(float(value))

        try:
            if last_item['referral'] is not None:
                response4 = database.bot_users_table.query(
                    KeyConditionExpression=Key('id_user').eq(last_item['referral'])
                )
                ref_item = response4['Items'][-1]
                ref_balance = ref_item['balance']
                ref_income = int(float(value) * 0.05)
                new_ref_income = ref_income + ref_item['ref_income']
                new_balance_ref = ref_balance + ref_income
                response3 = database.bot_users_table.update_item(
                    Key={
                        'id_user': last_item['referral'],
                    },
                    UpdateExpression='set balance= :b',
                    ExpressionAttributeValues={
                        ':b': new_balance_ref
                    }
                )
                response5 = database.bot_users_table.update_item(Key={'id_user': last_item['referral']},
                                                                 UpdateExpression="SET ref_income= :b",
                                                                 ExpressionAttributeValues={':b': new_ref_income})
        except:
            True

        response1 = database.bot_users_table.update_item(Key={'id_user': id_user},
                                                         UpdateExpression="SET balance= :b",
                                                         ExpressionAttributeValues={
                                                             ':b': new_balance})  # updated user balance
        response9 = database.profile_users.query(KeyConditionExpression=Key('id_user').eq(id_user))
        item_fput = response9['Items'][-1]

        response10 = database.profile_users.update_item(Key={'id_user': id_user},
                                                        UpdateExpression="SET deposits= :b",
                                                        ExpressionAttributeValues={
                                                            ':b': item_fput['deposits'] + int(float(value))})
        if type == 777:

            bot.edit_message_text(chat_id=int(id_user), message_id=call.message.id,
                                  text=f'Ваш платеж на сумму <b>{int(float(value))}</b> рублей успешно прошел ✅\n'
                                       f'Ваш баланс пополнен ✅.',
                                  parse_mode='HTML', reply_markup='')
            bot.send_message(chat_id=int(id_user), text='Успешный платеж!')
            return
        else:
            vpn_purchase.balance_confirm(user_id=id_user, type=type, call=call, operation=operation)
            return
    if status == 'WAITING':
        bot.send_message(int(id_user), text_samples.payment_waiting)
    if status == 'REJECTED':
        bot.send_message(int(id_user), text_samples.payment_rejected)
    if status == 'EXPIRED':
        bot.send_message(int(id_user), text_samples.payment_expired)
