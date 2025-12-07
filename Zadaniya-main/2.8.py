from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder



# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '8229577510:AAGOAEhbjYG5EPnua1ERftH9MATGrxdeaOY'

# Инициализируем билдер
kb_builder = ReplyKeyboardBuilder()



# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем список с кнопками
buttons: list[KeyboardButton] = [
    KeyboardButton(text=f'Кнопка {i + 1}') for i in range(10)
]


# Распаковываем список с кнопками в билдер, указываем, что
# в одном ряду должно быть 4 кнопки
kb_builder.row(*buttons, width=4)



# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        text='Вот такая получается клавиатура',
        reply_markup=kb_builder.as_markup(resize_keyboard=True)
    )



if __name__ == '__main__':
    dp.run_polling(bot)
