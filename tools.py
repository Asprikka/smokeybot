import json
import os
from typing import List

from aiogram import types

from datatypes import Vape
import res


def get_vapes_str(vapes_list: List[Vape]) -> str:
    result = ''

    cur_type = ''
    for vape in vapes_list:
        if vape.type != cur_type:
            cur_type = vape.type
            result += f'\n{vape.type}\n\n'

        result += f'{vape.name}\n'

    return result[1:-1]


def get_vapes_list(vapes_str: str) -> List[Vape]:
    vapes_split = [''] + vapes_str.split('\n') + ['']
    result: List[Vape] = []

    cur_type = ''
    for i in range(1, len(vapes_split)):
        if vapes_split[i] == '':
            continue

        if vapes_split[i - 1] == '' and vapes_split[i + 1] == '':
            cur_type = vapes_split[i]
            continue

        result.append(Vape(name=vapes_split[i], type=cur_type))

    return result


def update_json(path: str, list: list):
    with open(path, 'w') as f:
        f.write(json.dumps(list, default=lambda o: o.dict(), indent=4))


def load_vapes_list(path: str) -> List[Vape]:
    if not os.path.exists(path):
        f = open(path, 'x')
        f.close()

    with open(path, 'r') as f:
        f_str = f.read()

    if len(f_str) == 0:
        print(res.VAPES_LIST_EMPTY)
        return []

    vapes_dict = json.loads(f_str)
    vapes_list: List[Vape] = []

    for vape in vapes_dict:
        vapes_list.append(
            Vape(vape['name'], vape['type'])
        )

    return vapes_list


def build_forward_text(message: types.Message):
    result = f'''

Час: {message.date.strftime('%H:%M:%S - %d/%m')}

<b>{message.text}</b>'''

    if message.from_user.username in ['', None]:
        result = f'<b><a href="tg://user?id={message.chat.id}">({message.from_user.first_name} {message.from_user.last_name})</a></b>' + result
    else:
        result = f'<b>@{message.from_user.username}</b>' + result

    return result
