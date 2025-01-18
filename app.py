
from flask import Flask, render_template, redirect
import requests
import os

app = Flask(__name__)

# Ваш Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7152667196:AAGxc2RtlH9dKc9Q1pg1J1kLU4M-4kS0OUc'

# Функция для получения изображений из Telegram-канала
def fetch_telegram_posts():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates'
    response = requests.get(url).json()

    # Логируем весь ответ от Telegram
    print("Telegram API response:", response)

    images = []
    if response.get("result"):
        for update in response["result"]:
            print("Processing update:", update)  # Логируем каждое сообщение
            if 'message' in update and 'photo' in update['message']:
                photo = update['message']['photo'][-1]  # Берём самое большое фото
                file_id = photo['file_id']

                # Получаем URL файла
                file_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}'
                file_path = requests.get(file_url).json().get('result', {}).get('file_path', '')
                if file_path:
                    full_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'
                    images.append(full_url)

            if len(images) >= 5:  # Ограничиваемся 5 изображениями
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

@app.route('/debug')
def debug():
    response = fetch_telegram_posts()
    return f"Response: {response}"
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Получаем порт из переменной окружения или используем 5000
    app.run(host='0.0.0.0', port=port, debug=True)
