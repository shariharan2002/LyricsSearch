from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database helper
def get_db_connection():
    conn = sqlite3.connect('songs.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('index'))

    conn = get_db_connection()
    songs = conn.execute(
        "SELECT id, title FROM songs WHERE title LIKE ? OR lyrics LIKE ?",
        (f'%{query}%', f'%{query}%')
    ).fetchall()
    conn.close()

    return render_template('search_results.html', query=query, songs=songs)

@app.route('/song/<int:song_id>')
def song(song_id):
    conn = get_db_connection()
    song = conn.execute("SELECT * FROM songs WHERE id = ?", (song_id,)).fetchone()
    conn.close()

    if not song:
        return "Song not found!", 404

    return render_template('song.html', song=song)

if __name__ == '__main__':
    app.run(debug=True)
