from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Data dummy untuk contoh
books = [
    {"id": "1", "title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "description": "A young wizard's journey begins."},
    {"id": "2", "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "description": "An epic fantasy adventure to destroy a powerful ring."},
    {"id": "3", "title": "To Kill a Mockingbird", "author": "Harper Lee", "description": "A story of racial injustice in the Deep South."},
    {"id": "4", "title": "1984", "author": "George Orwell", "description": "A dystopian novel about surveillance and control."},
    {"id": "5", "title": "Pride and Prejudice", "author": "Jane Austen", "description": "A classic romance and social commentary."},
    {"id": "6", "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "description": "A critique of the American Dream in the Roaring Twenties."},
    {"id": "7", "title": "Moby Dick", "author": "Herman Melville", "description": "A seafaring tale of obsession and revenge."},
    {"id": "8", "title": "War and Peace", "author": "Leo Tolstoy", "description": "A historical novel set during the Napoleonic Wars."},
    {"id": "9", "title": "The Catcher in the Rye", "author": "J.D. Salinger", "description": "A young man's struggle with growing up."},
    {"id": "10", "title": "The Hobbit", "author": "J.R.R. Tolkien", "description": "The adventure of a reluctant hero in Middle-earth."},
    {"id": "11", "title": "The Odyssey", "author": "Homer", "description": "An epic journey home after the Trojan War."},
    {"id": "12", "title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "description": "A tale of guilt and redemption in 19th-century Russia."},
    {"id": "13", "title": "Brave New World", "author": "Aldous Huxley", "description": "A dystopian society obsessed with technology and control."},
    {"id": "14", "title": "Anna Karenina", "author": "Leo Tolstoy", "description": "A tragic story of love, society, and morality."},
    {"id": "15", "title": "Jane Eyre", "author": "Charlotte Bronte", "description": "The life and struggles of an orphaned girl."},
]

# Helper function untuk mencari buku berdasarkan ID
def find_book(book_id):
    return next((book for book in books if book['id'] == book_id), None)

class BookList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(books),
            "books": books
        }

    def post(self):
        data = request.get_json()
        new_book = {
            "id": str(len(books) + 1),
            "title": data.get("title"),
            "author": data.get("author"),
            "description": data.get("description"),
        }
        books.append(new_book)
        return {"error": False, "message": "Book added", "book": new_book}, 201

class BookDetail(Resource):
    def get(self, book_id):
        book = find_book(book_id)
        if book:
            return {"error": False, "message": "success", "book": book}
        return {"error": True, "message": "Book not found"}, 404

    def put(self, book_id):
        data = request.get_json()
        book = find_book(book_id)
        if book:
            book.update({
                "title": data.get("title", book["title"]),
                "author": data.get("author", book["author"]),
                "description": data.get("description", book["description"])
            })
            return {"error": False, "message": "Book updated", "book": book}
        return {"error": True, "message": "Book not found"}, 404

    def delete(self, book_id):
        global books
        book = find_book(book_id)
        if book:
            books = [b for b in books if b["id"] != book_id]
            return {"error": False, "message": "Book deleted"}
        return {"error": True, "message": "Book not found"}, 404

class BookSearch(Resource):
    def get(self):
        query = request.args.get('q', '').lower()
        result = [b for b in books if query in b['title'].lower() or query in b['description'].lower()]
        return {
            "error": False,
            "found": len(result),
            "books": result
        }

api.add_resource(BookList, '/books')
api.add_resource(BookDetail, '/books/<string:book_id>')
api.add_resource(BookSearch, '/books/search')

if __name__ == '__main__':
    app.run(debug=True)
