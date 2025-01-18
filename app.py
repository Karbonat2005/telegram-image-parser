
from flask import Flask, render_template, redirect
import requests
import os

app = Flask(__name__)

# Ваш Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7152667196:AAGxc2RtlH9dKc9Q1pg1J1kLU4M-4kS0OUc'

# Функция для получения изображений из Telegram-канала
def fetch_telegram_posts():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    images = []
    offset = None

    while True:
        # Добавляем offset для получения всех сообщений
        params = {'offset': offset} if offset else {}
        response = requests.get(url, params=params).json()

        if not response.get("result"):
            break  # Если нет новых сообщений, выходим

        for update in response["result"]:
            offset = update["update_id"] + 1  # Обновляем offset для следующего запроса

            # Проверяем наличие фото в сообщении
            if 'channel_post' in update and 'photo' in update['channel_post']:
                photos = update['channel_post']['photo']
                largest_photo = photos[-1]  # Берём самое большое фото
                file_id = largest_photo['file_id']

                # Получаем URL файла
                file_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}'
                file_path = requests.get(file_url).json().get('result', {}).get('file_path', '')
                if file_path:
                    full_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'
                    images.append(full_url)

            if len(images) >= 4:  # Ограничиваемся 5 изображениями
                break

        if len(images) >= 4:
            break

    print("Collected images:", images)  # Логируем собранные URL изображений
    return images

# Главная страница
@app.route('/')
def home():
    return redirect('/iframe')

# Рендеринг HTML-страницы с изображениями
@app.route('/iframe')
def generate_iframe():
    images = fetch_telegram_posts()
    return render_template('iframe.html', images=images)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Получаем порт из переменной окружения или используем 5000
    app.run(host='0.0.0.0', port=port, debug=True)
