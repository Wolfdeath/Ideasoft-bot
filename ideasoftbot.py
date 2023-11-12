import telebot
from telebot import types
import daemon
import time

bot = telebot.TeleBot('6957477344:AAHpeVkBCRPWPn1Z46Us6E2FCU8FhA8Iv00')

# Список вопросов
questions = [
    "Знаете ли Вы, что ожидает от Вас работодатель?",
    "Имеете ли Вы необходимые материалы и инструменты для надлежащего выполнения своей работы?",
    "Имеете ли Вы возможность ежедневно делать на своей работе то, что Вы делаете лучше всего?",
    "Получали ли Вы за последние семь дней одобрение или похвалу за хорошо выполненную работу?",
    "Относится ли Ваш непосредственный руководитель или кто-либо другой на работе к Вам как к личности?",
    "Кто-нибудь на Вашей работе способствует Вашему профессиональному развитию?",
    "Принимается ли во внимание Ваша точка зрения?",
    "Вызывают ли у Вас миссия и стратегия вашей компании чувство значимости выполняемой Вами работы?",
    "Считают ли Ваши коллеги своим долгом качественное выполнение работы?",
    "Есть ли у Вас на работе настоящий друг?",
    "За последние полгода говорил ли кто-нибудь с Вами на работе о Ваших профессиональных успехах и достижениях?",
    "За последний год были ли у Вас на работе возможности для приобретения новых знаний и профессионального роста?"
]

# Словарь для хранения ответов
user_answers = {}

# Функция для отправки следующего вопроса
def ask_question(chat_id):
    if chat_id not in user_answers:
        user_answers[chat_id] = []

    if len(user_answers[chat_id]) < len(questions):
        question = questions[len(user_answers[chat_id])]
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add(types.KeyboardButton('Да'))
        markup.add(types.KeyboardButton('Нет'))
        bot.send_message(chat_id, question, reply_markup=markup)
    else:
        bot.send_message(chat_id, "Опрос завершен. Спасибо за участие!")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет! Давайте начнем опрос.")
    ask_question(chat_id)

# Обработчик ответов на вопросы
@bot.message_handler(func=lambda message: message.text in ['Да', 'Нет'])
def handle_answer(message):
    chat_id = message.chat.id
    answer = message.text
    user_answers[chat_id].append(answer)
    ask_question(chat_id)

if __name__ == "__main__":
    # Функция, которая будет выполняться в качестве демона
    def run_bot():
        while True:
            try:
                bot.polling(none_stop=True, interval=0)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

    # Создание объекта DaemonContext
    with daemon.DaemonContext():
        run_bot()
