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
    data = await state.get_data()
    bug_message: Message = data.get('bug_message')

    if bug_message is None:
        user_presets = presets.get_from_user(message.from_user.id)
        await state.update_data(bug_message=message)

        if len(user_presets) == 0:
            await message.reply(f"{phrases['no_presets']}", reply_markup=kb.no_presets)
        else:
            kb_have_presets = await kb.make_presets_kb(user_presets)
            await message.reply(f"{phrases['have_presets']}", reply_markup=kb_have_presets)
