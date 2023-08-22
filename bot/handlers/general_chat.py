from aiogram import types
from aiogram import Dispatcher
from bot.messages_localization import messages_help, icons, messages_registration
from api.Turtle_API import API
from utils import Prepods, distance_leven


# Хендлер обработки команды "пары на неделю"
async def get_week_apairs(message: types.Message):
    #  Фильтры для разделения команды от передаваемого объекта
    filtered_message = lambda message: message.text.lower().replace('пары на неделю ', '').upper()
    if filtered_message(message) == 'ПАРЫ НА НЕДЕЛЮ':
        pass
    else:
        try:
            # Сборка расписания из json-файла
            schedule = f'{filtered_message(message)}'
            for day in API().take_schedule_group(group=filtered_message(message)).get('days'):
                schedule += f"{icons.before_strike}{icons.calendar} {day.get('day')}{icons.after_strike}"
                for apairs in day.get('apairs'):
                    element = apairs.get('apair')[0]
                    schedule += f"{icons.time} {apairs.get('time')} {icons.number_pairs(element.get('number'))}\n{icons.pair} {element.get('doctrine')}" \
                                f"\n{icons.teacher} {element.get('teacher')}\n{icons.key} {element.get('auditoria')}\n{icons.building} {element.get('corpus')}\n"
            await message.answer(text=schedule)
        except TypeError:
            #  Обработка ошибки неопределенных данных из API, при которых выдает NoneType "сборка расписания" -- надо изменить, как починят API
            await message.answer(text=messages_registration.registration_no_group)


# Хендлер для обработки команды "пары"
async def get_apairs(message: types.Message):
    #  Фильтры для разделения команды от передаваемого объекта
    filtered_message = lambda message: message.text.lower().replace('пары ', '').upper()
    if filtered_message(message) == 'ПАРЫ':
        pass
    else:
        try:
            # Сборка расписания из json-файла
            schedule = f'{filtered_message(message)}'
            for day in API().take_schedule_group(group=filtered_message(message)).get('days')[0:2]:
                schedule += f"{icons.before_strike}{icons.calendar} {day.get('day')}{icons.after_strike}"
                for apairs in day.get('apairs'):
                    element = apairs.get('apair')[0]
                    schedule += f"{icons.time} {apairs.get('time')} {icons.number_pairs(element.get('number'))}\n{icons.pair} {element.get('doctrine')}" \
                                f"\n{icons.teacher} {element.get('teacher')}\n{icons.key} {element.get('auditoria')}\n{icons.building} {element.get('corpus')}\n"
            await message.answer(text=schedule)
        except TypeError:
            #  Обработка ошибки неопределенных данных из API, при которых выдает NoneType "сборка расписания" -- надо изменить, как починят API
            await message.answer(text=messages_registration.registration_no_group)


# Хендлер для обработки команды "фио"
async def get_fio_teacher(message: types.Message):
    filtered_message = lambda message: message.text.lower().replace('фио ', '').upper()
    if filtered_message(message) == 'ФИО':
        pass
    else:
        finded_name = Prepods.find_people(filtered_message(message))
        if len(finded_name) == 1:
            msg = finded_name[0].full_name
        else:
            print('ok1')
            print(finded_name)
            if len(finded_name) > 1:
                print("ok2")
                if finded_name[0].family != finded_name[1].family:
                    msg = f'{messages_help.answer_not_fio}\n\n'
                    msg += f'Возможно, Вы искали:\n'
                    finded_name = list(map(lambda x: x.family, finded_name))
                    msg += '\n'.join(finded_name)
                    await message.answer(text=msg+"    ----")
                elif finded_name[0].family == finded_name[1].family:
                    finded_name = list(map(lambda x: x.full_name, finded_name))
                    msg = '\n'.join(finded_name)
            else:
                msg = f'{messages_help.answer_not_fio}'
        await message.answer(text=msg)

# Хендлер для обработки команды "помощь"
async def get_help(message: types.Message):
    await message.answer(text=messages_help.help_message)


# Хендлер для обработки команды "звонки"
async def get_sounds(message: types.Message):
    await message.answer(text=messages_help.calls_message)


# Функция-регистаротор хендлеров общих сообщений
def register_general_chat_handlers(dp: Dispatcher):
    dp.register_message_handler(get_week_apairs, lambda message: 'пары на неделю' in message.text.lower())
    dp.register_message_handler(get_apairs, lambda message: "пары" in message.text.lower())
    dp.register_message_handler(get_fio_teacher, lambda message: 'фио' in message.text.lower())
    dp.register_message_handler(get_help, lambda message: message.text.lower() == "помощь")
    dp.register_message_handler(get_sounds, lambda message: message.text.lower() == "звонки")
