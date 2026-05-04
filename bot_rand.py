import os
import asyncio
import random
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events

# ===== ДАННЫЕ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ =====
api_id = int(os.environ.get('API_ID'))
api_hash = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
# =========================================

app = Flask('')

@app.route('/')
def home():
    return "Бот работает"

def run_http():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_http)
    t.start()

bot = TelegramClient('bot_rand', api_id, api_hash).start(bot_token=BOT_TOKEN)

searching = False
consonants = 'bcdfghjklmnpqrstvwxz'
vowels = 'aeiouy'

def generate_random_word(length):
    word = ""
    for i in range(length):
        if i % 2 == 0:
            word += random.choice(consonants)
        else:
            word += random.choice(vowels)
    return word

async def check_username(name):
    try:
        await bot.get_entity(name)
        return False
    except:
        return True

@bot.on(events.NewMessage)
async def commands(event):
    global searching
    text = event.raw_text.lower().strip()

    if text == '/start':
        await event.reply("Бот работает!\n/rand — найти юзернеймы")

    elif text == '/rand':
        if searching:
            await event.reply("⏳ Уже ищу")
            return

        searching = True
        found = []
        await event.reply("🎲 Проверяю 5 случайных юзернеймов...")

        for i in range(5):
            length = random.choice([5, 6, 7])
            username = generate_random_word(length)
            await event.reply(f"🔄 {i+1}/5: @{username}")

            if await check_username(username):
                found.append(f"@{username}")
                await event.reply(f"✅ СВОБОДЕН! @{username}")
            else:
                await event.reply(f"❌ Занят: @{username}")

            await asyncio.sleep(0.5)

        if found:
            await event.reply(f"🎉 Найдено: " + ", ".join(found))
        else:
            await event.reply("❌ Ничего не найдено")

        searching = False

    elif text == '/stop':
        if searching:
            searching = False
            await event.reply("⏹ Остановлено")
        else:
            await event.reply("Поиск не запущен")

async def main():
    await bot.start()
    print("Бот запущен")
    await bot.run_until_disconnected()

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())
