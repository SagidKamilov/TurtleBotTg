from aiogram import types
from aiogram.dispatcher.filters import Text, ChatTypeFilter
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher
from api.Turtle_API import API
from bot.keyboards import general_keyboards
from bot.messages_localization import messages_registration, messages_help

class RegisterUser(StatesGroup):
    registration_one = State()
    registration_two = State()


# Запуск машины состояний для регистрации
async def begin(message: types.Message):
    await RegisterUser.registration_one.set()
    await message.answer(text='👀 Привет, перед использованием бота давай я помогу в нем разобраться.', reply_markup=general_keyboards.full_choice_keyboard())

async def interceptor(callback: types.CallbackQuery):
    await callback.answer()

async def stop(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text='📌 Если тебе вдруг понадобится помощь в регистрации, набери команду "регистрация".\nВот список моих команд:')
    await callback.message.answer(text=messages_help.help_message)
async def interrupt(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.edit_text(text='Как скажешь 🐢\nВот список моих команд:')
    await callback.message.answer(text=messages_help.help_message)

async def yes_agree(callback: types.CallbackQuery):
    await RegisterUser.next()
    await callback.message.edit_text(text=messages_registration.registration_enter_group)


async def finish(message: types.Message, state: FSMContext):
    if message.text.upper() in API().take_group_list().get('group'):
        await message.answer(text=messages_registration.registration_finish, reply_markup=general_keyboards.full_keyboard(group=message.text.upper()))
        await state.finish()
    else:
        await message.answer(text=messages_registration.registration_no_group, reply_markup=general_keyboards.no_registration_keyboard())
# Функция- регистаротор хендлеров личных сообщений

async def my_group(message: types.Message):
    filtered_message = lambda message: message.text.lower().replace('моя группа ', '').upper()
    if filtered_message(message=message) in API().take_group_list().get('group'):
        await message.answer(text=messages_registration.registration_finish, reply_markup=general_keyboards.full_keyboard(group=filtered_message(message=message)))
    else:
        await message.answer(text='[🚫] Не могу найти такую группу, проверь пожалуйста, правильно ли ты написал группу.')

async def del_keyboard(message: types.Message):
    await message.answer(text='[✅] Убрал клавиатуру', reply_markup=general_keyboards.ReplyKeyboardRemove())


def register_temp_chat_handlers(dp: Dispatcher):
    dp.register_message_handler(begin, commands=['start'])
    dp.register_message_handler(begin, ChatTypeFilter(chat_type=types.ChatType.PRIVATE), Text(equals=messages_registration.equals.get('start'), ignore_case=True), state=None)
    dp.register_callback_query_handler(interrupt, Text(equals=messages_registration.equals.get('interrupt'), ignore_case=True), state="*")
    dp.register_callback_query_handler(stop, Text(equals=messages_registration.equals.get('stop'), ignore_case=True), state="*")
    dp.register_callback_query_handler(yes_agree, Text(equals=messages_registration.equals.get('continue')), state=RegisterUser.registration_one)
    dp.register_message_handler(finish, content_types='text', state=RegisterUser.registration_two)
    dp.register_message_handler(my_group, lambda message: "моя группа" in message.text.lower())
    dp.register_message_handler(del_keyboard, Text(equals='убери клавиатуру', ignore_case=True))
