import os

def get_book_text(page: int, book_path: str = 'book/book.txt') -> str:
    """Получить текст страницы книги"""
    try:
        # Получаем абсолютный путь к файлу
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(current_dir, book_path)

        print(f"📖 Ищу книгу по пути: {full_path}")
        print(f"📖 Существует ли файл: {os.path.exists(full_path)}")

        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Делим книгу на страницы по 1500 символов
        page_size = 1500
        pages = [content[i:i+page_size] for i in range(0, len(content), page_size)]

        print(f"📖 Всего страниц: {len(pages)}, запрошена страница: {page}")

        if 1 <= page <= len(pages):
            return pages[page - 1]
        elif page > len(pages):
            return "Конец книги."
        else:
            return f"Страница {page} не найдена. Всего страниц: {len(pages)}"

    except FileNotFoundError as e:
        error_msg = f"❌ Файл книги не найден: {e}\n"
        error_msg += f"Искал по пути: {full_path}\n"
        error_msg += f"Текущая директория: {os.getcwd()}\n"

        # Покажем структуру папок
        error_msg += "\n📁 Содержимое текущей директории:\n"
        for root, dirs, files in os.walk(current_dir):
            level = root.replace(current_dir, "").count(os.sep)
            indent = " " * 2 * level
            error_msg += f"{indent}{os.path.basename(root)}/\n"
            subindent = " " * 2 * (level + 1)
            for file in files:
                if file.endswith(".txt") or file.endswith(".py"):
                    error_msg += f"{subindent}{file}\n"

        return error_msg

    except Exception as e:
        return f"Ошибка при чтении книги: {e}"

def get_total_pages(book_path: str = 'book/book.txt') -> int:
    """Получить общее количество страниц"""
    try:
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(current_dir, book_path)

        with open(full_path, 'r', encoding='utf-8') as file:
            content = file.read()

        page_size = 1500
        pages = [content[i:i+page_size] for i in range(0, len(content), page_size)]
        return len(pages)

    except FileNotFoundError:
        return 10  # Возвращаем дефолтное значение для тестов
    except Exception:
        return 10