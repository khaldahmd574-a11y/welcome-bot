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
    user = event.new_chat_member.user
    
    # عرض اسم العضو كما هو في حسابه تماماً
    name = user.full_name or user.first_name or "الضيف"
    
    # نص الترحيب الخاص بك
    welcome_text = (
        f"✨ يا هلا بـ {name} 🤍\n"
        f"🌷 نورت/ي وشرفت/ي، حياك الله بيننا 🙏🏻\n"
        f"🤍 سعداء بخدمتك دائمًا ✨"
    )
    
    try:
        # إرسال الرسالة
        msg = await bot.send_message(chat_id=event.chat.id, text=welcome_text)
        
        # الانتظار دقيقة واحدة (60 ثانية) بالضبط ثم الحذف
        await asyncio.sleep(60)
        await bot.delete_message(chat_id=event.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"حدث خطأ أثناء الترحيب أو الحذف: {e}")

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
