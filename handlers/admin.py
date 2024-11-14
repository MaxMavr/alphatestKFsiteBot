from config import *
from typing import Tuple
rt: Router = Router()


PAGE_SIZE_USER = 20
PAGE_SIZE_BUG = 7


async def make_page_title(template: str, a=None, b=None, c=None, d=None, e=None) -> str:
    page_title = phrases[template]

    if a is not None:
        page_title = page_title.replace("&", str(a))
    if b is not None:
        page_title = page_title.replace("$", str(b))
    if c is not None:
        page_title = page_title.replace("#", str(c))
    if d is not None:
        page_title = page_title.replace("@", str(d))
    if e is not None:
        page_title = page_title.replace("№", str(e))

    return page_title


async def make_users_list(users_page: list) -> str:
    if len(users_page) == 0:
        text_list = phrases['err_empty_list']
        return text_list

    text_list = ''

    for (user_id, username, status) in users_page:
        if status > 0:
            text_list += f'<b>' \
                         f'<code>{str(user_id).ljust(12)}</code>👸 @{username}' \
                         f'</b>\n'
        elif status < 0:
            text_list += f'<strike>' \
                         f'<code>{str(user_id).ljust(12)}</code>@{username}' \
                         f'</strike>\n'
        else:
            text_list += f'<code>{str(user_id).ljust(12)}</code>@{username}\n'

    return text_list


async def make_bugs_list(bugs_page: list) -> str:
    if len(bugs_page) == 0:
        text_list = phrases['err_empty_list']
        return text_list

    text_list = ''

    for (bug_id, user_id, _, preset_id, description, status) in bugs_page:
        username = users.get_username(user_id)
        user_preset = presets.get_from_id(preset_id)

        if status > 0:
            text_list += f'✅ <code>{bug_id} </code><i>{", ".join(user_preset)}</i>\n' \
                         f'<blockquote>{description}</blockquote>' \
                         f'<code>{str(user_id).ljust(12)}</code>@{username}\n\n'
        else:
            text_list += f'<code>{bug_id} </code><i>{", ".join(user_preset)}</i>\n' \
                         f'<blockquote>{description}</blockquote>' \
                         f'<code>{str(user_id).ljust(12)}</code>@{username}\n\n'

    return text_list


async def split_list2page(list_pages: list, max_number: int, page_number: int = 1) -> Tuple[list, int]:
    start_index = (page_number - 1) * max_number
    end_index = start_index + max_number

    if start_index < 0 or start_index >= len(list_pages):
        return [], 1

    return list_pages[start_index:end_index], ceil(len(list_pages) / max_number)


@rt.message(Command(commands='root'), IsAdmin())  # /root
async def cmd_demote(message: Message):
    users.demote(message.from_user.id)
    await message.answer(phrases['dem_admin'])


@rt.message(Command(commands='root'))  # /root
async def cmd_promote(message: Message):
    password = await get_cmd_args(message)
    if password[0] == PASSWORD:
        users.promote(message.from_user.id)
        await message.answer(phrases['new_admin'])


@rt.message(Command(commands='get_phrases'), IsAdmin())  # /get_phrases
async def cmd_get_phrases(message: Message):
    for phrase in phrases.keys():
        await message.answer(f'<b>{phrase}</b>')
        await message.answer(str(phrases[phrase]))
    await message.answer(f'<b>/getcoms</b>')
    await cmd_getcoms(message)


@rt.message(Command(commands='get_users'), IsAdmin())  # /get_users
async def cmd_get_users(message: Message):
    users_page, count_pages = await split_list2page(users.get_all(), PAGE_SIZE_USER, 1)

    text_message = await make_page_title('users_page_title', 1, count_pages)
    text_message += await make_users_list(users_page)
    users_kb = await kb.make_pages_kb(1, count_pages, 'users')

    await message.answer(text_message, reply_markup=users_kb)


@rt.message(Command(commands='get_admins'), IsAdmin())  # /get_admins
async def cmd_get_admins(message: Message):
    admins_page, count_pages = await split_list2page(users.get_admins(), PAGE_SIZE_USER, 1)

    text_message = await make_page_title('admins_page_title', 1, count_pages)
    text_message += await make_users_list(admins_page)
    admins_kb = await kb.make_pages_kb(1, count_pages, 'admins')

    await message.answer(text_message, reply_markup=admins_kb)


