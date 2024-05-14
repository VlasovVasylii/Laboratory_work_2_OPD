import random
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import API_TOKEN

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Состояния для игры
class GuessGame(StatesGroup):
    start = State()
    guess = State()


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет Давай сыграем в игру 'Угадай число'.\n"
                         "Я загадал число от 1 до 100. Попробуй угадать!")
    await message.answer("Введи свое число:")

    await GuessGame.guess.set()


# Обработчики ввода
@dp.message_handler(lambda message: not message.text.isdigit() and 1 <= int(message.text) <= 100, state=GuessGame.guess)
async def wrong_input(message: types.Message, state: FSMContext):
    await message.answer("Неправильно! Это должно быть число от 1 до 100.")


@dp.message_handler(state=GuessGame.guess)
async def process_guess(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if 'number' not in data:
            data['number'] = random.randint(1, 100)
            data['count'] = 0
        else:
            data['count'] += 1
        number = data['number']
        count = data['count']

    # Получаем число, введенное пользователем
    guess = int(message.text)

    if guess == number:
        await message.answer(f"Поздравляю Ты угадал число. Попыток: {count}.")
        await state.finish()
    elif guess < number:
        await message.answer("Твое число меньше загаданного. Попробуй еще раз:")
    else:
        await message.answer("Твое число больше загаданного. Попробуй еще раз:")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
