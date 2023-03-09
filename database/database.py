from datetime import datetime

import boto3
import telebot
from boto3.dynamodb.conditions import Key, Attr

import config
import text_samples

bot = telebot.TeleBot(token=config.bot_token)

telegram_db = boto3.resource(
    'dynamodb',
    endpoint_url=config.USER_STORAGE_URL,
    region_name='ru-central1',
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
)

bot_users_table = telegram_db.Table('bot-users')
profile_users = telegram_db.Table('user-profile')
purchase_table = telegram_db.Table('purchase-table')

# response = purchase_table.query(KeyConditionExpression=Key('id_user').eq('5858633688')&Key('number').eq('2'))
# print(response['Items'][-1])

# response1 = bot_users_table.update_item(Key={'id_user': '5858633688'},
#                                         UpdateExpression='SET  balance = :a',
#                                         ExpressionAttributeValues={':a': 159  })


def add_user_no_ref(id_user, username, unix_date):
    try:
        response3 = bot_users_table.query(KeyConditionExpression=Key('id_user').eq(id_user))
        item = response3['Items'][-1]

    except:
        add_profile(id_user)
        unix_time = unix_date + 3 * 60 * 60
        date = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

        response2 = bot_users_table.put_item(
            Item={
                'id_user': id_user,
                'username': username,
                'join_date': date,
                'balance': 0,
                'ref_income': 0
            }
        )


def add_user_ref(id_user, username, unix_date, referral):
    try:
        response3 = bot_users_table.query(KeyConditionExpression=Key('id_user').eq(id_user))
        item = response3['Items'][-1]
        bot.send_message(int(id_user), text_samples.registered_with_ref)
    except:
        add_profile(id_user)
        unix_time = unix_date + 3 * 60 * 60
        date = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

        response2 = bot_users_table.put_item(
            Item={
                'id_user': id_user,
                'username': username,
                'join_date': date,
                'balance': 5,
                'referral': referral,
                'ref_income': 0
            }
        )


def add_profile(id_user):
    response = profile_users.put_item(
        Item={
            'id_user': id_user,
            'deposits': 0,
            'number-active': 0,
            'number-orders': 0,
            'number-process': 0
        }

    )


def get_balance(id_user):
    response = bot_users_table.query(KeyConditionExpression=Key('id_user').eq(id_user))
    last_item = response['Items'][-1]
    return last_item['balance']


def count_number_referrals(id_user):
    scan = bot_users_table.scan(
        FilterExpression=Attr('referral').eq(id_user)
    )
    return scan['Count']


def get_ref_income(id_user):
    response = bot_users_table.query(KeyConditionExpression=Key('id_user').eq(id_user))
    last_item = response['Items'][-1]

    return last_item['ref_income']


def get_number_of_purchases():
    try:
        response = purchase_table.scan()
        last_item = response['Items'][-1]
        number_of_orders = int(last_item['number'])
        return number_of_orders
    except:
        return 0


def get_moscow_time(unix_date):
    unix_time = unix_date + 3 * 60 * 60
    date = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
    return date
