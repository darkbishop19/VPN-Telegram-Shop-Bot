import markups
import text_samples


def value_vpn(type):
    if type == 1:
        return 170
    if type == 2:
        return 500
    if type == 3:
        return 1920
def value_vps(type):
    match type:
        case 1:
            return 160
        case 2:
            return 470
        case 3:
            return 1800
        case 4:
            return 300
        case 5:
            return 840
        case 6:
            return 3500
        case 7:
            return 1200
        case 8:
            return 3400
        case 9:
            return 12000
        case 10:
            return 4000
        case 11:
            return 11000
        case 12:
            return 40000

def type(text):
    if text == 'vpg,1':
        return 1
    if text == 'vpg,3':
        return 2
    if text == 'vpg,12':
        return 3


def good_vpn(number_of_type):
    if number_of_type == 1:
        return 'vpn,1'
    if number_of_type == 2:
        return 'vpn,2'
    if number_of_type == 3:
        return 'vpn,3'

def good_vps(type):
    match type:
        case 1:
            return 'vps,1'
        case 2:
            return 'vps,2'
        case 3:
            return 'vps,3'
        case 4:
            return 'vps,4'
        case 5:
            return 'vps,5'
        case 6:
            return 'vps,6'
        case 7:
            return 'vps,7'
        case 8:
            return 'vps,8'
        case 9:
            return 'vps,9'
        case 10:
            return 'vps,10'
        case 11:
            return 'vps,11'
        case 12:
            return 'vps,12'





def normal_name_vpn(type):
    if type == 1:
        return 'VPN 🇩🇪 Germany 1 месяц\n'
    if type == 2:
        return 'VPN 🇩🇪 Germany 3 месяца\n'
    if type == 3:
        return 'VPN 🇩🇪 Germany 12 месяцев\n'

def normal_name_vps(type):
    match type:
        case 1:
            return text_samples.server_1
        case 2:
            return text_samples.server_2
        case 3:
            return text_samples.server_3
        case 4:
            return text_samples.server_4
        case 5:
            return text_samples.server_5
        case 6:
            return text_samples.server_6
        case 7:
            return text_samples.server_7
        case 8:
            return text_samples.server_8
        case 9:
            return text_samples.server_9
        case 10:
            return text_samples.server_10
        case 11:
            return text_samples.server_11
        case 12:
            return text_samples.server_12
def short_name_vps(type):
    match type:
        case 1:
            return (f'VPN 🇩🇪 Germany 1 месяц\n'
                    f'{text_samples.conf_about_cheapest}')
        case 2:
            return (f'VPN 🇩🇪 Germany 3 месяца\n'
            f'{text_samples.conf_about_cheapest}')
        case 3:
            return (f'VPN 🇩🇪 Germany 1 год\n'
                    f'{text_samples.conf_about_cheapest}')
        case 4:
            return (f'VPN 🇩🇪 Germany 1 месяц\n'
                    f'{text_samples.conf_about_normal}')
        case 5:
            return (f'VPN 🇩🇪 Germany 3 месяца\n'
                    f'{text_samples.conf_about_normal}')
        case 6:
            return (f'VPN 🇩🇪 Germany 1 год\n'
                    f'{text_samples.conf_about_normal}')
        case 7:
            return (f'VPN 🇩🇪 Germany 1 месяц\n'
                    f'{text_samples.conf_about_high}')
        case 8:
            return (f'VPN 🇩🇪 Germany 3 месяца\n'
                    f'{text_samples.conf_about_high}')
        case 9:
            return (f'VPN 🇩🇪 Germany 1 год\n'
                    f'{text_samples.conf_about_high}')
        case 10:
            return (f'VPN 🇩🇪 Germany 1 месяц\n'
                    f'{text_samples.conf_about_golden}')
        case 11:
            return (f'VPN 🇩🇪 Germany 3 месяца\n'
                    f'{text_samples.conf_about_golden}')
        case 12:
            return (f'VPN 🇩🇪 Germany 1 год\n'
                    f'{text_samples.conf_about_golden}')

def get_country_markup(user_id, operation, country_number):
    match operation:
        case 'vpn':
            if country_number == '1':

                markup = markups.german_vpn_prices(user_id)
        case 'vps':
            if country_number == '1':
                markup = markups.german_servers_ops(user_id)

    return markup


def get_name_of_good(operation):
    match operation:
        case 'vpn':
            name = 'vpn'
        case 'vps':
            name = 'vps'

    return name


def get_price_by_server(user_id, type):
    markup = markups.german_vps_prices(user_id, type)

    return markup

def server_prices_callback(type):
    match type:
        case 1:
            list = [1,2,3]
        case 2:
            list = [4,5,6]
        case 3:
            list = [7,8,9]
        case 4:
            list = [10,11,12]
    return list

def server_prices_text_list(type):
    match type:
        case 1:
            list = [text_samples.month_german_cheap_vps, text_samples.three_months_german_cheap_vps, text_samples.year_german_cheap_vps]
        case 2:
            list = [text_samples.month_german_normal_vps, text_samples.three_months_german_normal_vps, text_samples.year_german_normal_vps]
        case 3:
            list = [text_samples.month_german_high_vps, text_samples.three_months_german_high_vps, text_samples.year_german_high_vps]
        case 4:
            list = [text_samples.month_german_golden_vps, text_samples.three_months_german_golden_vps, text_samples.year_german_golden_vps]

    return list