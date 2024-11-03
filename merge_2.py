import os

# Mengembalikan urutan hex yang telah diformat kembali ke bentuk aslinya
def unformat_hex_data(formatted_data):
    return formatted_data.replace(' ', '').lower()

# Mengembalikan urutan spesial ke bentuk aslinya
def restore_special_sequences(formatted_data):
    formatted_data = formatted_data.replace('46 08 46 08', '0A 00 0A 00')
    formatted_data = formatted_data.replace('F7 09 5E 00', '7C 00 20 00')
    formatted_data = formatted_data.replace('FF 5E 00', 'FF 20 00')
    formatted_data = formatted_data.replace('00 7C 09', '00 7C 00')
    formatted_data = formatted_data.replace('46 08', '0A 00')
    return formatted_data

# Fungsi untuk menghapus newline agar data hasil pemulihan berada pada satu baris
def remove_newlines(data):
    return data.replace('\n', '').replace('\r', '')

# Fungsi untuk memproses file input
def process_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            formatted_data = f.read().strip()
        
        formatted_data = restore_special_sequences(formatted_data)
        restored_data = unformat_hex_data(formatted_data)
        
        restored_data = remove_newlines(restored_data)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(restored_data)

        print(f"Restored data saved to: {output_file}")
        
    except Exception as e:
        print(f"Failed to process file {input_file}: {e}")

# Main execution
def main():
    for filename in os.listdir():
        if filename.endswith('_encode.txt'):
            input_file = filename
            output_file = filename.replace('_encode.txt', '_p.txt')
            print(f"Processing file: {input_file} -> {output_file}")
            process_file(input_file, output_file)
            os.remove(input_file)
            print(f"Input file '{input_file}' has been deleted after processing.")

if __name__ == "__main__":
    main()
