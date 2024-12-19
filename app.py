from flask import Flask, render_template, request, redirect, url_for, jsonify
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
    fulltext = request.args.get('fulltext', 'off') == 'on'
    
    if not query:
        return redirect(url_for('index'))

    conn = get_db_connection()
    
    if fulltext:
        # Use LOWER() to make the query case-insensitive
        songs = conn.execute(
            "SELECT id, title FROM songs WHERE LOWER(title) LIKE LOWER(?) OR LOWER(lyrics) LIKE LOWER(?)",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
    else:
        songs = conn.execute(
            "SELECT id, title FROM songs WHERE LOWER(title) LIKE LOWER(?)",
            (f'%{query}%',)
        ).fetchall()
    
    conn.close()

    return render_template('search_results.html', query=query, songs=songs)

@app.route('/search/suggestions')
def suggestions():
    query = request.args.get('q', '').strip()
    fulltext = request.args.get('fulltext', 'off') == 'on'
    
    if not query or len(query) < 4:
        return jsonify({'songs': []})

    conn = get_db_connection()
    
    if fulltext:
        # Use LOWER() to make the query case-insensitive
        songs = conn.execute(
            "SELECT id, title FROM songs WHERE LOWER(title) LIKE LOWER(?) OR LOWER(lyrics) LIKE LOWER(?) LIMIT 5",
            (f'%{query}%', f'%{query}%')
        ).fetchall()
    else:
        songs = conn.execute(
            "SELECT id, title FROM songs WHERE LOWER(title) LIKE LOWER(?) LIMIT 5",
            (f'%{query}%',)
        ).fetchall()
    
    conn.close()
    
    return jsonify({'songs': [{'id': song['id'], 'title': song['title']} for song in songs]})

@app.route('/song/<int:song_id>')
def song(song_id):
    conn = get_db_connection()
    song = conn.execute("SELECT * FROM songs WHERE id = ?", (song_id,)).fetchone()
    conn.close()

    if not song:
        return "Song not found!", 404

    return render_template('song.html', song=song)


@app.route('/all_songs')
def all_songs():
    conn = get_db_connection()
    songs = conn.execute("SELECT id, title FROM songs").fetchall()
    conn.close()
    return render_template('all_songs.html', songs=songs)



if __name__ == '__main__':
    app.run(debug=True)
