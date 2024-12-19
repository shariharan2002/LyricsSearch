import os
import sqlite3

# Database connection
DB_PATH = 'songs.db'  # Update with your database path
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Ensure the table exists (with the schema you provided)
cursor.execute('''
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    lyrics TEXT NOT NULL
)
''')
conn.commit()

# Directory containing the text files
TEXT_FILES_DIR = r"C:\Users\shari\OneDrive\Desktop\lyrics_search\Lyrics"

def push_files_to_db(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            title = os.path.splitext(filename)[0]  # Use filename (without extension) as the title
            file_path = os.path.join(directory, filename)

            # Read the lyrics from the file
            with open(file_path, 'r', encoding='utf-8') as f:
                lyrics = f.read()

            # Check if the song already exists based on the title
            cursor.execute("SELECT id FROM songs WHERE title = ?", (title,))
            result = cursor.fetchone()

            if result:
                # Update existing entry
                print(f"Updating lyrics for: {title}")
                cursor.execute(
                    '''
                    UPDATE songs 
                    SET lyrics = ? 
                    WHERE title = ?
                    ''', (lyrics, title)
                )
            else:
                # Insert new entry
                print(f"Inserting new song: {title}")
                cursor.execute(
                    '''
                    INSERT INTO songs (title, lyrics) 
                    VALUES (?, ?)
                    ''', (title, lyrics)
                )

    # Commit changes and close the database connection
    conn.commit()
    print("Database updated successfully!")

# Run the function
push_files_to_db(TEXT_FILES_DIR)

# Close connection
conn.close()
