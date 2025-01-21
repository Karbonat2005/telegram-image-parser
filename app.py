
from flask import Flask, render_template, redirect
import requests
import os

app = Flask(__name__)

# Ваш Telegram Bot Token
TELEGRAM_BOT_TOKEN = '7152667196:AAGxc2RtlH9dKc9Q1pg1J1kLU4M-4kS0OUc'

# Переменная для хранения сообщений в памяти
stored_posts = []  # Глобальный список для сохранения всех сообщений

# Функция для получения изображений и текста из Telegram-канала
def fetch_telegram_posts():
    global stored_posts  # Используем глобальную переменную для сохранения старых постов
    chat_id = '@rndmcIub'  # Укажите username вашего Telegram-канала
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatHistory'
    posts = stored_posts.copy()  # Создаём копию текущего состояния

    response = requests.get(url, params={'chat_id': chat_id, 'limit': 10}).json()
    print("Telegram API response:", response)  # Логируем ответ от Telegram API

    if response.get("result"):
        for message in response["result"]:
            # Проверяем наличие фото в сообщении
            if 'photo' in message:
                photos = message['photo']
                largest_photo = photos[-1]  # Берём самое большое фото
                file_id = largest_photo['file_id']

                # Получаем URL файла
                file_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getFile?file_id={file_id}'
                file_path = requests.get(file_url).json().get('result', {}).get('file_path', '')
                if file_path:
                    full_url = f'https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file_path}'

                    # Проверяем, есть ли это изображение уже в списке
                    if not any(post['image'] == full_url for post in posts):
                        posts.append({'image': full_url, 'text': ''})  # Текст можно дополнить

                        # Удаляем самое старое сообщение, если их больше 4
                        if len(posts) > 4:
                            posts.pop(0)

    stored_posts = posts  # Сохраняем обновлённый список
    print("Updated stored posts:", stored_posts)  # Логируем итоговый список постов
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
