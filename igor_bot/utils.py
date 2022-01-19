from traceback import format_exc
from db import Users, db
from vkbottle import API


def get_profile_text(user: Users):
    return f"""{user.nickname},
user_id: {user.user_id}
nickname: {user.nickname}
balance: {user.balance}
verified: {'✅' if user.verified else '❌'}"""


async def parse_user_id(message, api: API, user_id=None):
    if message.reply_message:
        return message.reply_message.from_id

    if not user_id:
        user_id = message.text

    if user_id and user_id.strip().isdigit():
        return int(user_id.strip())

    if user_id.startswith("-"):
        return int(user_id)

    if user_id.startswith("https://vk.com/"):
        user_id = user_id[15:]

    elif user_id.startswith("vk.com/"):
        user_id = user_id[7:]

    if user_id[:3] == "[id":
        puid = user_id[3:].split("|")[0]

        if puid.isdigit() and "]" in user_id[3:]:
            return int(puid)

    if user_id[:5] == "[club":
        puid = user_id[:5].split("|")[0]

        if "]" in user_id[5:]:
            return int(puid)

    tuid = await api.utils.resolve_screen_name(screen_name=user_id)

    try:
        return tuid.object_id or tuid.group_id
    except:
        return None

    return None


async def start_pension_accruals():

    from asyncio import sleep

    while True:
        await sleep(3)

        try:
            db.execute_sql(
                """UPDATE users SET balance = balance + ((CAST(strftime('%s', datetime('now', 'localtime')) AS INT) - CAST(strftime('%s', last_accrual_timestamp) AS INT)) / 1800 * 0.1),
            last_accrual_timestamp = datetime('now', 'localtime')
            WHERE (CAST(strftime('%s', datetime('now', 'localtime')) AS INT) - CAST(strftime('%s', last_accrual_timestamp) AS INT)) >= 1800
            AND verified=1;"""
            )
        except:
            print("[start_pension_accruals] [db.execute_sql]: " + format_exc())
