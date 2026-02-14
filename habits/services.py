import requests
from config import settings


def send_telegram_message(chat_id, message):
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)
