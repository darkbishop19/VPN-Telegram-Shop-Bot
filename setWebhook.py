import requests

import config

url = "https://api.telegram.org/bot{token}/{method}".format(
    token=config.bot_token,
      method="setWebhook"
    #  method="getWebhookinfo"
    #   method="deleteWebhook"
)

data = {"url": config.Function_url}

r = requests.post(url, data=data)
print(r.json())
