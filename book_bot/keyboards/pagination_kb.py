from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON

def create_pagination_keyboard(page: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['backward'],
            callback_data='backward'
        ),
        InlineKeyboardButton(
            text=str(page),
            callback_data=str(page)
        ),
        InlineKeyboardButton(
            text=LEXICON['forward'],
            callback_data='forward'
        ),
        width=3
    )
    
    return kb_builder.as_markup()