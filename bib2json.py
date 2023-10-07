from tinydb import TinyDB
from bibtexparser.bparser import BibTexParser

def bib2table(bib_file_path, db_path, table_name='papers'):
    db = TinyDB(db_path)
    
    # Check if the table already exists
    if table_name not in db.tables():
        with open(bib_file_path, 'r', encoding='utf-8') as bib_file:
            bib_content = bib_file.read()
            paper_table = db.table(table_name)
            parser = BibTexParser()
            bib_database = parser.parse(bib_content)
            for entry in bib_database.entries:
                paper_table.insert(entry)

        print(f'{bib_file_path} has been imported into the {table_name} table.')
    else:
        print(f'The table {table_name} already exists in the database.')

# Usage example:
bib2table('paper.bib', 'paper.json', 'papers')
