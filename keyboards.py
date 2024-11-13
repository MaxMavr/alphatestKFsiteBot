from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder


site = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ссылка на все страницы', url='kfprod.ru/all-pages')]
    ]
)

preset = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Система', callback_data='goto_preset_system'),
         InlineKeyboardButton(text='Устройство', callback_data='goto_preset_device'),
         InlineKeyboardButton(text='Браузер', callback_data='goto_preset_browser')]
    ]
)

fill_preset = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Система', callback_data='goto_preset_system'),
         InlineKeyboardButton(text='Устройство', callback_data='goto_preset_device'),
         InlineKeyboardButton(text='Браузер', callback_data='goto_preset_browser')],
        [InlineKeyboardButton(text='Сохранить', callback_data='end_fill_preset')]
    ]
)

no_presets = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Заполнить форму', callback_data='start_fill_preset')]
    ]
)


async def make_clear_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Очистить!', callback_data=f'clear_user_{user_id}')]
        ]
    )


async def make_pages_kb(past_pages: int, next_pages: int, name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if past_pages != 0:
        kb.button(text='< Прошлая', callback_data=f'past_{name}_{past_pages}')
    kb.button(text='Следующая >', callback_data=f'next_{name}_{next_pages}')
    return kb.adjust(2).as_markup(resize_keyboard=True)


async def make_presets_kb(presets: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for pst in presets:
        kb.button(text=f'{pst[2]}, {pst[3]}, {pst[4]}',
                  callback_data=f'preset_{pst[0]}')
    kb.button(text='Добавить форму', callback_data='start_fill_preset')
    return kb.adjust(1).as_markup(resize_keyboard=True)


async def make_del_presets_kb(presets: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for pst in presets:
        kb.button(text=f'{pst[2]}, {pst[3]}, {pst[4]}',
                  callback_data=f'del_preset_{pst[0]}')
    return kb.adjust(1).as_markup(resize_keyboard=True)
