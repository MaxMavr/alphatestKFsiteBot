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
    await message.answer(phrases["alpha"], reply_markup=kb.site)


@dp.message(Command(commands='del_form'))  # /del_form
async def cmd_del_form(message: Message):
    presets = get_presets_from_user(message.from_user.id)
    kb_del_presets = await kb.make_del_presets_kb(presets)
    await message.answer(phrases['del_presets'], reply_markup=kb_del_presets)


async def show_preset(state: FSMContext) -> Message:
    cur_state = await state.get_state()
    data = await state.get_data()
    edit_message_id = data.get('edit_message_id')
    edit_chat_id = data.get('edit_chat_id')
    system = data.get('system')
    device = data.get('device')
    browser = data.get('browser')

    if None in [system, device, browser]:
        edit_kb = kb.preset
        text_message = phrases['filling_presets']
    else:
        edit_kb = kb.fill_preset
        text_message = phrases['fill_presets']

    if cur_state == 'Preset:system':
        text_message += f'▶️ <b>Система</b> {"" if system is None else system}\n'
    else:
        text_message += f'    Система {"" if system is None else system}\n'

    if cur_state == 'Preset:device':
        text_message += f'▶️ <b>Устройство</b> {"" if device is None else device}\n'
    else:
        text_message += f'    Устройство {"" if device is None else device}\n'

    if cur_state == 'Preset:browser':
        text_message += f'▶️ <b>Браузер</b> {"" if browser is None else browser}\n'
    else:
        text_message += f'    Браузер {"" if browser is None else browser}\n'

    return await bot.edit_message_text(
        chat_id=edit_chat_id,
        message_id=edit_message_id,
        text=text_message,
        reply_markup=edit_kb
    )


@dp.callback_query(F.data == 'add_preset')
async def fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Preset.system)

    message = await bot.send_message(callback.from_user.id, phrases['empty_presets'], reply_markup=kb.preset)
    await state.update_data(edit_message_id=message.message_id)
    await state.update_data(edit_chat_id=message.chat.id)


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
    userid = await get_cmd_user_id(message)

    if userid == -1:
        return

    if not await Isadmin.check(userid):
        await message.answer(phrases['err_user_not_admin'])
        return

    upd_user_admin_status(userid, 0)
    await bot.send_message(chat_id=userid, text=phrases["kiss_admin"])
    await message.answer(phrases["del_admin"])


@dp.message(Command(commands='banana'), Issuperadmin())  # /banana
async def cmd_delete_admin(message: Message):
    userid = await get_cmd_user_id(message)

    if userid == -1:
        return

    upd_user_admin_status(userid, 0)
    upd_user_ban_status(userid, 1)
    await message.answer(phrases["ban_user"])


@dp.message(Command(commands='banana'), Isadmin())  # /banana
async def cmd_delete_admin(message: Message):
    userid = await get_cmd_user_id(message)

    if userid == -1:
        return

    if await Isadmin.check(userid):
        await message.answer(phrases['err_user_admin'])
        return

    upd_user_ban_status(userid, 1)
    await message.answer(phrases["ban_user"])


# @dp.message(F.text, Isadmin())
# async def catch_admin_text(message: Message):
#     await message.answer(phrases['default_answers_admin'])


@dp.message(Preset.system)
async def fill_preset(message: Message, state: FSMContext):
    await state.update_data(system=message.text)
    await state.set_state(Preset.device)
    await show_preset(state)


@dp.message(Preset.device)
async def fill_preset(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(Preset.browser)
    await show_preset(state)


@dp.message(Preset.browser)
async def fill_preset(message: Message, state: FSMContext):
    await state.update_data(browser=message.text)
    await state.set_state(Preset.system)
    await show_preset(state)


@dp.callback_query(F.data == 'goto_system')
async def fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Preset.system)
    await show_preset(state)


@dp.callback_query(F.data == 'goto_device')
async def fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Preset.device)
    await show_preset(state)


@dp.callback_query(F.data == 'goto_browser')
async def fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Preset.browser)
    await show_preset(state)


@dp.callback_query(F.data == 'end_preset')
async def fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    edit_message_id = data.get('edit_message_id')
    edit_chat_id = data.get('edit_chat_id')
    system = data.get('system')
    device = data.get('device')
    browser = data.get('browser')
    await state.clear()

    text_message = f'<b>Сохранили форму</b>\n\n' \
                   f'    <b>Система</b> {data.get("system")}\n' \
                   f'    Устройство {data.get("device")}\n' \
                   f'    Браузер {data.get("browser")}\n'

    add_preset(callback.from_user.id, system, device, browser)
    presets = get_presets_from_user(callback.from_user.id)

    print(presets)

    await bot.edit_message_text(
        chat_id=edit_chat_id,
        message_id=edit_message_id,
        text=text_message,
        reply_markup=None
    )


@dp.callback_query(F.data.startswith('preset_'))
async def cmd_start(callback: CallbackQuery):
    await callback.answer()
    preset_id = int(callback.data.replace('preset_', ''))
    print(preset_id)


@dp.callback_query(F.data.startswith('del_preset'))
async def catch_del_preset(callback: CallbackQuery):
    await callback.answer()
    presets = get_presets_from_user(callback.from_user.id)
    preset_id = int(callback.data.replace('del_preset_', ''))
    del_preset(preset_id)

    kb_del_presets = await kb.make_del_presets_kb(presets)

    if len(presets) == 0:
        text_message = phrases['del_presets_null']
    elif len(presets) == 1:
        text_message = phrases['del_presets_one']
    else:
        text_message = phrases['del_presets']

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text_message,
        reply_markup=kb_del_presets
    )


@dp.message(F.content_type.in_({ContentType.TEXT,
                                ContentType.PHOTO,
                                ContentType.VOICE,
                                ContentType.VIDEO}))
async def catch_bug(message: Message):
    presets = get_presets_from_user(message.from_user.id)

    if presets is None:
        await message.reply(f"{phrases['no_presets']}", reply_markup=kb.no_presets)
    else:
        kb_have_presets = await kb.make_presets_kb(presets)
        await message.reply(f"{phrases['have_presets']}", reply_markup=kb_have_presets)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    print("Погнали ловить баги!")
    asyncio.run(main())
