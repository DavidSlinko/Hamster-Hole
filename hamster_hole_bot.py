import telebot
import requests
from telebot import types

API_TOKEN = '6421365318:AAEUxW8vh3r-s8FgZXkiFwCC8iy0MVRoYoA'  # Замените на ваш токен от BotFather
API_BASE_URL = 'http://127.0.0.1:8000/api/'  # URL вашего API

bot = telebot.TeleBot(API_TOKEN)

# Ссылка на канал для подписки
CHANNEL_LINK = "t.me/mkperevod"

# Словарь для хранения данных о состоянии пользователя
user_data = {}

# Хэндлер для команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_subscribe = types.KeyboardButton("Подписаться на канал")
    btn_search = types.KeyboardButton("Поиск инструкций")
    markup.add(btn_subscribe, btn_search)

    welcome_text = (
        "Привет! Добро пожаловать в нашего бота.\n"
        f"Для продолжения подпишитесь на наш канал: {CHANNEL_LINK}\n"
        "Нажмите на кнопку ниже, чтобы перейти к подписке или для поиска инструкций."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


# Хэндлер для кнопки "Поиск инструкций"
@bot.message_handler(func=lambda message: message.text == "Поиск инструкций")
def search_instructions(message):
    response = requests.get(f"{API_BASE_URL}categories/")
    if response.status_code == 200:
        categories = response.json()

        # Создаем клавиатуру с категориями
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in categories:
            markup.add(types.KeyboardButton(category['name']))
        markup.add(types.KeyboardButton("Назад"))

        bot.send_message(message.chat.id, "Выберите категорию для поиска инструкций:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Ошибка при получении категорий.")


# Хэндлер для выбора категории
@bot.message_handler(func=lambda message: message.text in [cat['name'] for cat in requests.get(f"{API_BASE_URL}categories/").json()])
def handle_category_selection(message):
    category_name = message.text
    user_data[message.chat.id] = {"category": category_name}  # Сохраняем выбранную категорию

    # Запрос на получение букв для выбранной категории
    response = requests.get(f"{API_BASE_URL}letters/")
    if response.status_code == 200:
        letters = response.json()

        # Создаем клавиатуру с буквами
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for letter in letters:
            markup.add(types.KeyboardButton(letter['symbol']))
        markup.add(types.KeyboardButton("Назад"))

        bot.send_message(message.chat.id, f"Выберите букву для поиска авторов в категории {category_name}:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Ошибка при получении букв.")


# Хэндлер для выбора буквы
@bot.message_handler(func=lambda message: len(message.text) == 1)  # Предполагаем, что буква это один символ
def handle_letter_selection(message):
    selected_letter = message.text

    # Получаем сохраненную категорию
    category_name = user_data.get(message.chat.id, {}).get("category")

    if not category_name:
        bot.send_message(message.chat.id, "Ошибка: категория не выбрана.")
        return

    # Запрос на получение авторов по категории и букве
    response = requests.get(f"{API_BASE_URL}authors/", params={"category": category_name, "letter": selected_letter})
    if response.status_code == 200:
        authors = response.json()

        if authors:
            # Создаем клавиатуру с авторами
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for author in authors:
                markup.add(types.KeyboardButton(author['name']))
            markup.add(types.KeyboardButton("Назад"))

            bot.send_message(message.chat.id, f"Авторы в категории '{category_name}' на букву '{selected_letter}':", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Нет авторов, соответствующих вашему запросу.")
    else:
        bot.send_message(message.chat.id, "Ошибка при получении авторов.")


@bot.message_handler(
    func=lambda message: message.text in [author['name'] for author in requests.get(f"{API_BASE_URL}authors/").json()])
def handle_author_selection(message):
    author_name = message.text

    # Запрос на получение инструкций для выбранного автора
    response = requests.get(f"{API_BASE_URL}authors/", params={"name": author_name})
    if response.status_code == 200:
        author = response.json()

        if author:
            # Запрос на получение инструкций для данного автора
            author_id = author[0]['id']
            response_instructions = requests.get(f"{API_BASE_URL}instructions/", params={"author": author_id})
            if response_instructions.status_code == 200:
                instructions = response_instructions.json()

                if instructions:
                    for instruction in instructions:
                        image_url = instruction.get('image')
                        file_url = instruction.get('file')
                        description = instruction['description']

                        # Отправляем изображение или ссылку на изображение
                        if image_url:
                            try:
                                bot.send_photo(message.chat.id, image_url, caption=f"Описание: {description}")
                            except Exception as e:
                                bot.send_message(message.chat.id, f"Ошибка при отправке изображения: {e}")

                        # Отправляем файл, если он есть
                        if file_url:
                            try:
                                bot.send_document(message.chat.id, file_url)
                            except Exception as e:
                                bot.send_message(message.chat.id, f"Ошибка при отправке файла: {e}")
                else:
                    bot.send_message(message.chat.id, "Нет инструкций для этого автора.")
            else:
                bot.send_message(message.chat.id, "Ошибка при получении инструкций.")
        else:
            bot.send_message(message.chat.id, "Ошибка: автор не найден.")
    else:
        bot.send_message(message.chat.id, "Ошибка при получении автора.")


# Хэндлер для кнопки "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def go_back(message):
    # Возвращаемся к главному меню
    send_welcome(message)


# Запуск бота
bot.polling(none_stop=True)