import sqlite3
import csv
import os

# Chemins
csv_path = os.path.join(os.path.dirname(__file__), '../data/stanford_ranking_2025.csv')
db_path = os.path.join(os.path.dirname(__file__), '../data/stanford_ranking_2025.db')

def main():
    # Lire le CSV
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    # Créer la base SQLite
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stanford_ranking_2025 (
        authfull TEXT,
        inst_name TEXT,
        cntry TEXT,
        firstyr INTEGER,
        lastyr INTEGER,
        rank_ns INTEGER
    )''')
    c.execute('DELETE FROM stanford_ranking_2025')
    for row in rows:
        c.execute('''INSERT INTO stanford_ranking_2025 (authfull, inst_name, cntry, firstyr, lastyr, rank_ns) VALUES (?, ?, ?, ?, ?, ?)''',
                  (row['authfull'], row['inst_name'], row['cntry'], int(row['firstyr']), int(row['lastyr']), int(row['rank (ns)'])))
    conn.commit()
    conn.close()
    print(f"Base de données créée : {db_path}")

if __name__ == "__main__":
    main()
