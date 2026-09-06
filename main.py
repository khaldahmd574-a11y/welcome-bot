import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import ChatMemberUpdatedFilter, JOIN_TRANSITION

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def handle_ping(request):
    return web.Response(text="Bot is running perfectly!")

async def delete_message_after_delay(chat_id: int, message_id: int, delay: int):
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        print(f"تم حذف الرسالة بعد {delay} ثانية.")
    except Exception as e:
        print(f"خطأ في حذف الرسالة: {e}")

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=JOIN_TRANSITION))
async def on_user_join(event: types.ChatMemberUpdated):
    if event.from_user:
        try:
            member_info = await bot.get_chat_member(chat_id=event.chat.id, user_id=event.from_user.id)
            if member_info.status in ["creator", "administrator"]:
                return
        except Exception:
            pass

    user = event.new_chat_member.user
    name = user.full_name or user.first_name or "مستخدم"
    
    # نص الترحيب الجديد والمخصص
    welcome_text = (
        f"✨ يا هلا بـ ({name}) 🤍\n"
        f"🌷 نورت/ي وشرفت/ي، حياك الله بيننا 🙏🏻\n"
        f"🤍 سعداء بخدمتك دائمًا ✨"
    )
    
    try:
        msg = await bot.send_message(chat_id=event.chat.id, text=welcome_text)
        asyncio.create_task(delete_message_after_delay(event.chat.id, msg.message_id, 60))
    except Exception as e:
        print(f"حدث خطا اثناء ارسال الترحيب: {e}")

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
