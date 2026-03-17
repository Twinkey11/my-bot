import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER
from aiohttp import web # مكتبة لعمل سيرفر وهمي

# --- بياناتك ---
TOKEN = '8531530454:AAFaqt0jTm4I-QaQM4w_2MRYjy0veWOAfnM'
CHANNELS = [-1003689581074, -1003761868452, -1003790425574, -1003666740348, -1003737621856, -1003779982472, -1003789291157, -1003856001705]

bot = Bot(token=TOKEN)
dp = Dispatcher()
active_trackers = set()

# --- السيرفر الوهمي لإرضاء موقع Koyeb ---
async def handle(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Koyeb بيعطينا رقم Port تلقائي في المتغير البيئي PORT
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌍 تم تشغيل السيرفر الوهمي على بورت {port}")

# --- منطق البوت الأساسي ---
@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER))
async def on_user_join(event: types.ChatMemberUpdated):
    user_id = event.from_user.id
    if event.chat.id in CHANNELS and user_id not in active_trackers:
        active_trackers.add(user_id)
        print(f"👤 رصد دخول: {event.from_user.full_name} - بدأ عداد ساعة")
        await asyncio.sleep(3600) # ساعة
        for channel_id in CHANNELS:
            try:
                await bot.ban_chat_member(chat_id=channel_id, user_id=user_id)
            except:
                pass
        active_trackers.remove(user_id)

async def main():
    # تشغيل السيرفر الوهمي في الخلفية
    await start_web_server()
    print("🚀 البوت يعمل الآن بنظام الـ Web Service...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
