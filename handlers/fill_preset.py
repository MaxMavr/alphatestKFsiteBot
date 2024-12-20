from config import *

rt: Router = Router()

MAX_NUMBER_CHAR = 80


async def check_state(message: Message = None,
                      callback: CallbackQuery = None,
                      state: FSMContext = None) -> bool:

    data = await state.get_data()

    if not data.get('bug_messages'):
        if callback:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text=phrases['err_end_session'],
                reply_markup=None
            )

        elif message:
            await message.answer(phrases['err_end_session'],
                                 reply_markup=None)
        return False

    return True


async def send_bug(messages: List[Message], preset_id: int):
    description = ''

    if messages[0].video:
        description += '📼 '
    if messages[0].audio:
        description += '🗣 '
    if messages[0].video_note:
        description += '📼 '
    if messages[0].document:
        description += '📄 '
    if messages[0].voice:
        description += '🗣 '
    if messages[0].photo:
        description += '📷 '
    if messages[0].media_group_id:
        description += '📷📼🗣 '

    msg_text = messages[0].caption if messages[0].caption else messages[0].text

    if msg_text:
        description += msg_text[:MAX_NUMBER_CHAR]

        if len(msg_text) > MAX_NUMBER_CHAR:
            description += '...'

    msgs_id = []
    for msg in messages:
        msgs_id.append(msg.message_id)
    msgs_id = dumps(msgs_id)

    bugs.add(
        user_id=messages[0].chat.id,
        messages_id=msgs_id,
        preset_id=preset_id,
        description=description
    )

    await messages[0].answer(phrases['add_bug'])


async def show_preset(state: FSMContext) -> None:
    cur_state = await state.get_state()
    data = await state.get_data()
    edit_message_id = data.get('edit_message_id')
    edit_chat_id = data.get('edit_chat_id')
    system = data.get('system')
    device = data.get('device')
    browser = data.get('browser')

    state_status = cur_state.replace('Preset:', '')

    if None in [system, device, browser]:
        edit_kb = kb.preset
        text_message = phrases['filling_presets']
        text_message += phrases[f'example_{state_status}']
    else:
        edit_kb = kb.fill_preset
        text_message = phrases['fill_presets']

    system = '' if not system else system
    device = '' if not device else device
    browser = '' if not browser else browser

    if state_status == 'system':
        text_message += phrases['select_system'] + f'{system}\n'
    else:
        text_message += phrases['no_select_system'] + f'{system}\n'

    if state_status == 'device':
        text_message += phrases['select_device'] + f'{device}\n'
    else:
        text_message += phrases['no_select_device'] + f'{device}\n'

    if state_status == 'browser':
        text_message += phrases['select_browser'] + f'{browser}\n'
    else:
        text_message += phrases['no_select_browser'] + f'{browser}\n'

    if '' in [system, device, browser]:
        await bot.edit_message_text(
            chat_id=edit_chat_id,
            message_id=edit_message_id,
            text=text_message,
            reply_markup=edit_kb
        )
    else:
        await bot.delete_message(
            chat_id=edit_chat_id,
            message_id=edit_message_id
        )

        message = await bot.send_message(
            chat_id=edit_chat_id,
            text=text_message,
            reply_markup=edit_kb
        )

        await state.update_data(edit_message_id=message.message_id)


@rt.callback_query(F.data == 'start_fill_preset')
async def start_fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    if not await check_state(callback=callback, state=state):
        return

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
    await message.answer(phrases['put_system'])
    await state.set_state(Preset.device)
    await show_preset(state)


@rt.message(Preset.device)
async def fill_preset(message: Message, state: FSMContext):
    await state.update_data(device=message.text)
    await message.answer(phrases['put_device'])
    await state.set_state(Preset.browser)
    await show_preset(state)


@rt.message(Preset.browser)
async def fill_preset(message: Message, state: FSMContext):
    await state.update_data(browser=message.text)
    await message.answer(phrases['put_browser'])
    await state.set_state(Preset.system)
    await show_preset(state)


@rt.callback_query(F.data.startswith('goto_preset_'))
async def fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    if not await check_state(callback=callback, state=state):
        return

    goto_status = callback.data.replace('goto_preset_', '')

    await state.set_state(preset_status[goto_status])
    await show_preset(state)


@rt.callback_query(F.data == 'end_fill_preset')
async def end_fill_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    if not await check_state(callback=callback, state=state):
        return

    data = await state.get_data()
    edit_message_id = data.get('edit_message_id')
    bug_messages: List[Message] = data.get('bug_messages')
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

    await send_bug(bug_messages, preset_id)

    await bot.edit_message_text(
        chat_id=edit_chat_id,
        message_id=edit_message_id,
        text=text_message,
        reply_markup=None
    )


@rt.callback_query(F.data.startswith('preset_'))
async def call_preset(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    if not await check_state(callback=callback, state=state):
        return

    preset_id = int(callback.data.replace('preset_', ''))
    data = await state.get_data()
    bug_messages: List[Message] = data.get('bug_messages')
    await state.clear()

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=callback.message.text,
        reply_markup=None
    )

    await send_bug(bug_messages, preset_id)
