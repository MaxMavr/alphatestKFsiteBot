from config import *
rt: Router = Router()


@rt.message(CommandStart())  # /start
async def cmd_start(message: Message):
    if users.add(message.from_user.id, message.from_user.username):
        await message.answer(text=phrases["start"])


@rt.message(IsBaned())
async def catch_ban(message: Message):
    await ban_message(message)


@rt.message(Command(commands='about'))  # /about
async def cmd_about(message: Message):
    await message.answer(phrases["about"])


@rt.message(Command(commands='help'))  # /help
async def cmd_help(message: Message):
    await message.answer(phrases["help"])


@rt.message(Command(commands='alpha'))  # /alpha
async def cmd_alpha(message: Message):
    await message.answer(phrases["alpha"], reply_markup=kb.site)
    await message.answer(''.join(phrases["q&a"]))


@rt.message(Command(commands='del_form'))  # /del_form
async def cmd_del_form(message: Message):
    user_presets = presets.get_from_user(message.from_user.id)
    kb_del_presets = await kb.make_del_presets_kb(user_presets)

    if len(user_presets) == 0:
        text_message = phrases['del_presets_none']
    elif len(user_presets) == 1:
        text_message = phrases['del_presets_one']
    else:
        text_message = phrases['del_presets']

    await message.answer(text_message, reply_markup=kb_del_presets)


@rt.callback_query(F.data.startswith('del_preset_'))
async def call_del_preset(callback: CallbackQuery):
    await callback.answer()
    preset_id = int(callback.data.replace('del_preset_', ''))
    presets.hide(preset_id)

    user_presets = presets.get_from_user(callback.from_user.id)
    kb_del_presets = await kb.make_del_presets_kb(user_presets)

    if len(user_presets) == 0:
        text_message = phrases['del_presets_null']
    elif len(user_presets) == 1:
        text_message = phrases['del_presets_one']
    else:
        text_message = phrases['del_presets']

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=text_message,
        reply_markup=kb_del_presets
    )


@rt.callback_query(F.data == 'cancel')
async def call_cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text=phrases['cancel'],
        reply_markup=None
    )
