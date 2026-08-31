import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = "8826323705:AAH6jf-oyZwo-Fln1l1CslFaGtA4UHZMhAo"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            chat_id = update.message.chat_id
            first_name = member.first_name

            welcome_text = f"✨ يا هلا ومرحبا بـ <b>{first_name}</b> 🤍\n🌷 نورتنا وشرفت المكان، وسعدنا بانضمامك ❤️"

            try:
                sent_msg = await context.bot.send_message(
                    chat_id=chat_id,
                    text=welcome_text,
                    parse_mode="HTML"
                )
                await asyncio.sleep(60)
                await context.bot.delete_message(chat_id=chat_id, message_id=sent_msg.message_id)
            except Exception as e:
                print(f"Error: {e}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    welcome_handler = MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member)
    application.add_handler(welcome_handler)

    print("البوت جاهز ويرحب بالأعضاء...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