@rt.message(Command(commands='get_bugs'), IsAdmin())  # /get_bugs
async def cmd_get_bugs(message: Message):
    fix_count, all_count = bugs.stat()
    bugs_page, count_pages = await split_list2page(bugs.get_all(), PAGE_SIZE_BUG, 1)

    text_message = await make_page_title('bugs_page_title', 1, count_pages, fix_count, all_count)
    text_message += await make_bugs_list(bugs_page)
    bugs_kb = await kb.make_pages_kb(1, count_pages, 'bugs')

    await message.answer(text_message, reply_markup=bugs_kb)


@rt.message(Command(commands='get_fixs'), IsAdmin())  # /get_fixs
async def cmd_get_fixs(message: Message):
    fixs_page, count_pages = await split_list2page(bugs.get_fix(), PAGE_SIZE_BUG, 1)

    text_message = await make_page_title('fixs_page_title', 1, count_pages)
    text_message += await make_bugs_list(fixs_page)
    fixs_kb = await kb.make_pages_kb(1, count_pages, 'fixs')

    await message.answer(text_message, reply_markup=fixs_kb)


@rt.message(Command(commands='get_user_bugs'), IsAdmin())  # /get_user_bugs
async def cmd_get_user_bugs(message: Message):
    user_id = await get_cmd_user_id(message)

    if user_id == -1:
        return

    username = users.get_username(user_id)
    fix_count, all_count = bugs.stat_from_user(user_id)
    userbugs_page, count_pages = await split_list2page(bugs.get_from_user(user_id), PAGE_SIZE_BUG, 1)

    text_message = await make_page_title('userbugs_page_title', 1, count_pages, fix_count, all_count, username)
    text_message += await make_bugs_list(userbugs_page)
    userbugs_kb = await kb.make_pages_kb(1, count_pages, f'userbugs-{user_id}')

    await message.answer(text_message, reply_markup=userbugs_kb)


@rt.callback_query(F.data.startswith('goto_page_'))
async def call_goto_page_users(callback: CallbackQuery):
    await callback.answer()

    split_callback = callback.data.split('_')

    type_of_page = split_callback[2]
    page_number = int(split_callback[-1])
    fix_count = None
    all_count = None
    username = None
    page_list = []

    if type_of_page in ['users', 'admins']:
        page_size = PAGE_SIZE_USER
    else:
        page_size = PAGE_SIZE_BUG

    if type_of_page == 'users':
        page_list = users.get_all()
    elif type_of_page == 'admins':
        page_list = users.get_admins()
    elif type_of_page == 'bugs':
        fix_count, all_count = bugs.stat()
        page_list = bugs.get_all()
    elif type_of_page == 'fixs':
        page_list = bugs.get_fix()
    elif 'userbugs' in type_of_page:
        user_id = int(type_of_page.split("-")[1])
        username = users.get_username(user_id)
        fix_count, all_count = bugs.stat_from_user(user_id)
        page_list = bugs.get_from_user(user_id)

    page, count_pages = await split_list2page(page_list, page_size, page_number=page_number)
    text_message = await make_page_title(f'{type_of_page.split("-")[0]}_page_title', page_number, count_pages, fix_count, all_count, username)

    if type_of_page in ['users', 'admins']:
        text_message += await make_users_list(page)
    else:
        text_message += await make_bugs_list(page)

    page_kb = await kb.make_pages_kb(page_number, count_pages, type_of_page)
    await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=text_message, reply_markup=page_kb)


@rt.message(Command(commands='get_bug'), IsAdmin())  # /get_bug
async def cmd_get_bug(message: Message):
    bug_id = await get_cmd_bug_id(message)
    if bug_id == -1:
        return

    _, user_id, message_id, preset_id, _, _ = bugs.get_from_id(bug_id)
    user_preset = presets.get_from_id(preset_id)

    text_message = '<i>' + '\n'.join(user_preset) + '</i>'

    await message.answer(text_message)

    await bot.forward_message(
        chat_id=message.chat.id,
        from_chat_id=user_id,
        message_id=message_id)


