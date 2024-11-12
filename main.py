from config import *


'''
Команды для обычных пользователей
'''


@dp.message(Isban())
async def catch_text(message: Message):
    await ban_msg(message)


@dp.message(CommandStart())  # /start
async def cmd_start(message: Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer(text=phrases["start"])


@dp.message(Command(commands='about'))  # /about
async def cmd_about(message: Message):
    await message.answer(phrases["about"])


@dp.message(Command(commands='help'))  # /help
async def cmd_help(message: Message):
    await message.answer(phrases["help"])


'''
Команды для админов. 
'''


@dp.message(Command(commands='root'), Isadmin())  # /root
async def cmd_demote_admin(message: Message):
    update_user_admin_status(message.from_user.id, 0)
    await message.answer(phrases['dem_admin'])


@dp.message(Command(commands='root'))  # /root
async def cmd_add_admin(message: Message):
    password = await take_command_arguments(message)

    if password[0] == PASSWORD:
        update_user_admin_status(message.from_user.id, 1)
        await message.answer(phrases['new_admin'])
    else:
        await message.answer('угцрркуципркуип')


@dp.message(Command(commands='get_phrases'), Isadmin())  # /get_phrases
async def cmd_get_phrases(message: Message):
    for phrase in phrases.keys():
        await message.answer(f'<b>{phrase}</b>')
        await message.answer(phrases[phrase])
    await message.answer(f'/getcoms')
    await cmd_getcoms(message)


@dp.message(Command(commands='getcoms'), Isadmin())  # /getcoms
async def cmd_getcoms(message: Message):
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


@dp.message(Command(commands='kiss'), Issuperadmin())  # /kiss
async def cmd_delete_admin(message: Message):
    userid = await check_command_to_id(message)

    if userid == -1:
        return

    if not Isadmin.check(userid):
        await message.answer(phrases['err_user_not_admin'])
        return

    update_user_admin_status(userid, 0)
    await bot.send_message(chat_id=userid, text=phrases["fuck_admin"])
    await message.answer(phrases["del_admin"])


@dp.message(Command(commands='banana'), Issuperadmin())  # /banana
async def cmd_delete_admin(message: Message):
    userid = await check_command_to_id(message)

    if userid == -1:
        return

    update_user_admin_status(userid, 0)
    update_user_ban_status(userid, 1)
    await message.answer(phrases["ban_user"])


@dp.message(Command(commands='banana'), Isadmin())  # /banana
async def cmd_delete_admin(message: Message):
    userid = await check_command_to_id(message)

    if userid == -1:
        return

    if Isadmin.check(userid):
        await message.answer(phrases['err_user_admin'])
        return

    update_user_ban_status(userid, 1)
    await message.answer(phrases["ban_user"])


@dp.message(F.text, Isadmin())
async def catch_admin_text():
    await default_msg(phrases['default_answers_admin'])


@dp.message(F.text)
async def catch_text(message: Message):
    await default_msg(message)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Погнали ловить баги!")
    asyncio.run(main())