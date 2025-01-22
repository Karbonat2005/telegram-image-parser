
from flask import Flask, render_template, redirect
import requests
import os

app = Flask(__name__)

# Ваш Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7152667196:AAGxc2RtlH9dKc9Q1pg1J1kLU4M-4kS0OUc'

# Функция для получения изображений и ссылок на посты Telegram
def fetch_latest_posts():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    response = requests.get(url).json()

    print("Telegram API response:", response)  # Логируем ответ от Telegram API
    posts = []  # Список для хранения картинок, текста и ссылок

    if response.get("result"):
        updates = response["result"][-3:]  # Берем последние 3 обновления
        for update in updates:
            if 'channel_post' in update and 'photo' in update['channel_post']:
                photos = update['channel_post']['photo']
                largest_photo = photos[-1]  # Берём самое большое фото
                file_id = largest_photo['file_id']
                message_id = update['channel_post']['message_id']  # ID сообщения

                # Получаем URL файла
                file_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}'
                file_path = requests.get(file_url).json().get('result', {}).get('file_path', '')
                if file_path:
                    full_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'

                    # Создаем ссылку на оригинальный пост
                    chat_username = 'rndmcIub'  # Укажите username вашего Telegram-канала
                    post_url = f'https://t.me/{chat_username}/{message_id}'

                    # Добавляем пост с картинкой и ссылкой
                    posts.append({'image': full_url, 'text': '', 'url': post_url})

    print("Collected posts with links:", posts)  # Логируем собранные посты
    return posts

# Главная страница
@app.route('/')
def home():
    return redirect('/iframe')

# Рендеринг HTML-страницы с изображениями
@app.route('/iframe')
def generate_iframe():
    posts = fetch_latest_posts()
    return render_template('iframe.html', posts=posts)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Получаем порт из переменной окружения или используем 5000
    app.run(host='0.0.0.0', port=port, debug=True)
