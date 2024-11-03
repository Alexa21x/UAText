import os

# Format data heksadesimal menjadi huruf besar dengan spasi di antara setiap dua karakter
def format_hex_data(hex_data):
    hex_data = hex_data.upper()
    formatted_data = ' '.join([hex_data[i:i + 2] for i in range(0, len(hex_data), 2)])
    return formatted_data

# Ganti urutan byte khusus
def replace_special_sequences(formatted_data):
    formatted_data = formatted_data.replace('0A 00 0A 00', '46 08 46 08')
    formatted_data = formatted_data.replace('7C 00 20 00', 'F7 09 5E 00')
    formatted_data = formatted_data.replace('FF 20 00', 'FF 5E 00')
    formatted_data = formatted_data.replace('00 7C 00', '00 7C 09')
    formatted_data = formatted_data.replace('0A 00', '46 08')
    return formatted_data

# Fungsi untuk mengganti trailing 00
def replace_trailing_zeros(formatted_data):
    while formatted_data.endswith('00'):
        count = 0
        # Hitung jumlah byte 00 di akhir data
        while formatted_data.endswith('00'):
            count += 1
            formatted_data = formatted_data[:-3]  # Menghapus '00' dan spasi sebelumnya
        
        if count >= 5:
            replacement = f' 00 00 00 [B={count - 3}]'
            formatted_data += replacement
            break  # Hentikan setelah mengganti
        
    return formatted_data

# Menghapus file input setelah diproses
def delete_input_file(file_path):
    try:
        os.remove(file_path)
        print(f"Input file {file_path} has been deleted.")
    except Exception as e:
        print(f"Failed to delete input file: {e}")

# Memproses file .txt
def process_file(file_path):
    if file_path.endswith('.txt'):
        try:
            with open(file_path, 'r') as f:
                hex_data = f.read().strip()
            formatted_data = format_hex_data(hex_data)
            formatted_data = replace_special_sequences(formatted_data)
            formatted_data = replace_trailing_zeros(formatted_data)  # Panggil fungsi baru
            
            output_file_path = os.path.splitext(file_path)[0] + '_formatted.txt'
            with open(output_file_path, 'w') as f:
                f.write(formatted_data)
            
            print(f"Formatted data saved to: {output_file_path}")
            
            # Hapus file input setelah proses selesai
            delete_input_file(file_path)

        except Exception as e:
            print(f"Failed to process file: {e}")

# Temukan dan proses semua file .bin.txt di direktori yang sama
for filename in os.listdir():
    if filename.endswith('.bin.txt'):
        process_file(filename)
