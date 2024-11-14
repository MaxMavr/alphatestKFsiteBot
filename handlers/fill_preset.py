from config import *
rt: Router = Router()


MAX_NUMBER_CHAR = 80


async def send_bug(message: Message, preset_id: int,):
    description = message.caption if message.text is None else message.text

    if description is None:
        description = 'Нема'
    else:
        if len(description) > MAX_NUMBER_CHAR:
            description = description[:MAX_NUMBER_CHAR] + '...'

    bugs.add(
        user_id=message.chat.id,
        message_id=message.message_id,
        preset_id=preset_id,
        description=description
    )

    await message.answer(phrases['add_bug'])


async def show_preset(state: FSMContext) -> None:
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

    await bot.edit_message_text(
        chat_id=edit_chat_id,
        message_id=edit_message_id,
        text=text_message,
        reply_markup=edit_kb
    )


@rt.callback_query(F.data == 'start_fill_preset')
async def start_fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Preset.system)

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=callback.message.text,
        reply_markup=None
    )

    message = await bot.send_message(callback.from_user.id, phrases['empty_presets'], reply_markup=kb.preset)
    await state.update_data(edit_message_id=message.message_id)
    await state.update_data(edit_chat_id=message.chat.id)


@rt.message(Preset.system)
async def fill_preset(message: Message, state: FSMContext):
    await state.update_data(system=message.text)
    await state.set_state(Preset.device)
    await show_preset(state)


@rt.message(Preset.device)
async def fill_preset(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await state.set_state(Preset.browser)
    await show_preset(state)


@rt.message(Preset.browser)
async def fill_preset(message: Message, state: FSMContext):
    await state.update_data(browser=message.text)
    await state.set_state(Preset.system)
    await show_preset(state)


@rt.callback_query(F.data == 'goto_preset_system')
async def fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Preset.system)
    await show_preset(state)


@rt.callback_query(F.data == 'goto_preset_device')
async def fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Preset.device)
    await show_preset(state)


@rt.callback_query(F.data == 'goto_preset_browser')
async def fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Preset.browser)
    await show_preset(state)


@rt.callback_query(F.data == 'end_fill_preset')
async def end_fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    edit_message_id = data.get('edit_message_id')
    bug_message: Message = data.get('bug_message')
    edit_chat_id = data.get('edit_chat_id')
    system = data.get('system')
    device = data.get('device')
    browser = data.get('browser')
    await state.clear()

    text_message = f'<b>Сохранили форму</b>\n\n' \
                   f'    Система {system}\n' \
                   f'    Устройство {device}\n' \
                   f'    Браузер {browser}\n'
    preset_id = presets.add(callback.from_user.id, system, device, browser)

    await send_bug(bug_message, preset_id)

    await bot.edit_message_text(
        chat_id=edit_chat_id,
        message_id=edit_message_id,
        text=text_message,
        reply_markup=None
    )


@rt.callback_query(F.data.startswith('preset_'))
async def call_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    preset_id = int(callback.data.replace('preset_', ''))
    data = await state.get_data()
    bug_message: Message = data.get('bug_message')
    await state.clear()

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=callback.message.text,
        reply_markup=None
    )

    await send_bug(bug_message, preset_id)
