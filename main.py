from config import *


'''
Команды для обычных пользователей
'''


@dp.message(CommandStart())  # /start
async def cmd_start(message: Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer(text=phrases["start"])


@dp.message(Isban())
async def catch_text(message: Message):
    await ban_msg(message)


@dp.message(Command(commands='about'))  # /about
async def cmd_about(message: Message):
    await message.answer(phrases["about"])


@dp.message(Command(commands='help'))  # /help
async def cmd_help(message: Message):
    await message.answer(phrases["help"])


@dp.message(Command(commands='alpha'))  # /alpha
async def cmd_help(message: Message):
    await message.answer(phrases["alpha"])


# async def edit_msg(user_id: int, msg_id: int, msg: str):
#     space = await search_phrase(msg)
#
#     if space is not None:
#         await bot.edit_message_text(chat_id=user_id,
#                                     message_id=msg_id,
#                                     disable_web_page_preview=True,
#                                     text=await make_msg(space),
#                                     reply_markup=await make_inline_kb(space['kb']))
#     else:
#         await bot.edit_message_text(chat_id=user_id,
#                                     message_id=msg_id,
#                                     text=F"Поле {msg + ' ' if msg.isdigit() else ''}не найдено!")
#
#
# @dp.callback_query(Callback())
# async def fill_preset(callback: CallbackQuery, state: FSMContext):
#     await callback.answer()
#     await state.set_state(Preset.system)
#     await bot.send_message(callback.from_user.id, 'Заполним пресет настроек\n'
#                                                   '<code>'
#                                                   '> <b>Система</b>: \n'
#                                                   '  Устройство: \n'
#                                                   '  Браузер: '
#                                                   '</code>')
#
#
# @dp.message(state=Preset.system)
# async def process_color(message: Message, state: FSMContext):
#     user_color = message.text
#     await state.update_data(color=user_color)  # Сохраняем ответ
#     await Preset.  # Переходим к следующему вопросу
#     await message.reply("Какое ваше любимое животное?")  # Задаём второй вопрос
#
#
# @dp.message_handler(state=Form.waiting_for_animal)
# async def process_animal(message: types.Message, state: FSMContext):
#     user_animal = message.text
#     await state.update_data(animal=user_animal)  # Сохраняем ответ
#     await Form.next()  # Переходим к следующему вопросу
#     await message.reply("Какое ваше любимое блюдо?")  # Задаём третий вопрос
#
# @dp.message_handler(state=Form.waiting_for_food)
# async def process_food(message: types.Message, state: FSMContext):
#     user_food = message.text
#     await state.update_data(food=user_food)  # Сохраняем ответ
#
#     # Получаем все данные
#     data = await state.get_data()
#     color = data.get('color')
#     animal = data.get('animal')
#     food = data.get('food')
#
#     await message.reply(f"Спасибо за заполнение формы! 🎉\n"
#                          f"Ваш любимый цвет: {color}\n"
#                          f"Ваше любимое животное: {animal}\n"
#                          f"Ваше любимое блюдо: {food}")
#
#     await state.finish()  # Завершаем состояние


'''
Команды для админов. 
'''


@dp.message(Command(commands='root'), Isadmin())  # /root
async def cmd_demote_admin(message: Message):
    upd_user_admin_status(message.from_user.id, 0)
    await message.answer(phrases['dem_admin'])


@dp.message(Command(commands='root'))  # /root
async def cmd_add_admin(message: Message):
    password = await get_cmd_args(message)

    if password[0] == PASSWORD:
        upd_user_admin_status(message.from_user.id, 1)
        await message.answer(phrases['new_admin'])


@dp.message(Command(commands='get_phrases'), Isadmin())  # /get_phrases
async def cmd_get_phrases(message: Message):
    for phrase in phrases.keys():
        await message.answer(f'<b>{phrase}</b>')
        await message.answer(phrases[phrase])
    await message.answer(f'<b>/getcoms</b>')
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
    userid = await get_cmd_id(message)

    if userid == -1:
        return

    if not Isadmin.check(userid):
        await message.answer(phrases['err_user_not_admin'])
        return

    upd_user_admin_status(userid, 0)
    await bot.send_message(chat_id=userid, text=phrases["kiss_admin"])
    await message.answer(phrases["del_admin"])


@dp.message(Command(commands='banana'), Issuperadmin())  # /banana
async def cmd_delete_admin(message: Message):
    userid = await get_cmd_id(message)

    if userid == -1:
        return

    upd_user_admin_status(userid, 0)
    upd_user_ban_status(userid, 1)
    await message.answer(phrases["ban_user"])


@dp.message(Command(commands='banana'), Isadmin())  # /banana
async def cmd_delete_admin(message: Message):
    userid = await get_cmd_id(message)

    if userid == -1:
        return

    if Isadmin.check(userid):
        await message.answer(phrases['err_user_admin'])
        return

    upd_user_ban_status(userid, 1)
    await message.answer(phrases["ban_user"])


@dp.message(F.text, Isadmin())
async def catch_admin_text(message: Message):
    await message.answer(phrases['default_answers_admin'])


@dp.message(F.content_type.in_({ContentType.TEXT,
                                ContentType.PHOTO,
                                ContentType.VOICE,
                                ContentType.VIDEO}))
async def catch_default(message: Message):
    presets = get_presets_from_user(message.from_user.id)

    print(presets)

    if len(presets) == 0:
        await message.reply(f"{phrases['no_presets']}", reply_markup=kb.no_presets)


@dp.message(F.text)
async def catch_text(message: Message):
    presets = get_presets_from_user(message.from_user.id)

    print(presets)

    if len(presets) == 0:
        await message.reply(f"{phrases['no_presets']}", reply_markup=kb.no_presets)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Погнали ловить баги!")
    asyncio.run(main())