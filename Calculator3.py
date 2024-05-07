import asyncio
import aiogram
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types, executor
import math

# Создаем бота и диспетчер
bot = Bot(token="6992774428:AAHkuw6u5fRAB01tZhsPmAnVazhjJyFAEcw")
dp = Dispatcher(bot)

# Словарь с формулами и подсказками
formulas = {
    "Скорость": ("расстояние (м)", "время (с)"),
    "Ускорение": ("начальная скорость (м/с)", "конечная скорость (м/с)", "время (с)"),
    "Сила тяжести": ("масса (кг)"),
    "Закон Кулона": ("заряд 1 (Кл)", "заряд 2 (Кл)", "расстояние (м)"),
    "Магнитное поле": ("ток (А)", "расстояние (м)"),
}

# Клавиатура с формулами
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons = ["Скорость", "Ускорение", "Сила тяжести", "Закон Кулона", "Магнитное поле"]
keyboard.add(*buttons)

# Обработчик старта
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Выберите формулу для расчета:", reply_markup=keyboard)

# Обработчик нажатий на кнопки
@dp.message_handler(lambda message: message.text in formulas)
async def request_values(message: types.Message):
    # Выводим подсказки для ввода значений
    formula = message.text
    prompts = formulas[formula]
    await message.answer(f"Введите значения для '{formula}' через пробел (разделяйте целые и дробные части точкой): {prompts}")

# Обработчик ввода значений
@dp.message_handler(lambda message: message.text not in formulas)
async def calculate(message: types.Message):
    # Получаем введенные значения
    values = message.text.split()
    try:
        values = [float(value) for value in values]
    except ValueError:
        await message.answer("Пожалуйста, введите числа.")
        return

    # Вычисляем результат
    result = None
    if len(values) == 2:
        displacement, time = values
        result = displacement / time
        await message.answer(f"Результат: скорость = {result} м/с")
    elif len(values) == 3 and "Ускорение" in message.reply_to_message.text:
        initial_velocity, final_velocity, time = values
        result = (final_velocity - initial_velocity) / time
        await message.answer(f"Результат: Ускорение = {result} м/с²")
    elif len(values) == 1 and "Сила тяжести" in message.reply_to_message.text:
        mass = values[0]
        acceleration_due_to_gravity = 9.81
        result = mass * acceleration_due_to_gravity
        await message.answer(f"Результат: Сила тяжести = {result} Н")
    elif len(values) == 3 and "Закон Кулона" in message.reply_to_message.text:
        charge1, charge2, distance = values
        k = 8.9875517873681764 * math.pow(10, 9)  # Константа Кулона
        result = k * (charge1 * charge2) / (math.pow(distance, 2))
        await message.answer(f"Результат: Закон Кулона = {result} Н·м²/Кл²")
    elif len(values) == 2 and "Магнитное поле" in message.reply_to_message.text:
        current, distance = values
        permeability_of_free_space = 4 * math.pi * math.pow(10, -7)
        result = (permeability_of_free_space * current) / (2 * math.pi * distance)
        await message.answer(f"Результат: =Магнитное поле = {result} Тл")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
