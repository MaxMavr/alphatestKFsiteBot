from config import *
rt: Router = Router()


@rt.message(F.content_type.in_({ContentType.TEXT,
                                ContentType.PHOTO,
                                ContentType.VOICE,
                                ContentType.VIDEO}))
async def catch_bug(message: Message):
    user_presets = presets.get_from_user(message.from_user.id)

    if user_presets is None:
        await message.reply(f"{phrases['no_presets']}", reply_markup=kb.no_presets)
    else:
        kb_have_presets = await kb.make_presets_kb(user_presets)
        await message.reply(f"{phrases['have_presets']}", reply_markup=kb_have_presets)
