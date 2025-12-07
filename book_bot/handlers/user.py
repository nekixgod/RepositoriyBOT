from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_bookmarks_keyboard
from services.file_handling import get_book_text, get_total_pages
from database.database import db

router = Router()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON['/start'])
    if not db.get_user_page(message.from_user.id):
        db.save_user_page(message.from_user.id, 1)

@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(LEXICON['/help'])

@router.message(Command(commands=['beginning']))
async def process_beginning_command(message: Message):
    db.save_user_page(message.from_user.id, 1)
    text = get_book_text(1)
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(1)
    )

@router.message(Command(commands=['continue']))
async def process_continue_command(message: Message):
    page = db.get_user_page(message.from_user.id)
    text = get_book_text(page)
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard(page)
    )

@router.message(Command(commands=['bookmarks']))
async def process_bookmarks_command(message: Message):
    bookmarks = db.get_bookmarks(message.from_user.id)
    if bookmarks:
        await message.answer(
            text=LEXICON['bookmarks'],
            reply_markup=create_bookmarks_keyboard(bookmarks)
        )
    else:
        await message.answer(LEXICON['no_bookmarks'])

@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    current_page = int(callback.message.reply_markup.inline_keyboard[0][1].text)
    total_pages = get_total_pages()
    
    if current_page < total_pages:
        new_page = current_page + 1
        db.save_user_page(callback.from_user.id, new_page)
        
        text = get_book_text(new_page)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(new_page)
        )
    await callback.answer()

@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    current_page = int(callback.message.reply_markup.inline_keyboard[0][1].text)
    
    if current_page > 1:
        new_page = current_page - 1
        db.save_user_page(callback.from_user.id, new_page)
        
        text = get_book_text(new_page)
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(new_page)
        )
    await callback.answer()

@router.callback_query(lambda x: x.data.isdigit() and 
                      x.message.reply_markup and 
                      len(x.message.reply_markup.inline_keyboard) == 1)
async def process_page_press(callback: CallbackQuery):
    page = int(callback.data)
    
    if db.add_bookmark(callback.from_user.id, page):
        await callback.answer(f'Страница {page} добавлена в закладки!')
    else:
        await callback.answer('Эта страница уже в закладках!')

@router.callback_query(F.data.startswith('bookmark_'))
async def process_bookmark_press(callback: CallbackQuery):
    page = int(callback.data.split('_')[1])
    db.save_user_page(callback.from_user.id, page)
    
    text = get_book_text(page)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard(page)
    )
    await callback.answer()

@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_bookmarks(callback: CallbackQuery):
    bookmarks = db.get_bookmarks(callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks'],
        reply_markup=create_edit_bookmarks_keyboard(bookmarks)
    )
    await callback.answer()

@router.callback_query(F.data == 'cancel')
async def process_cancel(callback: CallbackQuery):
    await callback.message.edit_text(LEXICON['cancel'])
    await callback.answer()

@router.callback_query(F.data.startswith('del_'))
async def process_delete_bookmark(callback: CallbackQuery):
    bookmark_id = int(callback.data.split('_')[1])
    db.delete_bookmark(bookmark_id)
    
    bookmarks = db.get_bookmarks(callback.from_user.id)
    if bookmarks:
        await callback.message.edit_text(
            text=LEXICON['edit_bookmarks'],
            reply_markup=create_edit_bookmarks_keyboard(bookmarks)
        )
    else:
        await callback.message.edit_text(LEXICON['no_bookmarks'])
    await callback.answer()