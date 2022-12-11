from aiogram import types
from aiogram.dispatcher.filters import Filter

import res


class IsAdmin(Filter):
    key = "is_admin"

    async def check(self, message: types.Message):
        return message.from_user.id in res.ADMIN_ID
