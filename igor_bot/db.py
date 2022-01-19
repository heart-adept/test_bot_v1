from peewee import *
from vkbottle import API
from vkbottle.framework.bot.labeler import default
from vkbottle.tools.dev_tools.uploader import doc
from datetime import date, datetime

db = SqliteDatabase("database.db")

# Models
# User model
class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    user_id = BigIntegerField(primary_key=True, index=True)
    nickname = CharField(max_length=32)
    balance = FloatField(default=100)
    verified = BooleanField(default=False)
    last_accrual_timestamp = DateTimeField(
        default=datetime.now()
    )  # Не вызывается каждый раз при создании, устанавливается при запуске


class Admins(BaseModel):
    user_id = ForeignKeyField(
        Users, Users.user_id, on_delete="CASCADE", on_update="CASCADE"
    )


def get_or_none(model, *args, **kwargs):
    try:
        return model.get(*args, **kwargs)

    except DoesNotExist:
        return None


async def get_or_create_user(user_id: int, vk_api_client: API):

    _user = get_or_none(Users, user_id=user_id)
    _created = False

    if not _user:
        _users_info = await vk_api_client.users.get(user_id)
        _user = Users.create(
            user_id=user_id,
            nickname=_users_info[0].first_name,
            last_accrual_timestamp=datetime.now(),
        )
        _created = True

    return _user, _created


def user_is_admin(user_id):
    if get_or_none(Admins, user_id=user_id):
        return True

    return False


if db:
    Users.create_table(True)
    Admins.create_table(True)
