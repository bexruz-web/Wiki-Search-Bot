import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters

# Config
from config import BOT_TOKEN

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Salom👋 <b>{update.message.from_user.first_name}</b> Xush kelibsiz.\n"
                              f"🌐 Wikipediadan so'rovingiz bo'yicha malumot olib kelaman! "
                              f"/search va so'rovingizni yozing.\nMasalan: /search Alisher Navoiy", parse_mode='HTML')

def search(update: Update, context: CallbackContext):
    args = context.args

    if len(args) == 0:
        update.message.reply_text("🤔 Izlamoqchi bo'lgan malumotingizni sarlavhasini kiriting.\nMasalan: /search Alisher Navoiy")
    else:
        search_text = ' '.join(args)
        response = requests.get("https://uz.wikipedia.org/w/api.php", {
            'action': 'opensearch',
            'search': search_text,
            'limit': 1,
            'namespace': 0,
            'format': 'json'
        })

        result = response.json()
        link = result[3]

        if len(link):
            update.message.reply_text("😃 Sizning so'rovingiz bo'yicha havola: " + link[0])
        else:
            update.message.reply_text("Sizning so'rovingiz bo'yicha hech nima topilmadi😔\nQayta urining...")

def main() -> None:
    # Botni ishga tushirish
    print("Bot started....")
    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('search', search))
    dispatcher.add_handler(MessageHandler(Filters.all, start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
