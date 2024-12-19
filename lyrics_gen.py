import os
import re

# Function to process the text file and create song files
def process_lyrics_file(input_file):
    # Create a directory named 'Lyrics' if it doesn't exist
    output_dir = "Lyrics"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the content of the input file
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Regex to match the time format hh:mm:ss
    time_pattern = re.compile(r"\d{1,2}:\d{2}:\d{2}")

    current_song = None
    current_lyrics = []

    for line in lines:
        # Check if the line contains a timestamp
        if time_pattern.match(line.strip()):
            # If there's a current song being processed, save it
            if current_song:
                save_song_to_file(output_dir, current_song, current_lyrics)

            # Start a new song
            parts = line.strip().split(maxsplit=1)
            current_song = parts[1] if len(parts) > 1 else "Unknown_Song"
            current_song = capitalize_song_name(current_song)  # Capitalize the song name
            current_lyrics = []
        else:
            # Add the line to the current song's lyrics
            if line.strip():
                current_lyrics.append(format_lyrics_sentence_case(line.strip()))  # Format lyrics to sentence case

    # Save the last song if any
    if current_song:
        save_song_to_file(output_dir, current_song, current_lyrics)

# Function to capitalize the song name (capitalize each word)
def capitalize_song_name(song_name):
    # Capitalize each word, while handling exceptions like 'the', 'a', etc.
    exceptions = ['a', 'an', 'and', 'but', 'for', 'nor', 'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet']
    words = song_name.split()
    capitalized_words = [word.capitalize() if word.lower() not in exceptions else word.lower() for word in words]
    return " ".join(capitalized_words)

# Function to format the lyrics to sentence case (capitalize first letter of each sentence)
def format_lyrics_sentence_case(lyric_line):
    # Capitalize the first letter of the line and make the rest lowercase
    return lyric_line.capitalize()

# Function to save a song's lyrics to a file
def save_song_to_file(output_dir, song_name, lyrics):
    # Capitalize the song name for the filename (ensure it's in Capitalize Each Word Case)
    song_name_for_filename = capitalize_song_name(song_name)
    
    # Replace spaces and special characters in the song name to make it a valid filename
    filename = re.sub(r"[\\/:*?\"<>|]", "_", song_name_for_filename) + ".txt"
    file_path = os.path.join(output_dir, filename)

    # Write the lyrics to the file
    with open(file_path, "w", encoding="utf-8") as file:
        if lyrics:
            file.write("\n".join(lyrics))
        else:
            file.write("(Lyrics not available)")

# Example usage
if __name__ == "__main__":
    input_file = "bhajans.txt"  # Replace with your input text file
    process_lyrics_file(input_file)
