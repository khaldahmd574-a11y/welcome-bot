import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# خادم ويب وهمي لإرضاء Render
async def handle_ping(request):
    return web.Response(text="Bot is running perfectly!")

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def on_user_join(event: types.ChatMemberUpdated):
    user_name = event.new_chat_member.user.first_name
    welcome_text = f"أهلاً بك يا {user_name} في المجموعة! 👋"
    
    msg = await bot.send_message(chat_id=event.chat.id, text=welcome_text)
    
    await asyncio.sleep(60)
    try:
        await bot.delete_message(chat_id=event.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

async def main():
    print("Bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    
    # تشغيل خادم الويب على المنفذ المطلوب لـ Render
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    # بدء استقبال التحديثات
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
