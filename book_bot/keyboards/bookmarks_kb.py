from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON
from services.file_handling import get_book_text

def create_bookmarks_keyboard(bookmarks: list) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    for bookmark_id, page in bookmarks:
        # Получаем первые 50 символов текста страницы
        page_text = get_book_text(page)[:50] + '...'
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{page} - {page_text}',
                callback_data=f'bookmark_{page}'
            )
        )
    
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit_bookmarks_button'],
            callback_data='edit_bookmarks'
        ),
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        ),
        width=2
    )
    
    return kb_builder.as_markup()

def create_edit_bookmarks_keyboard(bookmarks: list) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    
    for bookmark_id, page in bookmarks:
        page_text = get_book_text(page)[:50] + '...'
        kb_builder.row(
            InlineKeyboardButton(
                text=f'❌ {page} - {page_text}',
                callback_data=f'del_{bookmark_id}'
            )
        )
    
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        )
    )
    
    return kb_builder.as_markup()