from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardBuilder
from db_interface import get_presets_from_user


site = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ссылка на все страницы', url='kfprod.ru/all-pages')]
    ]
)

preset = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Система', callback_data='goto_system'),
         InlineKeyboardButton(text='Устройство', callback_data='goto_device'),
         InlineKeyboardButton(text='Браузер', callback_data='goto_browser')]
    ]
)

fill_preset = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Система', callback_data='goto_system'),
         InlineKeyboardButton(text='Устройство', callback_data='goto_device'),
         InlineKeyboardButton(text='Браузер', callback_data='goto_browser')],
        [InlineKeyboardButton(text='Сохранить', callback_data='end_preset')]
    ]
)

no_presets = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Заполнить форму', callback_data='add_preset')]
    ]
)


async def make_list_kb(presets: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for pst in presets:
        kb.button(text=f'{pst[2]}, {pst[3]}, {pst[4]}',
                  callback_data=f'preset_{pst[0]}')
    kb.button(text='Добавить форму', callback_data='add_preset')
    return kb.adjust(1).as_markup(resize_keyboard=True)



async def make_presets_kb(presets: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for pst in presets:
        kb.button(text=f'{pst[2]}, {pst[3]}, {pst[4]}',
                  callback_data=f'preset_{pst[0]}')
    kb.button(text='Добавить форму', callback_data='add_preset')
    return kb.adjust(1).as_markup(resize_keyboard=True)


async def make_del_presets_kb(presets: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for pst in presets:
        kb.button(text=f'{pst[2]}, {pst[3]}, {pst[4]}',
                  callback_data=f'del_preset_{pst[0]}')
    return kb.adjust(1).as_markup(resize_keyboard=True)



