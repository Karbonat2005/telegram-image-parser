
from flask import Flask, render_template
import requests

app = Flask(__name__)

# Ваш Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7152667196:AAGxc2RtlH9dKc9Q1pg1J1kLU4M-4kS0OUc'

# Функция для получения изображений из Telegram-канала
def fetch_telegram_posts():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    response = requests.get(url).json()
    images = []

    if response.get("result"):
        for update in response["result"]:
            # Проверяем наличие фото в сообщении
            if 'message' in update and 'photo' in update['message']:
                photo = update['message']['photo'][-1]  # Берём самое большое фото
                file_id = photo['file_id']

                # Получаем URL файла
                file_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}'
                file_path = requests.get(file_url).json()['result']['file_path']
                full_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'
                images.append(full_url)
            if len(images) >= 5:  # Ограничиваемся 5 изображениями
                break
    return images

# Рендеринг HTML-страницы с изображениями
@app.route('/iframe')
def generate_iframe():
    images = fetch_telegram_posts()
    return render_template('iframe.html', images=images)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Получаем порт из переменной окружения или используем 5000
    app.run(host='0.0.0.0', port=port, debug=True)
