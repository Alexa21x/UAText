import os
import sqlite3

# Inisialisasi database SQLite
def init_db():
    conn = sqlite3.connect('unique_codes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS codes (code TEXT PRIMARY KEY, name TEXT NOT NULL)''')
    conn.commit()
    return conn

# Menambahkan kode unik ke database
def add_unique_code(conn, code, name):
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO codes (code, name) VALUES (?, ?)', (code, name))
    conn.commit()

# Mengambil semua kode unik dari database
def get_unique_codes(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT code, name FROM codes')
    return cursor.fetchall()

def format_hex_data(hex_data):
    hex_data = hex_data.upper()
    formatted_data = ' '.join([hex_data[i:i + 2] for i in range(0, len(hex_data), 2)])
    return formatted_data

def replace_unique_codes(formatted_data, unique_codes):
    for code, name in unique_codes:
        formatted_data = formatted_data.replace(code, f'\n"{name}"\n')
    return formatted_data

def replace_special_sequences(formatted_data):
    formatted_data = formatted_data.replace('0A 0A', 'A6 A6')
    formatted_data = formatted_data.replace('2E 0A 00', '2E A6 00')
    formatted_data = formatted_data.replace('0A 00 0A 00', 'A6 00 A6 00')
    return formatted_data

def delete_input_file(file_path):
    try:
        os.remove(file_path)
        print(f"Input file {file_path} has been deleted.")
    except Exception as e:
        print(f"Failed to delete input file: {e}")

def process_file(file_path, conn):
    if file_path.endswith('.txt'):
        try:
            with open(file_path, 'r') as f:
                hex_data = f.read().strip()
            formatted_data = format_hex_data(hex_data)
            formatted_data = replace_special_sequences(formatted_data)
            unique_codes = get_unique_codes(conn)
            formatted_data = replace_unique_codes(formatted_data, unique_codes)
            
            output_file_path = os.path.splitext(file_path)[0] + '_formatted.txt'
            with open(output_file_path, 'w') as f:
                f.write(formatted_data)
            
            print(f"Formatted data saved to: {output_file_path}")
            
            # Hapus file input setelah proses selesai
            delete_input_file(file_path)

        except Exception as e:
            print(f"Failed to process file: {e}")

# Inisialisasi database dan menambahkan contoh kode unik
conn = init_db()
add_unique_code(conn, "80 1F 40 38 CB FE FF FF 48 00 61 00 79 00 20 00 71 00 75 00 65 00 20 00 6D 00 65 00 6A 00 6F 00 72 00 61 00 72 00 20 00 65 00 73 00 74 00 61 00 73 00 20 00 70 00 69 00 73 00 74 00 61 00 73 00 2E 00 20 00 45 00 6E 00 20 00 72 00 6F 00 73 00 61 00 20 00 6C 00 61 00 73 00 20 00 71 00 75 00 65 00 20 00 73 00 65 00 20 00 70 00 6F 00 64 00 72 00 ED 00 61 00 6E 00 20 00 71 00 75 00 69 00 74 00 61 00 72 00 2E 00 20 00 45 00 6E 00 20 00 76 00 65 00 72 00 64 00 65 00 20 00 69 00 6D 00 70 00 6F 00 72 00 74 00 61 00 6E 00 74 00 65 00 73 00 20 00 61 00 20 00 6D 00 61 00 6E 00 74 00 65 00 6E 00 65 00 72 00 2E 00 20 00 53 00 75 00 73 00 74 00 69 00 74 00 75 00 69 00 72 00 20 00 4D 00 61 00 64 00 65 00 6C 00 69 00 6E 00 65 00 20 00 70 00 6F 00 72 00 20 00 6D 00 6F 00 6E 00 6A 00 61 00 20 00 6F 00 20 00 45 00 76 00 69 00 6C 00 20 00 4E 00 75 00 6E 00 2E 00 20 00 45 00 78 00 70 00 6C 00 69 00 63 00 61 00 72 00 20 00 63 00 75 00 61 00 6C 00 20 00 65 00 73 00 20 00 65 00 6C 00 20 00 6F 00 62 00 6A 00 65 00 74 00 69 00 76 00 6F 00 20 00 64 00 65 00 6C 00 20 00 6A 00 75 00 65 00 67 00 6F 00 2E 00 20 00 45 00 78 00 70 00 6C 00 69 00 63 00 61 00 72 00 20 00 71 00 75 00 65 00 20 00 74 00 65 00 20 00 70 00 75 00 65 00 64 00 65 00 73 00 20 00 65 00 73 00 63 00 6F 00 6E 00 64 00 65 00 72 00 2E 00 20 00 45 00 6C 00 20 00 6A 00 75 00 67 00 61 00 64 00 6F 00 72 00 20 00 70 00 75 00 65 00 64 00 65 00 20 00 6D 00 6F 00 72 00 69 00 72 00 20 00 61 00 75 00 6E 00 71 00 75 00 65 00 20 00 6E 00 6F 00 20 00 6C 00 65 00 20 00 6D 00 61 00 74 00 65 00 20 00 53 00 4D 00 2E 00 20 00 45 00 78 00 70 00 6C 00 69 00 63 00 61 00 72 00 20 00 6D 00 6F 00 64 00 6F 00 73 00 20 00 64 00 65 00 20 00 6A 00 75 00 65 00 67 00 6F 00 20 00 79 00 20 00 63 00 6F 00 6E 00 66 00 69 00 67 00 75 00 72 00 61 00 63 00 69 00 6F 00 6E 00 65 00 73 00 20 00 64 00 65 00 6C 00 20 00 6D 00 65 00 6E 00 FA 00 2E 00 00 00", "Explanation of Sister Madeline")
add_unique_code(conn, "80 1F F9 7F 3A 00 00 00 41 70 70 72 6F 78 69 6D 61 74 65 6C 79 20 68 6F 77 20 6C 6F 6E 67 20 77 69 6C 6C 20 74 68 69 73 20 67 61 6D 65 20 62 65 20 69 6E 20 45 61 72 6C 79 20 41 63 63 65 73 73 3F 00 B5 FF FF FF BF 00 43 00 75 00 E1 00 6E 00 74 00 6F 00 20 00 74 00 69 00 65 00 6D 00 70 00 6F 00 20 00 76 00 61 00 20 00 61 00 20 00 65 00 73 00 74 00 61 00 72 00 20 00 65 00 73 00 74 00 65 00 20 00 6A 00 75 00 65 00 67 00 6F 00 20 00 65 00 6E 00 20 00 61 00 63 00 63 00 65 00 73 00 6F 00 20 00 61 00 6E 00 74 00 69 00 63 00 69 00 70 00 61 00 64 00 6F 00 20 00 61 00 70 00 72 00 6F 00 78 00 69 00 6D 00 61 00 64 00 61 00 6D 00 65 00 6E 00 74 00 65 00 3F 00 00 00 35 01 00 00 00 00 00 00 80 1F 41 38", "Full Game Release Announcement")
add_unique_code(conn, "80 1F 40 38 A1 FF FF FF 65 00 73 00 74 00 6F 00 20 00 65 00 73 00 74 00 61 00 20 00 74 00 72 00 61 00 64 00 75 00 63 00 69 00 64 00 6F 00 20 00 64 00 65 00 20 00 6D 00 69 00 6C 00 20 00 6D 00 61 00 6E 00 65 00 72 00 61 00 73 00 20 00 65 00 6E 00 20 00 6C 00 6F 00 73 00 20 00 64 00 69 00 73 00 74 00 69 00 6E 00 74 00 6F 00 73 00 20 00 69 00 64 00 69 00 6F 00 6D 00 61 00 73 00 2E 00 20 00 65 00 6C 00 20 00 66 00 72 00 61 00 6E 00 63 00 E9 00 73 00 20 00 6E 00 6F 00 20 00 63 00 6F 00 72 00 72 00 65 00 73 00 70 00 6F 00 6E 00 64 00 65 00 20 00 61 00 64 00 65 00 6D 00 E1 00 73 00 21 00 00 00", "Translated in Many Ways. Even French is still inappropriate!")
add_unique_code(conn, "00 1F AB FF FF FF 71 00 75 00 E9 00 20 00 64 00 69 00 66 00 65 00 72 00 65 00 6E 00 63 00 69 00 61 00 20 00 68 00 61 00 79 00 20 00 64 00 69 00 73 00 74 00 61 00 6E 00 63 00 69 00 61 00 20 00 66 00 6F 00 63 00 61 00 6C 00 20 00 28 00 32 00 30 00 20 00 74 00 65 00 6E 00 64 00 72 00 ED 00 61 00 20 00 71 00 75 00 65 00 20 00 65 00 73 00 74 00 61 00 72 00 20 00 61 00 20 00 6C 00 61 00 20 00 64 00 65 00 72 00 65 00 63 00 68 00 61 00 2C 00 20 00 67 00 72 00 61 00 6E 00 20 00 61 00 6E 00 67 00 75 00 6C 00 61 00 72 00 29 00 00 00", "Zoom in Zoom Out")
add_unique_code(conn, "80 1F 40 38 B9 FF FF FF 4F 00 74 00 72 00 61 00 20 00 76 00 65 00 7A 00 20 00 6C 00 ED 00 6F 00 20 00 63 00 6F 00 6E 00 20 00 50 00 72 00 6F 00 2C 00 20 00 64 00 69 00 66 00 65 00 72 00 65 00 6E 00 74 00 65 00 73 00 20 00 74 00 72 00 61 00 64 00 75 00 63 00 63 00 69 00 6F 00 6E 00 65 00 73 00 2C 00 20 00 6F 00 6A 00 6F 00 20 00 66 00 72 00 61 00 6E 00 63 00 E9 00 73 00 20 00 65 00 20 00 69 00 74 00 61 00 6C 00 69 00 61 00 6E 00 6F 00 21 00 00 00", "The word PRO is still a scourge. French still doesn't help!")
add_unique_code(conn, "80 1F 40 38 BF FF FF FF 4E 00 6F 00 6D 00 62 00 72 00 65 00 73 00 20 00 76 00 61 00 72 00 69 00 6F 00 73 00 20 00 65 00 6E 00 20 00 65 00 6C 00 20 00 65 00 73 00 63 00 61 00 70 00 65 00 2C 00 20 00 6F 00 6B 00 20 00 65 00 6E 00 20 00 63 00 61 00 73 00 74 00 65 00 6C 00 6C 00 61 00 6E 00 6F 00 20 00 70 00 61 00 72 00 61 00 20 00 65 00 73 00 63 00 61 00 70 00 65 00 20 00 6A 00 75 00 67 00 F3 00 6E 00 3F 00 00 00", "Various mentions of the word ESCAPE")
add_unique_code(conn, "80 1F 40 38 CD FF FF FF 45 00 73 00 74 00 61 00 72 00 ED 00 61 00 20 00 62 00 69 00 65 00 6E 00 20 00 71 00 75 00 65 00 20 00 70 00 75 00 73 00 69 00 65 00 72 00 61 00 20 00 46 00 75 00 73 00 69 00 62 00 6C 00 65 00 73 00 20 00 43 00 6F 00 6C 00 6F 00 63 00 61 00 64 00 6F 00 73 00 20 00 31 00 2F 00 33 00 2E 00 2E 00 2E 00 00 00", "It would be good to set Fuses Placed 1/3...")
add_unique_code(conn, "80 1F 40 38 65 00 00 00 45 6E 20 63 61 73 74 65 6C 6C 61 6E 6F 20 73 65 20 68 61 20 6D 6F 64 69 66 69 63 61 64 6F 20 6A 75 65 67 6F 20 63 6F 6D 70 6C 65 74 6F 20 70 6F 72 20 61 6C 20 63 6F 6D 70 72 61 72 20 65 6C 20 6A 75 65 67 6F 2E 20 53 65 20 65 6E 74 69 65 6E 64 65 20 22 6A 75 65 67 6F 20 63 6F 6D 70 6C 65 74 6F 22 3F 00", "The game is modified in Spanish 'upon purchase.' Is the 'complete game' understandable?")
add_unique_code(conn, "80 1F 40 38 59 00 00 00 20 68 74 74 70 73 3A 2F 2F 77 77 77 2E 6A 69 6F 73 61 61 76 6E 2E 63 6F 6D 2F 73 68 6F 77 73 2F 45 76 69 6C 2D 4E 75 6E 25 45 32 25 38 30 25 39 39 73 45 76 69 6C 2D 4E 75 6E 2D 47 61 6D 65 2D 56 6F 69 63 65 2D 4C 69 6E 65 73 2F 4E 51 70 35 4A 72 47 59 4D 67 59 5F 00", "Ritual")
add_unique_code(conn, "80 1F FF 7F 60 01 00 00 00 00 00 00 80 1F FF 7F 61 01 00 00 00 00 00 00 80 1F FF 7F 62 01 00 00 00 00 00 00 80 1F FF 7F E7 00 00 00 00 00 00 00 80 1F 40 38 0E 00 00 00 54 45 58 54 4F 53 20 54 49 45 4E 44 41 00", "TEXTOS TIENDA")
add_unique_code(conn, "80 1F FD 7F 4D 00 00 00 48 6F 77 20 61 72 65 20 79 6F 75 20 70 6C 61 6E 6E 69 6E 67 20 6F 6E 20 69 6E 76 6F 6C 76 69 6E 67 20 74 68 65 20 43 6F 6D 6D 75 6E 69 74 79 20 69 6E 20 79 6F 75 72 20 64 65 76 65 6C 6F 70 6D 65 6E 74 20 70 72 6F 63 65 73 73 3F 00 2A 01 00 00 00 00 00 00 80 1F 41 38", "Community Involvement Planning in the Development Process")
add_unique_code(conn, "80 1F FD 7F 49 00 00 00 48 6F 77 20 69 73 20 74 68 65 20 66 75 6C 6C 20 76 65 72 73 69 6F 6E 20 70 6C 61 6E 6E 65 64 20 74 6F 20 64 69 66 66 65 72 20 66 72 6F 6D 20 74 68 65 20 45 61 72 6C 79 20 41 63 63 65 73 73 20 76 65 72 73 69 6F 6E 3F 00 2C 01 00 00 00 00 00 00 80 1F 41 38", "Differences between the full version and the Early Access version")
add_unique_code(conn, "80 1F FD 7F 43 00 00 00 57 69 6C 6C 20 74 68 65 20 67 61 6D 65 20 62 65 20 70 72 69 63 65 64 20 64 69 66 66 65 72 65 6E 74 6C 79 20 64 75 72 69 6E 67 20 61 6E 64 20 61 66 74 65 72 20 45 61 72 6C 79 20 41 63 63 65 73 73 3F 00 33 01 00 00 00 00 00 00 80 1F 41 38", "Will the game be priced differently during and after Early Access?")
add_unique_code(conn, "80 1F FD 7F 37 00 00 00 57 68 61 74 20 69 73 20 74 68 65 20 63 75 72 72 65 6E 74 20 73 74 61 74 65 20 6F 66 20 74 68 65 20 45 61 72 6C 79 20 41 63 63 65 73 73 20 76 65 72 73 69 6F 6E 3F 00 2E 01 00 00 00 00 00 00 80 1F 41 38", "What is the current state of the Early Access version?")
add_unique_code(conn, "80 1F F9 7F 0D 00 00 00 4C 61 75 6E 64 72 79 20 42 65 6C 6C 00 E8 FF FF FF 41 00 6C 00 61 00 72 00 6D 00 61 00 20 00 64 00 65 00 20 00 6C 00 61 00 20 00 6C 00 61 00 76 00 61 00 6E 00 64 00 65 00 72 00 ED 00 61 00 00 00", "THE END")
add_unique_code(conn, "80 1F 40 38 34 00 00 00 67 75 69 6F 6E 20 61 6E 74 65 73 20 64 65 6C 20 74 65 78 74 6F 2E 20 45 6C 6C 61 3F 20 53 65 20 65 6E 74 69 65 6E 64 65 20 71 75 65 20 65 73 20 53 4D 3F 00", "Sister Madeline's level")
add_unique_code(conn, "00 80 1F 40 38 EA FF FF FF 70 00 6F 00 6E 00 ED 00 61 00 20 00 61 00 79 00 20 00 65 00 6E 00 20 00 76 00 65 00 7A 00 20 00 64 00 65 00 20 00 61 00 74 00 00 00", "I didn't get the achievement?")
add_unique_code(conn, "80 1F 40 38 24 00 00 00 45 78 70 6C 69 63 61 72 20 63 6F 6D 6F 20 73 65 20 61 62 72 65 20 65 6C 20 70 68 6F 74 6F 6D 6F 64 65 3F 00", "Photo Mode Explained")
add_unique_code(conn, "80 1F 40 38 22 00 00 00 54 6F 64 61 76 69 61 20 6E 6F 20 73 65 20 6C 61 20 70 75 65 64 65 20 71 75 65 6D 61 72 20 6E 6F 3F 00", "You still can't burn it, right?")
add_unique_code(conn, "80 1F FD 7F 12 00 00 00 57 68 79 20 45 61 72 6C 79 20 41 63 63 65 73 73 3F 00 31 01 00 00 00 00 00 00 80 1F 41 38", "Why Early Access?")
add_unique_code(conn, "80 1F FE 7F 10 00 00 00 53 4D 20 63 61 6E 74 75 72 72 65 61 6E 64 6F 00 06 02 00 00 00 00 00 00 80 1F 41 38", "SM humming")
add_unique_code(conn, "80 1F 40 38 19 00 00 00 54 6F 64 61 76 69 61 20 6E 6F 20 68 61 79 20 62 6F 6D 62 61 73 2E 2E 2E 00", "Still no bombs...")
add_unique_code(conn, "80 1F 40 38 18 00 00 00 4E 6F 20 73 65 20 6C 61 20 70 75 65 64 65 20 6D 61 74 61 72 2E 2E 2E 00", "You can't kill her...")
add_unique_code(conn, "80 1F 40 38 16 00 00 00 67 75 69 6F 6E 20 61 6E 74 65 73 20 64 65 6C 20 74 65 78 74 6F 00", "hyphen before text")
add_unique_code(conn, "80 1F 40 38 16 00 00 00 56 61 6D 6F 73 20 61 20 70 6F 6E 65 72 20 65 73 63 61 70 65 3F 00", "Are we going to put an exhaust?")
add_unique_code(conn, "80 1F 40 38 14 00 00 00 6E 6F 20 73 61 6C 65 20 65 6E 20 65 6C 20 6A 75 65 67 6F 00", "it doesn't appear in the game")
add_unique_code(conn, "80 1F 40 38 F5 FF FF FF 31 00 BA 00 20 00 70 00 65 00 72 00 73 00 6F 00 6E 00 61 00 00 00", "Trying to escape")
add_unique_code(conn, "80 1F 40 38 F5 FF FF FF 61 00 F1 00 61 00 64 00 69 00 72 00 20 00 22 00 3A 00 22 00 00 00", "Your name")
add_unique_code(conn, "80 1F 40 38 12 00 00 00 4D 69 72 61 20 68 61 63 69 61 20 61 72 72 69 62 61 00", "Look up")
add_unique_code(conn, "80 1F 40 38 10 00 00 00 43 6F 6D 65 6E 74 61 72 20 43 61 72 6C 6F 73 00", "Comment Carlos")
add_unique_code(conn, "00 1F 11 00 00 00 4E 6F 20 73 61 6C 65 20 65 6E 20 45 4E 54 42 4D 00", "It does not appear in ENTBM")
add_unique_code(conn, "80 1F 40 38 0C 00 00 00 4B 65 79 20 62 6F 72 72 61 64 61 00", "Blurred key")
add_unique_code(conn, "00 1F 0D 00 00 00 51 75 69 74 61 72 20 70 75 6E 74 6F 00", "Remove point")
add_unique_code(conn, "80 1F 40 38 0B 00 00 00 45 73 20 72 65 6A 69 6C 6C 61 00", "It's vent")
add_unique_code(conn, "80 1F 40 38 0A 00 00 00 4E 75 65 76 61 20 4B 65 79 00", "New Key")
add_unique_code(conn, "80 1F 40 38 08 00 00 00 54 6F 20 73 6B 69 70 00", "Skip Cutscene")
add_unique_code(conn, "80 1F 01 00", "UI-Menu")
add_unique_code(conn, "80 1F 01 20", "Photo Mode")
add_unique_code(conn, "80 1F 41 38", "Dialogue & Subtitles")

# Temukan dan proses semua file .uasset.txt di direktori yang sama
for filename in os.listdir():
    if filename.endswith('.uasset.txt'):
        process_file(filename, conn)
