import telebot
import requests
import jsons
from Class_ModelResponse import ModelResponse

# Замените 'YOUR_BOT_TOKEN' на ваш токен от BotFather
API_TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)
context = {}

# Команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Я ваш Telegram бот.\n"
        "Доступные команды:\n"
        "/start - вывод всех доступных команд\n"
        "/model - выводит название используемой языковой модели\n"
        "/clear - очистить контекст\n"
        "Отправьте любое сообщение, и я отвечу с помощью LLM модели."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['clear'])
def clear_context(message):
    user_id = message.from_user.id
    context[user_id] = []
    bot.reply_to(message, "Контекст очищен.")

@bot.message_handler(commands=['context'])
def print_context(message):
    user_id = message.from_user.id
    if user_id in context and context[user_id]:
        bot.reply_to(message, " ".join(context[user_id]))
    else:
        bot.reply_to(message, "Контекст пуст.")



@bot.message_handler(commands=['model'])
def send_model_name(message):
    # Отправляем запрос к LM Studio для получения информации о модели
    response = requests.get('http://localhost:1234/v1/models')

    if response.status_code == 200:
        model_info = response.json()
        model_name = model_info['data'][0]['id']
        bot.reply_to(message, f"Используемая модель: {model_name}")
    else:
        bot.reply_to(message, 'Не удалось получить информацию о модели.')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text
    user_id = message.from_user.id
    if user_id not in context:
        context[user_id] = []

    context[user_id].append(f"user: {user_query}\n")

    if context:
        user_query = " ".join(context[user_id])

    request = {
        "messages": [
          {
            "role": "user",
            "content": user_query
          },
    ]
  }
    response = requests.post(
        'http://localhost:1234/v1/chat/completions',
        json=request
    )

    if response.status_code == 200:
        model_response :ModelResponse = jsons.loads(response.text, ModelResponse)
        context[user_id].append(f"assistant: {model_response.choices[0].message.content}\n")
        bot.reply_to(message, model_response.choices[0].message.content)
    else:
        bot.reply_to(message, 'Произошла ошибка при обращении к модели.')


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
