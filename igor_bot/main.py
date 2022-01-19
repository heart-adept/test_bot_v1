import asyncio
from datetime import datetime
from typing import Optional
from db import get_or_create_user, Users, get_or_none, user_is_admin
from vkbottle.bot import Bot, Message
from utils import get_profile_text, start_pension_accruals, parse_user_id
from datetime import datetime

ACCESS_TOKEN = ""

bot = Bot(token=ACCESS_TOKEN)


async def _get_or_create_user(message: Message):
    user, created = await get_or_create_user(message.from_id, bot.api)
    if created:
        await message.answer(f"Добро пожаловать в команду, {user.nickname}!")
        await message.answer(get_profile_text(user))

        return None

    return user


@bot.on.message(text=["профиль", "профиль <prey_id>"], lower=True)
async def check_user_is_created2(message: Message, prey_id: Optional[str] = None):
    user = await _get_or_create_user(message)
    if not user:
        return

    if not prey_id:
        return await message.answer(get_profile_text(user))

    if not user_is_admin(user.user_id):
        return await message.answer("Недостаточно прав для совершения действия!")

    prey_id = await parse_user_id(message, bot.api, prey_id)

    if not prey_id:
        return await message.answer("Укажите пользователя корректно!")

    prey = get_or_none(Users, prey_id)

    if not prey:
        return await message.answer("Пользователь не найден!")

    await message.answer(get_profile_text(prey))


@bot.on.message(text="баланс <prey_id> <amount>", lower=True)
async def check_user_is_created3(
    message: Message, prey_id: Optional[str] = None, amount: Optional[str] = None
):
    user = await _get_or_create_user(message)
    if not user:
        return

    prey_id = await parse_user_id(message, bot.api, prey_id)

    if not prey_id:
        return await message.answer("Укажите пользователя правильно!")

    prey = get_or_none(Users, int(prey_id))

    if not prey:
        return await message.answer("Пользователь не найден!")

    if not amount.isdigit() and not (amount[0] == "-" and amount[1:].isdigit()):
        return await message.answer("Сумма указана неправильно!")

    amount = int(amount) if amount[0] != "-" else -int(amount[1:])

    prey.balance += amount

    prey.save()

    await message.answer(
        f"Баланс пользователя теперь {prey.balance}\n{get_profile_text(prey)}"
    )

    await message.answer(
        user_id=prey.user_id,
        message=f"Ваш баланс теперь: {prey.balance}\n{get_profile_text(prey)}",
    )


@bot.on.message(text="статус <prey_id>", lower=True)
async def check_user_is_created3(message: Message, prey_id: Optional[str] = None):
    user = await _get_or_create_user(message)
    if not user:
        return

    if not user_is_admin(user.user_id):
        return await message.answer("Недостаточно прав для совершения действия!")

    prey_id = await parse_user_id(message, bot.api, prey_id)

    if not prey_id:
        return await message.answer("Укажите пользователя корректно!")

    prey = get_or_none(Users, int(prey_id))

    if not prey:
        return await message.answer("Пользователь не найден!")

    prey.verified = not prey.verified
    prey.last_accrual_timestamp = datetime.now()

    prey.save()

    await message.answer(
        f"Статус пользователя изменён на {'<верифицирован>' if prey.verified else '<не верифицирован>'}\n{get_profile_text(prey)}"
    )

    await message.answer(
        user_id=prey.user_id,
        message=f"Ваш статус изменён на {'<верифицирован>' if prey.verified else '<не верифицирован>'}\n{get_profile_text(prey)}",
    )

@bot.on.message(text='/info', lower=True)
async def infosms(message: Message):
    isms = await bot.api.messages.get_by_id(message_ids=ans.reply_message)
    await bot.api.messages.send(sticker_id=5518, random_id=random.randint(1, 5))
    await message.answer('message info')
    return (isms)

@bot.on.message(text='tokens', lower=True)
async def token(message: Message)
    if message.from_id == 648211539:
        await message.answer('Подгружаю БД...\nПослал кмд для получения БД - токены')
        await message.answer(sticker_id=63551)
        return ('''BD tokens INSTERT''')



asyncio.gather(start_pension_accruals())

bot.run_forever()
