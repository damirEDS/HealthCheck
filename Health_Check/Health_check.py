import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.environ.get('URL')
API_TOKEN = os.environ.get('API_KEY')
CHAT_ID = os.environ.get('CHAT_ID')
API_URL = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'


def parse_json():
    try:
        # Отправка GET-запроса к сайту для получения данных в формате JSON
        response = requests.get(URL, verify=False)
        # Проверка статуса ответа
        if response.status_code == 200:
            # Получение данных в формате JSON
            try:
                health_check_data = response.json()
                if health_check_data:
                    send_to_telegram(health_check_data)
                else:
                    send_error_to_telegram("Пустые данные JSON. Нет данных для отправки в Telegram.")
            except json.JSONDecodeError as e:
                error_message = f"Ошибка при разборе JSON: {str(e)}"
                send_error_to_telegram(error_message)
        else:
            error_message = f"Ошибка при получении данных. Код состояния: {response.status_code}"
            send_error_to_telegram(error_message)
    except requests.RequestException as e:
        error_message = f"Ошибка при получении данных: {str(e)}"
        send_error_to_telegram(error_message)


def send_to_telegram(health_check_data):
    try:
        error_messages = {}

        for key, value in health_check_data.items():
            if value != "working":
                error_message = f"Ошибка в {key}: {value}"
                if error_message not in error_messages:
                    response = requests.post(API_URL, json={'chat_id': CHAT_ID, 'text': error_message}, verify=False)
                    print(response.text)
                    error_messages[error_message] = True
            else:
                error_message = f"Ошибка в {key}: {value}"
                if error_message in error_messages:
                    del error_messages[error_message]

    except Exception as e:
        error_message = f"Ошибка при отправке в Telegram: {str(e)}"
        send_error_to_telegram(error_message)


def send_error_to_telegram(error_message):
    try:
        requests.post(API_URL, json={'chat_id': CHAT_ID, 'text': error_message}, verify=False)
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {str(e)}")


if __name__ == "__main__":
    parse_json()