@rt.message(Command(commands='del_bug'), IsAdmin())  # /del_bug
async def cmd_del_bug(message: Message):
    bug_id = await get_cmd_bug_id(message)
    if bug_id == -1:
        return
    bugs.delete(bug_id)
    await message.answer(phrases['del_bug'])


@rt.message(Command(commands='fix_bug'), IsAdmin())  # /fix_bug
async def cmd_del_bug(message: Message):
    bug_id = await get_cmd_bug_id(message)
    if bug_id == -1:
        return

    bugs.upd_status(bug_id)
    _, user_id, message_id, _, _, status = bugs.get_from_id(bug_id)

    if status == 1:
        await message.answer(phrases['fixed_bug'])

        await bot.send_message(user_id,
                               phrases['fix_bug'],
                               reply_to_message_id=message_id)

    else:
        await message.answer(phrases['unfixed_bug'])


@rt.message(Command(commands='getcoms'), IsSuperAdmin())  # /getcoms
async def cmd_getcoms(message: Message):
    await message.answer(
        "<b>Посмотреть</b>\n"
        "/get_users — пользователей\n"
        "/get_admins — админов\n"
        "/get_phrases — фразы бота\n"
        "/get_bugs — все баги\n"
        "/get_fixs — только те баги, которые нужно исправить\n"
        "/get_user_bugs {id пользователя} — баги пользователя\n"
        "/get_bug {id бага} — баг\n\n"
        "<b>Сделать</b>\n"
        "/fix_bug {id бага} — поменять состояние бага\n"
        "/del_bug {id бага} — удалить баг\n"
        "/banana {id пользователя} — забанить пользователя\n"
        "/kiss {id пользователя} — удалить админа\n\n"
        "<b>Прочее</b>\n"
        "/getcoms — посмотреть команды (Это сообщение)\n"
        "/root — уйти из админов\n"
    )


@rt.message(Command(commands='getcoms'), IsAdmin())  # /getcoms
async def cmd_getcoms(message: Message):
    await message.answer(
        "<b>Посмотреть</b>\n"
        "/get_users — пользователей\n"
        "/get_admins — админов\n"
        "/get_bugs — все баги\n"
        "/get_fixs — только те баги, которые нужно исправить\n"
        "/get_user_bugs {id пользователя} — баги пользователя\n"
        "/get_bug {id бага} — баг\n\n"
        "<b>Сделать</b>\n"
        "/fix_bug {id бага} — поменять состояние бага\n"
        "/del_bug {id бага} — удалить баг\n"
        "/banana {id пользователя} — забанить пользователя\n"
        "<b>Прочее</b>\n"
        "/getcoms — посмотреть команды (Это сообщение)\n\n"
        "/root — уйти из админов\n"
    )


@rt.message(Command(commands='kiss'), IsSuperAdmin())  # /kiss
async def scmd_demote(message: Message):
    user_id = await get_cmd_user_id(message)

    if user_id == -1:
        return

    if not await IsAdmin.check(user_id):
        await message.answer(phrases['err_user_not_admin'])
        return

    users.demote(user_id)
    await bot.send_message(chat_id=user_id, text=phrases["kiss_admin"])
    await message.answer(phrases["del_admin"])


@rt.message(Command(commands='banana'), IsSuperAdmin())  # /banana
async def scmd_ban(message: Message):
    user_id = await get_cmd_user_id(message)

    if user_id == -1:
        return

    users.ban(user_id)
    ban_kb = await kb.make_clear_kb(user_id)
    await message.answer(phrases["ban_user"], reply_markup=ban_kb)


@rt.message(Command(commands='banana'), IsAdmin())  # /banana
async def cmd_ban(message: Message):
    user_id = await get_cmd_user_id(message)

    if user_id == -1:
        return

    if await IsAdmin.check(user_id):
        await message.answer(phrases['err_user_admin'])
        return

    users.ban(user_id)
    ban_kb = await kb.make_clear_kb(user_id)
    await message.answer(phrases["ban_user"], reply_markup=ban_kb)


@rt.callback_query(F.data.startswith('clear_user_'))
async def call_clear_user(callback: CallbackQuery):
    await callback.answer()
    user_id = int(callback.data.replace('clear_user_', ''))
    presets.delete_from_user(user_id)
    bugs.delete_from_user(user_id)
