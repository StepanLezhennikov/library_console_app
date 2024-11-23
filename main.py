from crud import add_one_book, delete_book, find_book, show_all_books, change_status, Status


def main():
    print("Добро пожаловать в систему управления библиотекой!")
    while True:
        print("\nВыберите действие:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выйти")

        choice = input("Введите номер команды: ").strip()

        if choice == "1":
            title = input("Введите название книги: ").strip()
            author = input("Введите автора книги: ").strip()
            year = input("Введите год издания книги: ").strip()

            if not year.isdigit():
                print("Год издания должен быть числом!")
                continue

            new_book = add_one_book({
                "title": title,
                "author": author,
                "year": int(year)
            })

            if new_book:
                print(f"Книга добавлена: {new_book}")
            else:
                print("Ошибка при добавлении книги.")

        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ").strip()

            if not book_id.isdigit():
                print("ID должен быть числом!")
                continue

            deleted_book = delete_book(int(book_id))
            if deleted_book:
                print(f"Книга удалена: {deleted_book}")
            else:
                print("Ошибка: Книга с таким ID не найдена.")

        elif choice == "3":
            print("Введите параметры поиска (оставьте пустыми ненужные поля):")
            title = input("Название книги: ").strip() or None
            author = input("Автор книги: ").strip() or None
            year = input("Год издания книги: ").strip() or None


            year = int(year) if year and year.isdigit() else None

            found_books = find_book(title=title, author=author, year=year)
            if found_books:
                print("Найденные книги:")
                for book in found_books:
                    print(book)
            else:
                print("Книга не найдена.")

        elif choice == "4":
            books = show_all_books()
            if books:
                print("Список всех книг:")
                for book in books:
                    print(book)
            else:
                print("Книг пока что нет.")

        elif choice == "5":
            book_id = input("Введите ID книги для изменения статуса: ").strip()
            if not book_id.isdigit():
                print("ID должен быть числом!")
                continue

            new_status = input("Введите новый статус (в наличии/выдана): ").strip()
            if new_status not in [Status.IN_STOCK.value, Status.GIVEN.value]:
                print("Статус должен быть 'в наличии' или 'выдана'!")
                continue

            success = change_status(int(book_id), new_status)
            if success:
                print("Статус книги успешно обновлен.")
            else:
                print("Ошибка при обновлении статуса.")

        elif choice == "0":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Неверная команда, попробуйте снова.")


if __name__ == '__main__':
    main()
