
from flask import Flask, render_template, redirect
import requests
import os

app = Flask(__name__)

# Ваш Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7152667196:AAGxc2RtlH9dKc9Q1pg1J1kLU4M-4kS0OUc'

# Функция для получения изображений и текста из Telegram-канала
def fetch_telegram_posts():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    posts = []  # Список для хранения изображений и текста
    response = requests.get(url).json()

    # Логируем ответ от Telegram API
    print("Telegram API response:", response)

    if response.get("result"):
        for update in response["result"]:
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

                    # Извлекаем текст до разделителя "|"
                    text = update['channel_post'].get('text', '')
                    if "|" in text:
                        text = text.split("|")[0].strip()
                    else:
                        text = text.strip()

                    # Сохраняем изображение и текст
                    posts.append({'image': full_url, 'text': text})

                    # Удаляем самую старую запись, если их больше 4
                    if len(posts) > 4:
                        posts.pop(0)

    print("Collected posts:", posts)  # Логируем собранные посты
    return posts

# Главная страница
@app.route('/')
def home():
    return redirect('/iframe')

# Рендеринг HTML-страницы с изображениями и текстом
@app.route('/iframe')
def generate_iframe():
    posts = fetch_telegram_posts()
    return render_template('iframe.html', posts=posts)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Получаем порт из переменной окружения или используем 5000
    app.run(host='0.0.0.0', port=port, debug=True)
