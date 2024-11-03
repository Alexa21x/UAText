import os
import sqlite3

# Inisialisasi database SQLite
def init_db():
    conn = sqlite3.connect('unique_codes.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS codes (code TEXT PRIMARY KEY, name TEXT NOT NULL)''')
    conn.commit()
    return conn

# Mendapatkan kode unik dari nama kode
def get_code_by_name(conn, name):
    cursor = conn.cursor()
    cursor.execute('SELECT code FROM codes WHERE name = ?', (name,))
    result = cursor.fetchone()
    return result[0] if result else None

# Mengembalikan urutan hex yang telah diformat kembali ke bentuk aslinya
def unformat_hex_data(formatted_data):
    return formatted_data.replace(' ', '').lower()

# Mengembalikan urutan spesial ke bentuk aslinya
def restore_special_sequences(formatted_data):
    formatted_data = formatted_data.replace('A6 A6', '0A 0A')
    formatted_data = formatted_data.replace('A6 00 A6 00', '0A 00 0A 00')
    formatted_data = formatted_data.replace('2E A6 00', '2E 0A 00')
    return formatted_data

# Mengembalikan kode unik ke bentuk hex aslinya
def restore_unique_codes(formatted_data, conn):
    cursor = conn.cursor()
    cursor.execute('SELECT name, code FROM codes')
    unique_codes = cursor.fetchall()
    
    for name, code in unique_codes:
        clean_name = name.strip()
        formatted_data = formatted_data.replace(f'"{clean_name}"', code)
    
    return formatted_data

# Mengembalikan jumlah byte setelah urutan byte tertentu, termasuk urutan tersebut
def count_bytes_after_sequence(data, sequence):
    bytes_data = bytes.fromhex(data)
    sequence_bytes = bytes.fromhex(sequence)
    position = bytes_data.find(sequence_bytes)

    if position != -1:
        count = len(bytes_data) - position
        return count
    return 0

# Fungsi untuk mengubah jumlah byte menjadi 3 byte heksadesimal terbalik
def decimal_to_hex_reversed(decimal):
    hex_digits = []
    while decimal > 0:
        remainder = decimal % 16
        hex_digits.append(str(remainder) if remainder < 10 else chr(remainder - 10 + ord('A')))
        decimal //= 16
    hex_digits.reverse()
    hex_string = ''.join(hex_digits).zfill(6)
    return f"{hex_string[:2]} {hex_string[2:4]} {hex_string[4:]}"

# Fungsi untuk mengganti urutan C0 F7 13 dengan 3 byte baru
def replace_sequence_with_byte_count(data, sequence, new_bytes):
    bytes_data = bytes.fromhex(data)
    new_bytes_data = bytes.fromhex(new_bytes)
    sequence_bytes = bytes.fromhex(sequence)
    position = bytes_data.find(sequence_bytes)

    if position != -1:
        new_data = bytes_data[:position] + new_bytes_data + bytes_data[position + len(sequence_bytes):]
        return new_data.hex()
    return data

# Fungsi untuk menghapus newline agar data hasil pemulihan berada pada satu baris
def remove_newlines(data):
    return data.replace('\n', '').replace('\r', '')

# Fungsi untuk membalik urutan hex
def reverse_hex_sequence(hex_string):
    parts = hex_string.split()
    return ' '.join(reversed(parts))

# Fungsi untuk memproses file input
def process_file(input_file, output_file, conn):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            formatted_data = f.read().strip()
        
        formatted_data = restore_special_sequences(formatted_data)
        formatted_data = restore_unique_codes(formatted_data, conn)
        restored_data = unformat_hex_data(formatted_data)

        sequence_count = '00 03 FB FF FF FF'
        byte_count = count_bytes_after_sequence(restored_data, sequence_count)
        reversed_byte_count = reverse_hex_sequence(decimal_to_hex_reversed(byte_count))

        replace_sequence = 'C0 F7 13'
        restored_data = replace_sequence_with_byte_count(restored_data, replace_sequence, reversed_byte_count)
        
        restored_data = remove_newlines(restored_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(restored_data)

        print(f"Restored data saved to: {output_file}")
        
    except Exception as e:
        print(f"Failed to process file {input_file}: {e}")

# Main execution
def main():
    conn = init_db()
    for filename in os.listdir():
        if filename.endswith('_encode.txt'):
            input_file = filename
            output_file = filename.replace('_encode.txt', '_hex.txt')
            print(f"Processing file: {input_file} -> {output_file}")
            process_file(input_file, output_file, conn)
            os.remove(input_file)
            print(f"Input file '{input_file}' has been deleted after processing.")

if __name__ == "__main__":
    main()
