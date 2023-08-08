import unittest
from unittest import mock
import requests
from Health_check import parse_json
import json
from dotenv import load_dotenv
import os
load_dotenv()

API_TOKEN = os.environ.get('API_KEY')
CHAT_ID = os.environ.get('CHAT_ID')
URL = os.environ.get('URL')


class MyFileTest(unittest.TestCase):

    @mock.patch('requests.get')
    def test_successful_json_parsing(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key1': 'working', 'key2': 'working'}
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(os.environ.get('URL'), verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json={'chat_id': CHAT_ID, 'text': 'Success'},
                verify=False
            )

    @mock.patch('requests.get')
    def test_empty_json_data(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json={
                    'chat_id': CHAT_ID,
                    'text': 'Пустые данные JSON. Нет данных для отправки в Telegram.'
                },
                verify=False
            )

    @mock.patch('requests.get')
    def test_json_parsing_error(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Expecting property name enclosed in double quotes",
                                                              '{"key1": "working"}', 0)
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json=mock.ANY,  # Проверяем, что передан любой JSON-объект
                verify=False
            )


    @mock.patch('requests.get')
    def test_send_to_telegram_success(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key1": "working"}
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json={'chat_id': CHAT_ID, 'text': 'Success'},
                verify=False
            )

    @mock.patch('requests.get')
    def test_send_to_telegram_empty_data(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json={'chat_id': CHAT_ID, 'text': 'Пустые данные JSON. Нет данных для отправки в Telegram.'},
                verify=False
            )

    @mock.patch('requests.get')
    def test_send_to_telegram_error_status(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json={'chat_id': CHAT_ID, 'text': 'Ошибка при получении данных. Код состояния: 500'},
                verify=False
            )

    @mock.patch('requests.get')
    def test_send_to_telegram_request_error(self, mock_get):
        mock_get.side_effect = requests.RequestException("Request Error")

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json={'chat_id': CHAT_ID, 'text': 'Ошибка при получении данных: Request Error'},
                verify=False
            )

    @mock.patch('requests.get')
    def test_send_error_to_telegram_request_error(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key1": "error"}
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            mock_post.side_effect = requests.RequestException("Request Error")

            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_has_calls([
                mock.call(
                    f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                    json={'chat_id': CHAT_ID, 'text': 'Ошибка в key1: error'},
                    verify=False
                ),
                mock.call(
                    f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                    json={'chat_id': CHAT_ID, 'text': 'Ошибка при отправке в Telegram: Request Error'},
                    verify=False
                )
            ])

    @mock.patch('requests.get')
    def test_send_to_telegram_remove_error(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key1": "working", "key2": "working"}
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json={'chat_id': CHAT_ID, 'text': 'Success'},
                verify=False
            )

    @mock.patch('requests.get')
    def test_send_to_telegram_empty_json_data(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json={'chat_id': CHAT_ID, 'text': 'Пустые данные JSON. Нет данных для отправки в Telegram.'},
                verify=False
            )

    @mock.patch('requests.get')
    def test_parse_json_invalid_response_status(self, mock_get):
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with mock.patch('requests.post') as mock_post:
            parse_json()

            mock_get.assert_called_once_with(URL, verify=False)
            mock_post.assert_called_once_with(
                f'https://api.telegram.org/bot{API_TOKEN}/sendMessage',
                json={'chat_id': CHAT_ID, 'text': 'Ошибка при получении данных. Код состояния: 404'},
                verify=False
            )


if __name__ == '__main__':
    unittest.main()
