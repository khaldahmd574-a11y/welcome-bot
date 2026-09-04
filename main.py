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

# دالة مستقلة تعنى بانتظار 60 ثانية وحذف الرسالة في الخلفية
async def delete_message_after_delay(chat_id: int, message_id: int, delay: int = 60):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        print(f"تم حذف الرسالة {message_id} بنجاح بعد {delay} ثانية.")
    except Exception as e:
        print(f"خطأ أثناء حذف الرسالة: {e}")

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def on_user_join(event: types.ChatMemberUpdated):
    user = event.new_chat_member.user
    
    # عرض اسم العضو كما هو
    name = user.full_name or user.first_name or "الضيف"
    
    # نص الترحيب الخاص بك
    welcome_text = (
        f"✨ يا هلا بـ {name} 🤍\n"
        f"🌷 نورت/ي وشرفت/ي، حياك الله بيننا 🙏🏻\n"
        f"🤍 سعداء بخدمتك دائمًا ✨"
    )
    
    try:
        # 1. إرسال الرسالة
        msg = await bot.send_message(chat_id=event.chat.id, text=welcome_text)
        
        # 2. تشغيل مهمة الحذف في الخلفية بشكل مستقل دون إيقاف البوت
        asyncio.create_task(delete_message_after_delay(event.chat.id, msg.message_id, 60))
        
    except Exception as e:
        print(f"حدث خطأ أثناء إرسال الترحيب: {e}")

async def main():
    print("Bot is starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
