from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
import re
app = Flask(__name__)

db = TinyDB('paper.json')
table = db.table('papers')
bookQuery=Query()

@app.route('/')
def index():
    books = table.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    ID = request.form.get('ID')
    author = request.form.get('author')
    year = request.form.get('year')
    journal = request.form.get('journal')
    doi = request.form.get('doi')
    litmapsid = request.form.get('litmapsid')

    table.insert({'title': title, 'ID':ID, 'author': author, 'year': year, 'journal': journal, 'doi':doi, 'litmapsid':litmapsid})
    return redirect(url_for('index'))

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit(book_id):
    book = table.get(doc_id=book_id)

    if request.method == 'POST':
        title = request.form.get('title')
        ID = request.form.get('ID')
        author = request.form.get('author')
        year = request.form.get('year')
        journal = request.form.get('journal')
        doi = request.form.get('doi')
        litmapsid = request.form.get('litmapsid')
        table.update({'title': title, 'ID':ID, 'author': author, 'year': year, 'journal': journal, 'doi':doi, 'litmapsid':litmapsid}, doc_ids=[book_id])
        return redirect(url_for('index'))
    return render_template('edit.html', book=book)

@app.route('/delete/<int:book_id>')
def delete(book_id):
    table.remove(doc_ids=[book_id])
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search').lower()

    books= table.search((bookQuery.title.search(search_query, flags=re.IGNORECASE)) |
                (bookQuery.ID.search(search_query, flags=re.IGNORECASE)) |
                (bookQuery.author.search(search_query, flags=re.IGNORECASE)) |
                (bookQuery.year.search(search_query, flags=re.IGNORECASE)) |
                (bookQuery.journal.search(search_query, flags=re.IGNORECASE)) |
                (bookQuery.doi.search(search_query, flags=re.IGNORECASE)))

    return render_template('search_results.html', books=books)



if __name__ == '__main__':
    app.run(debug=True)
