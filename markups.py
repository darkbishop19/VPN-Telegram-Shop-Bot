from telebot import types

import goods_list
import text_samples


def german_vpn_prices(user_id):
    markup = types.InlineKeyboardMarkup()
    month_button = types.InlineKeyboardButton(text=text_samples.month_german_vpn,
                                              callback_data=f'buyv,1_{user_id}')  # germany
    three_month_button = types.InlineKeyboardButton(text=text_samples.three_months_german_vpn,
                                                    callback_data=f'buyv,2_{user_id}')
    year_button = types.InlineKeyboardButton(text=text_samples.year_german_vpn, callback_data=f'buyv,3_{user_id}')
    back_button = types.InlineKeyboardButton(text = text_samples.back_text, callback_data=f'flag,1_{user_id}')
    markup.add(month_button)
    markup.add(three_month_button)
    markup.add(year_button)
    markup.add(back_button)
    return markup


def german_vps_prices(user_id, type):
    list = goods_list.server_prices_callback(type)
    month_1 = list[0]
    month_3 = list[1]
    month_12 = list[2]
    text_list = goods_list.server_prices_text_list(type)
    text_month_1 = text_list[0]
    text_month_3 = text_list[1]
    text_month_12 = text_list[2]
    markup = types.InlineKeyboardMarkup()
    month_button = types.InlineKeyboardButton(text=text_month_1,
                                              callback_data=f'buyd,{month_1}_{user_id}')  # germany
    three_month_button = types.InlineKeyboardButton(text=text_month_3,
                                                    callback_data=f'buyd,{month_3}_{user_id}')
    year_button = types.InlineKeyboardButton(text=text_month_12, callback_data=f'buyd,{month_12}_{user_id}')
    back = types.InlineKeyboardButton(text = text_samples.back_text, callback_data= f'servt,1_{user_id}')
    markup.add(month_button)
    markup.add(three_month_button)
    markup.add(year_button)
    markup.add(back)
    return markup

def german_servers_ops(user_id):
    markup = types.InlineKeyboardMarkup()
    cheap = types.InlineKeyboardButton(text=text_samples.conf_about_cheapest,
                                              callback_data=f'srv,1_{user_id}')  # germany
    normal = types.InlineKeyboardButton(text=text_samples.conf_about_normal,
                                                    callback_data=f'srv,2_{user_id}')
    high = types.InlineKeyboardButton(text=text_samples.conf_about_high, callback_data=f'srv,3_{user_id}')
    golden = types.InlineKeyboardButton(text=text_samples.conf_about_golden, callback_data=f'srv,4_{user_id}')
    back = types.InlineKeyboardButton(text = text_samples.back_text, callback_data=f'flag,2_{user_id}')
    markup.add(cheap)
    markup.add(normal)
    markup.add(high)
    markup.add(golden)
    markup.add(back)
    return markup

