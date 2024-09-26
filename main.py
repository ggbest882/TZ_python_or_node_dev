import aiohttp 
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Функция для получения курса USD
def get_usd_rate():
    try:
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data = response.json()
        usd_rate = data['Valute']['USD']['Value']
        return usd_rate
    except Exception as e:
        print(f"Error getting USD rate: {e}")
        return None

# Функция, которая приветствует пользователя
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Добрый день. Как вас зовут?')

# Функция, которая дает обратный ответ с его сообщением
async def handle_name(update: Update, context: CallbackContext) -> None:
    user_name = update.message.text
    usd_rate = get_usd_rate()
    if usd_rate:
        await update.message.reply_text(f'Рад знакомству, {user_name}! Курс доллара сегодня {usd_rate:.2f}р.')
    else:
        await update.message.reply_text(f'Рад знакомству, {user_name}! Не удалось получить курс доллара.')

def main() -> None:
    token = 'secret)'
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start)) #регистрация обработчки на команду /start
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))#обработчик для всех текстовых сообщений

    application.run_polling()

if __name__ == '__main__':
    main()
