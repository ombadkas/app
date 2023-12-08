from flask import Flask, render_template, request
import requests
from markupsafe import escape

app = Flask(__name__)

def get_book_details(isbn):
    # Using Google Books API to get book details by ISBN
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            book_info = data['items'][0]['volumeInfo']

            book_name = book_info.get('title', 'N/A')
            authors = book_info.get('authors', [])
            cover_photo_url = book_info.get('imageLinks', {}).get('thumbnail', None)
            description = book_info.get('description', 'N/A')
            language = book_info.get('language', 'N/A')

            return {
                'Book Name': book_name,
                'Authors': authors,
                'Cover Photo URL': cover_photo_url,
                'Description': description,
                'Language': language,
            }
        else:
            return {'error': 'Book not found on Google Books.'}
    else:
        return {'error': 'Failed to fetch details. Check the ISBN and try again.'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book-details', methods=['POST'])
def book_details():
    isbn = request.form['isbn']
    book_details = get_book_details(isbn)
    return render_template('book_details.html', book_details=book_details)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
