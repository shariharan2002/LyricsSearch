import sqlite3

# Create database and table
conn = sqlite3.connect('songs.db')
c = conn.cursor()
c.execute('''
CREATE TABLE songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    lyrics TEXT NOT NULL
)
''')

# Add sample data
songs = [
    ("Raghupati Raghav", "Raghupati Raghav Raja Ram\nPatit Pavan Sita Ram"),
    ("Shiv Tandav Stotram", "Jatatavigalajjalapravahapavitasthale..."),
    ("Gayatri Mantra", "Om Bhur Bhuva Swaha\nTat Savitur Varenyam...")
]
c.executemany('INSERT INTO songs (title, lyrics) VALUES (?, ?)', songs)

conn.commit()
conn.close()
