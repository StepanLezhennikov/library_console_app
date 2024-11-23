import enum
import json
import os
from typing import Dict, List, Optional

DATA_FILE = "db.json"

class Status(enum.Enum):
    """
    Enum-класс для статусов книг.
    """
    IN_STOCK = "в наличии"
    GIVEN = "выдана"


def load_full_data() -> List[Dict]:
    """
    Загрузка всех данных из файла.

    :return: Список словарей с данными о книгах. Если файл пустой или отсутствует, возвращается пустой список.
    """
    if not os.path.exists(DATA_FILE):
        return []
    if os.path.getsize(DATA_FILE) == 0:
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
        if type(data) is dict:
            data = [data]
        return data


def save_data(data: List[Dict]) -> None:
    """
    Сохранение всех данных в файл.

    :param data: Список словарей с данными о книгах.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def add_one_book(book: Dict[str, str | int]) -> Dict[str, str | int] | None:
    """
    Добавление новой книги в библиотеку.

    :param book: Словарь с полями "title", "author", "year".
    :return: Словарь с добавленной книгой (включая ID и статус), либо None в случае ошибки.
    """
    books = load_full_data()
    book_id = max([b.get('id') for b in books], default=0) + 1

    new_book = {
        "id": book_id,
        "title": book["title"],
        "author": book["author"],
        "year": book["year"],
        "status": Status.IN_STOCK.value,
    }
    books.append(new_book)
    save_data(books)
    return new_book


def delete_book(book_id: int) -> Dict[str, str | int] | None:
    """
    Удаление книги из библиотеки.

    :param book_id: ID книги, которую необходимо удалить.
    :return: Словарь с удаленной книгой, либо None, если книги с таким ID не существует.
    """
    books = load_full_data()
    try:
        book_index = [index for index, book in enumerate(books) if book['id'] == book_id][0]
    except IndexError:
        print(f"Книги с id={book_id} не существует")
        return None
    deleted_book = books.pop(book_index)
    save_data(books)
    return deleted_book


def find_book(title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None, id: Optional[int] = None) -> List[Dict[str, str | int]] | None:
    """
    Поиск книги в библиотеке.

    :param title: Название книги (необязательно).
    :param author: Автор книги (необязательно).
    :param year: Год издания книги (необязательно).
    :param id: ID книги (необязательно).
    :return: Список книг, удовлетворяющих критериям поиска, либо None, если ничего не найдено.
    """
    books = load_full_data()
    book = [b for b in books if (b['title'] == title or b['author'] == author or b['year'] == year or b['id'] == id)]
    if not book:
        print("Книга не найдена")
        return None
    return book


def show_all_books() -> List[Dict] | None:
    """
    Вывод всех книг из библиотеки.

    :return: Список всех книг, либо None, если библиотека пуста.
    """
    books = load_full_data()
    if not books:
        print("Книг пока что нет")
        return None
    return books


def change_status(book_id: int, new_status: Status) -> True | False:
    """
    Изменение статуса книги.

    :param book_id: ID книги, статус которой нужно изменить.
    :param new_status: Новый статус ("в наличии" или "выдана").
    :return: True, если статус успешно изменен, False, если произошла ошибка.
    """
    if new_status not in [Status.IN_STOCK.value, Status.GIVEN.value]:
        print("Неверно указан статус")
        return False
    books = load_full_data()

    for book in books:
        if book['id'] == book_id:
            book['status'] = new_status
            save_data(books)
            return True
    print(f"Книги с id={book_id} не существует")
    return False
