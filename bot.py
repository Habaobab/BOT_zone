import random
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = '8615567090:AAFUT4hSC9A71yTNMzfWa0UW44TNNDDTp3Y'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

DATA_FILE = "history.json"


def load_history():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(history):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-2:], f, ensure_ascii=False)


def distribute(names):
    history = load_history()

    zones_count = len(names)

    if zones_count == 9:
        z1 = 4
    elif zones_count == 8:
        z1 = 3
    elif zones_count == 7:
        z1 = 2
    else:
        return "Нужно 7-9 человек"

    z2 = 2
    z3 = 1
    z4 = 2

    random.shuffle(names)

    if history:
        last_shift = history[-1]

        def penalty(name, zone):
            if name in last_shift.get(zone, []):
                return 1
            return 0

        best = None
        best_score = 999

        for _ in range(50):
            random.shuffle(names)

            attempt = {
                "1": names[:z1],
                "2": names[z1:z1+z2],
                "3": names[z1+z2:z1+z2+z3],
                "4": names[z1+z2+z3:]
            }

            score = 0
            for zone in attempt:
                for name in attempt[zone]:
                    score += penalty(name, zone)

            if score < best_score:
                best_score = score
                best = attempt

        result = best
    else:
        result = {
            "1": names[:z1],
            "2": names[z1:z1+z2],
            "3": names[z1+z2:z1+z2+z3],
            "4": names[z1+z2+z3:]
        }

    history.append(result)
    save_history(history)

    return result


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "Отправь имена через пробел\n\nПример:\nИван Петр Саша Али Мага Руслан Артем"
    )


@dp.message_handler()
async def handle(message: types.Message):
    names = message.text.split()

# убираем первую команду (/zone)
if names[0].startswith("/"):
    
    names = names[1:]

    result = distribute(names)

    if isinstance(result, str):
        await message.answer(result)
        return

    text = ""

    for zone in ["1", "2", "3", "4"]:
        text += f"\nЗона {zone}:\n"
        for name in result[zone]:
            text += f"- {name}\n"

    await message.answer(text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

