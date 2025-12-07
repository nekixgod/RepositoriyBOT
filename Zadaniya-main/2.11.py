from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder



# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '8229577510:AAGOAEhbjYG5EPnua1ERftH9MATGrxdeaOY'


# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Инициализируем билдер
kb_builder = ReplyKeyboardBuilder()


# Создаем первый список с кнопками
buttons_1: list[KeyboardButton] = [
    KeyboardButton(text=f'Кнопка {i + 1}') for i in range(8)
]
# Распаковываем список с кнопками методом add
kb_builder.add(*buttons_1)


# Явно сообщаем билдеру сколько хотим видеть кнопок в 1-м и 2-м рядах
kb_builder.adjust(1, 3)




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
