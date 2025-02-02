from config import *
rt: Router = Router()


@rt.message(F.content_type.in_({ContentType.TEXT,
                                ContentType.PHOTO,
                                ContentType.AUDIO,
                                ContentType.VOICE,
                                ContentType.VIDEO,
                                ContentType.DOCUMENT,
                                ContentType.VIDEO_NOTE}))
async def catch_bug(message: Message, state: FSMContext):

    is_sug = False
    if message.text:
        is_sug = '#sug' in message.text
    if message.caption:
        is_sug = '#sug' in message.caption

    if is_sug:
        await message.answer(phrases['sug'])
        await message.forward(MAIN_ADMIN_ID)
        return

    data = await state.get_data()
    bug_messages: List[Message] = data.get('bug_messages')

    if not bug_messages:
        user_presets = presets.get_from_user(message.from_user.id)
        await state.update_data(bug_messages=[message])

        if len(user_presets) == 0:
            await message.reply(f"{phrases['no_presets']}", reply_markup=kb.no_presets)
        else:
            kb_have_presets = await kb.make_presets_kb(user_presets)
            await message.reply(f"{phrases['have_presets']}", reply_markup=kb_have_presets)
        return

    if message.media_group_id == bug_messages[0].media_group_id:
        await state.update_data(bug_messages.append(message))
