import random
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "8615567090:AAFUT4hSC9A71yTNMzfWa0UW44TNNDDTp3Y"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

history_file = "zone_history.json"


def load_history():
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_history(data):
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def distribute(names):

    history = load_history()

    zones = {
        "Зона 1": [],
        "Зона 2": [],
        "Зона 3": [],
        "Зона 4": []
    }

    count = len(names)

    if count >= 9:
        caps = {
            "Зона 1": 4,
            "Зона 2": 2,
            "Зона 3": 1,
            "Зона 4": 2
        }
    else:
        caps = {
            "Зона 1": 0,
            "Зона 2": 2,
            "Зона 3": 1,
            "Зона 4": 2
        }

    random.shuffle(names)

    for name in names:

        last = history.get(name, [])[-2:]

        possible = []

        for zone in zones:

            if len(zones[zone]) >= caps.get(zone, 0):
                continue

            if zone in last:
                continue

            possible.append(zone)

        if not possible:
            for zone in zones:
                if len(zones[zone]) < caps.get(zone, 0):
                    possible.append(zone)

        if not possible:
            possible = ["Зона 2", "Зона 3", "Зона 4"]

        zone = random.choice(possible)

        zones[zone].append(name)

        if name not in history:
            history[name] = []

        history[name].append(zone)

        if len(history[name]) > 5:
            history[name] = history[name][-5:]

    save_history(history)

    return zones


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Напиши:\n"
        "/zone Имена тех кто на смене"
    )


@dp.message_handler(commands=["zone"])
async def zone_command(message: types.Message):

    parts = message.text.split()

    if len(parts) < 2:
        await message.answer("Напиши имена после команды")
        return

    names = parts[1:]

    zones = distribute(names)

    text = "Распределение зон:\n\n"

    for z, people in zones.items():

        if not people:
            continue

        text += f"{z}\n"

        for p in people:
            text += f"• {p}\n"

        text += "\n"

    await message.answer(text)


if __name__ == "__main__":
    executor.start_polling(dp)
