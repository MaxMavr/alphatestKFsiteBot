from config import *
rt: Router = Router()


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
        await message.answer(phrases[phrase])
    await message.answer(f'<b>/getcoms</b>')
    await cmd_getcoms(message)


@rt.message(Command(commands='get_users'), IsAdmin())  # /get_users
async def cmd_get_users(message: Message):
    all_users = users.get_all()
    # Todo Сделать страницы и красивое отображение
    await message.answer(str(all_users))


@rt.message(Command(commands='get_admins'), IsAdmin())  # /get_users
async def cmd_get_admins(message: Message):
    admins = users.get_admins()
    # Todo Сделать страницы и красивое отображение
    await message.answer(str(admins))


@rt.message(Command(commands='get_bugs'), IsAdmin())  # /get_bugs
async def cmd_get_bugs(message: Message):
    fix_count, all_count = bugs.stat()
    all_bugs = bugs.get_all()
    # Todo Сделать страницы и красивое отображение
    await message.answer(str(fix_count))
    await message.answer(str(all_count))
    await message.answer(str(all_bugs))


@rt.message(Command(commands='get_fixs'), IsAdmin())  # /get_fixs
async def cmd_get_fixs(message: Message):
    fix_bugs = bugs.get_fix()
    # Todo Сделать страницы и красивое отображение
    await message.answer(str(fix_bugs))


@rt.message(Command(commands='get_user_bugs'), IsAdmin())  # /get_user_bugs
async def cmd_get_user_bugs(message: Message):
    user_id = await get_cmd_user_id(message)
    # Todo Сделать страницы и красивое отображение
    if user_id == -1:
        return

    fix_count, all_count = bugs.stat_from_user(user_id)
    user_bugs = bugs.get_from_user(user_id)
    await message.answer(str(fix_count))
    await message.answer(str(all_count))
    await message.answer(str(user_bugs))


@rt.message(Command(commands='get_bug'), IsAdmin())  # /get_bug
async def cmd_get_bug(message: Message):
    bug_id = await get_cmd_bug_id(message)
    # Todo Сделать страницы и красивое отображение
    if bug_id == -1:
        return

    bug = bugs.get_from_id(bug_id)

    await bot.forward_message(chat_id=message.chat.id, from_chat_id=message.chat.id, message_id=message.message_id)

    await message.answer(str(bug))


@rt.message(Command(commands='del_bug'), IsAdmin())  # /del_bug
async def cmd_del_bug(message: Message):
    bug_id = await get_cmd_bug_id(message)
    if bug_id == -1:
        return
    bugs.delete(bug_id)
    await message.answer(phrases['del_bug'])


@rt.message(Command(commands='getcoms'), IsAdmin())  # /getcoms
async def cmd_getcoms(message: Message):
    # Todo Заполнить

    await message.answer(
        "<b>Посмотреть</b>\n"
        "/getusers — пользователей\n"
        "/circleID {id} — кружок по АйДишнику\n\n"
        "<b>Работа с багами</b>\n"
        "/getcoms — посмотреть команды (Это сообщение)\n\n"
        "<b>Для плебса</b>\n"
        "/start — старт, есть старт\n"
        "/about — информация о боте\n"
        "/help — как пользоваться\n"
        "/morfinizm — команда для работяг, отправляющая в чатик рандомный видик\n\n"
        "<i>Регистр для всех команд важен.\n"
        "Советую закрепить это сообщение, а не постоянно писать.\n"
        "Все ID и HASH кликабельны (Если они написаны моноширинным)</i>"
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
