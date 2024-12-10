from init_config import *

MAX_NUMBER_BUTTON = 24


site = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=phrases['button_site'], url='http://kfprod.ru/all-pages')]
    ]
)

preset = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=phrases['button_cancel'], callback_data='cancel')
        ]
    ]
)

fill_preset = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=phrases['button_system'], callback_data='goto_preset_system'),
            InlineKeyboardButton(text=phrases['button_device'], callback_data='goto_preset_device'),
            InlineKeyboardButton(text=phrases['button_browser'], callback_data='goto_preset_browser')
        ],
        [
            InlineKeyboardButton(text=phrases['button_cancel'], callback_data='cancel'),
            InlineKeyboardButton(text=phrases['button_save'], callback_data='end_fill_preset')]
    ]
)

no_presets = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=phrases['button_cancel'], callback_data='cancel'),
            InlineKeyboardButton(text=phrases['button_fill_preset'], callback_data='start_fill_preset')
        ]
    ]
)


async def make_clear_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=phrases['button_clear'], callback_data=f'clear_user_{user_id}')
            ]
        ]
    )


async def make_pages_kb(page: int, max_page: int, name: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    past_page = page - 1
    next_page = page + 1

    if past_page != 0:
        kb.button(text=phrases['button_past'], callback_data=f'goto_page_{name}_{past_page}')
    if page < max_page:
        kb.button(text=phrases['button_next'], callback_data=f'goto_page_{name}_{next_page}')
    return kb.adjust(2).as_markup(resize_keyboard=True)


async def make_presets_kb(presets: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    for pst in presets:
        kb.button(text=f'{pst[2]}, {pst[3]}, {pst[4]}',
                  callback_data=f'preset_{pst[0]}')

    if len(presets) + 1 < MAX_NUMBER_BUTTON:
        kb.button(text=phrases['button_new_preset'], callback_data='start_fill_preset')

    kb.button(text=phrases['button_cancel'], callback_data='cancel')
    adjust_value = ceil((len(presets) + 1) / 8)

    return kb.adjust(adjust_value).as_markup(resize_keyboard=True)


async def make_del_presets_kb(presets: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for pst in presets:
        kb.button(text=f'{pst[2]}, {pst[3]}, {pst[4]}',
                  callback_data=f'del_preset_{pst[0]}')

    adjust_value = ceil(len(presets) / 8)

    return kb.adjust(adjust_value).as_markup(resize_keyboard=True)
