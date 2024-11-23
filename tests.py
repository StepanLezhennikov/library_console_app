import unittest
from crud import add_one_book, delete_book, find_book, change_status, save_data, load_full_data, Status


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            {"id": 1, "title": "Book One", "author": "Author A", "year": 2000, "status": "в наличии"},
            {"id": 2, "title": "Book Two", "author": "Author B", "year": 2010, "status": "выдана"}
        ]
        save_data(self.test_data)

    def test_add_one_book(self):
        new_book = add_one_book({"title": "Book Three", "author": "Author C", "year": 2020})
        self.assertEqual(new_book["title"], "Book Three")
        self.assertEqual(new_book["author"], "Author C")
        self.assertEqual(new_book["year"], 2020)
        self.assertEqual(new_book["status"], Status.IN_STOCK.value)

        books = load_full_data()
        self.assertIn(new_book, books)

    def test_delete_book(self):
        deleted_book = delete_book(1)
        self.assertIsNotNone(deleted_book)
        self.assertEqual(deleted_book["id"], 1)

        books = load_full_data()
        self.assertNotIn(deleted_book, books)

        self.assertIsNone(delete_book(99))

    def test_find_book(self):
        results = find_book(author="Author A")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["author"], "Author A")

        results = find_book(title="Book Two")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Book Two")

        results = find_book(year=2000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["year"], 2000)

        results = find_book(title="Nonexistent Book")
        self.assertIsNone(results)

    def test_change_status(self):
        result = change_status(1, Status.GIVEN.value)
        self.assertTrue(result)

        books = load_full_data()
        book = next((b for b in books if b["id"] == 1), None)
        self.assertIsNotNone(book)
        self.assertEqual(book["status"], Status.GIVEN.value)

        self.assertFalse(change_status(99, Status.IN_STOCK.value))

        self.assertFalse(change_status(1, "unknown"))

if __name__ == "__main__":
    unittest.main()
