from aiogram import types
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from bot.messages_localization import messages_registration, messages_help
from api.Turtle_API import API
from bot.keyboards import general_keyboards

# Временный список id
temp_list = ['1147186426']


class RegisterUser(StatesGroup):
    registration_one = State()
    registration_two = State()
    registration_three = State()
    registration_four = State()


# Запуск машины состояний для регистрации
async def begin(message: types.Message):
    if message.from_user.id in temp_list:
        await message.answer(text=messages_registration.already_regitered)
    else:
        await RegisterUser.registration_one.set()
        await message.answer(text=messages_registration.registration_start, reply_markup=general_keyboards.full_choice_keyboard())


# Перехватчик ненужных callback
async def interceptor(callback: types.CallbackQuery):
    await callback.answer()


# Прерывание машины состояний и редактирование сообщения + выдача списка команд help на текст "Нет, не надо"
async def stop(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text=messages_registration.registration_no_enter)
    await callback.message.answer(text=messages_help.help_message)


# Прерывание машины состояний и редактирование сообщения + выдача списка команд help на текст "Я больше не хочу регистрироваться"
async def interrupt(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text=messages_registration.registration_interrupt)
    await callback.message.answer(text=messages_help.help_message)


# Первый этап регистрации: точка входа
async def registration_one(callback: types.CallbackQuery):
    await RegisterUser.next()
    await callback.message.edit_text(text=messages_registration.registration_enter_group)


# Второй этап регистрации: ввод группы
async def registration_two(message: types.Message, state: FSMContext):
    if message.text.upper() in API().take_group_list().get('group'):
        async with state.proxy() as data:
            data["enter_group"] = message.text.upper()
        await message.answer(text=messages_registration.registration_sender, reply_markup=general_keyboards.short_choice_keyboard_3())
        await RegisterUser.next()
    else:
        await message.answer(text=messages_registration.registration_no_group, reply_markup=general_keyboards.no_registration_keyboard())


# Третий этап регистрации - ветка "да": выбор соглашения регистрации
async def registration_three_yes(callback: types.CallbackQuery):
    if callback.from_user.id in temp_list:
        await callback.message.edit_text(text=messages_registration.registration_already_regis)
    else:
        await callback.message.edit_text(text=messages_registration.registration_if_yes)
    await callback.message.answer(text=messages_registration.registration_want_keyboard, reply_markup=general_keyboards.short_choice_keyboard_4())
    await RegisterUser.next()


# Третий этап регистрации - ветка "нет": выбор отказа от регистрации
async def registration_three_no(callback: types.CallbackQuery):
    await callback.message.edit_text(text=messages_registration.registration_if_no)
    await callback.message.answer(text=messages_registration.registration_want_keyboard, reply_markup=general_keyboards.short_choice_keyboard_4())
    await RegisterUser.next()


# Четвертый этап регистрации - ветка "да": выбор получения клавиатуры с парами своей группы
async def registration_four_yes(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        enter_group = data["enter_group"]
    await state.finish()
    await callback.message.edit_text(text=messages_registration.registration_give_keyboard)
    await callback.message.answer(text=messages_registration.registration_finish, reply_markup=general_keyboards.full_keyboard(group=enter_group))


# Четвертый этап регистрации - ветка "да": выбор отказа от клавиатуры с парами своей группы
async def registration_four_no(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.answer(text=messages_registration.registration_finish)




# Функция-регистаротор хендлеров личных сообщений
def register_private_chat_handlers(dp: Dispatcher):
    dp.register_message_handler(begin, commands=['start'])
    dp.register_message_handler(begin, ChatTypeFilter(chat_type=types.ChatType.PRIVATE), Text(equals=messages_registration.equals.get('start'), ignore_case=True), state=None)
    dp.register_callback_query_handler(stop, Text(equals=messages_registration.equals.get('stop'), ignore_case=True), state="*")
    dp.register_callback_query_handler(interrupt, Text(equals=messages_registration.equals.get('interrupt'), ignore_case=True), state="*")
    dp.register_callback_query_handler(registration_one, ChatTypeFilter(chat_type=types.ChatType.PRIVATE), Text(equals=messages_registration.equals.get('continue'), ignore_case=True), state=RegisterUser.registration_one)
    dp.register_message_handler(registration_two, content_types='text', state=RegisterUser.registration_two)
    dp.register_callback_query_handler(registration_three_yes, Text(equals=messages_registration.equals.get('short_continue_3'), ignore_case=True), state=RegisterUser.registration_three)
    dp.register_callback_query_handler(registration_three_no, Text(equals=messages_registration.equals.get('short_stop_3'), ignore_case=True), state=RegisterUser.registration_three)
    dp.register_callback_query_handler(registration_four_yes, Text(equals=messages_registration.equals.get('short_continue_4'), ignore_case=True), state=RegisterUser.registration_four)
    dp.register_callback_query_handler(registration_four_no, Text(equals=messages_registration.equals.get('short_stop_4'), ignore_case=True), state=RegisterUser.registration_four)
    dp.register_callback_query_handler(interceptor, state="*")
