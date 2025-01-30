
from flask import Flask, render_template, redirect
import requests
import os

app = Flask(__name__)

# Ваш Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7152667196:AAGxc2RtlH9dKc9Q1pg1J1kLU4M-4kS0OUc'
CHAT_ID = '-1001812628545'  # ID Telegram-канала

# Функция для получения изображений из 3 последних постов
def fetch_latest_posts():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatHistory'
    response = requests.get(url, params={'chat_id': CHAT_ID, 'limit': 10}).json()

    print("Telegram API response:", response)  # Логируем ответ
    posts = []

    if response.get("result"):
        messages = response["result"][-3:]  # Берем последние 3 сообщения
        for message in messages:
            if 'photo' in message:
                photos = message['photo']
                largest_photo = photos[-1]  # Самое большое фото
                file_id = largest_photo['file_id']
                message_id = message['message_id']  # ID сообщения

                # Получаем URL файла
                file_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}'
                file_path = requests.get(file_url).json().get('result', {}).get('file_path', '')
                if file_path:
                    full_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'

                    # Создаем ссылку на пост
                    chat_username = 'rndmcIub'  # Username Telegram-канала
                    post_url = f'https://t.me/{chat_username}/{message_id}'

                    posts.append({'image': full_url, 'url': post_url})

    print("Collected posts:", posts)  # Логируем посты
    return posts

# Главная страница
@app.route('/')
def home():
    return redirect('/iframe')

# Рендеринг HTML-страницы
@app.route('/iframe')
def generate_iframe():
    posts = fetch_latest_posts()
    return render_template('iframe.html', posts=posts)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Используем порт 5000 или из окружения
    app.run(host='0.0.0.0', port=port, debug=True)
