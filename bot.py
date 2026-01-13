import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import ChatMemberUpdatedFilter, IS_MEMBER

# التوكن الخاص بك
TOKEN = '8531530454:AAFaqt0jTm4I-QaQM4w_2MRYjy0veWOAfnM'

# قائمة القنوات
CHANNELS = [-1003692216206, -1003565914121, -1003562101151, -1003640402409, -1003512003568]

bot = Bot(token=TOKEN)
dp = Dispatcher()
active_trackers = set()

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER))
async def on_user_join(event: types.ChatMemberUpdated):
    user_id = event.from_user.id
    if event.chat.id in CHANNELS and user_id not in active_trackers:
        active_trackers.add(user_id)
        print(f"👤 بدأ عداد 6 ساعات لـ {event.from_user.full_name}")
        
        await asyncio.sleep(21600) # 6 ساعات
        
        for channel_id in CHANNELS:
            try:
                await bot.ban_chat_member(chat_id=channel_id, user_id=user_id)
            except:
                pass
        active_trackers.remove(user_id)

async def main():
    print("🚀 البوت انطلق ويعمل 24 ساعة...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
