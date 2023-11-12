import daemon

from IdeaSoftBot import bot  # Импортируем бот из файла bot.py

def main():
    with daemon.DaemonContext():
        bot.infinity_polling()

if __name__ == "__main__":
    main()
