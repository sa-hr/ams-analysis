import csv
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE taxpayers (id INTEGER PRIMARY KEY AUTOINCREMENT, oib TEXT, posrednik TEXT, active INTEGER)''')

with open('/root/output.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    data = []
    
    for row in reader:
        start_date = row.get('Datum početka obveze PDV-a', '').strip()
        end_date = row.get('Datum završetka obveze PDV-a', '').strip()
        
        # Active only if Start Date exists AND End Date is empty
        is_active = 1 if start_date and not end_date else 0

        raw_oib = row['OIB obveznika']
        clean_oib = ''.join(filter(str.isdigit, raw_oib))
        
        data.append((clean_oib, None, is_active))

cursor.executemany('INSERT INTO taxpayers (oib, posrednik, active) VALUES (?, ?, ?)', data)

conn.commit()
conn.close()
