import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def on_user_join(event: types.ChatMemberUpdated):
    user_name = event.new_chat_member.user.first_name
    welcome_text = f"أهلاً بك يا {user_name} في المجموعة! 👋"
    
    # إرسال رسالة الترحيب
    msg = await bot.send_message(chat_id=event.chat.id, text=welcome_text)
    
    # الانتظار لمدة 60 ثانية ثم حذف الرسالة تلقائياً
    await asyncio.sleep(60)
    try:
        await bot.delete_message(chat_id=event.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

