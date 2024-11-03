import re
import sys

def encode_text_segment(text):
    """Mengencode teks menjadi format hex dengan tambahan byte di depan."""
    hex_bytes = []
    for char in text:
        unicode_val = format(ord(char), '04x')
        reversed_pair = unicode_val[2:] + unicode_val[:2]
        hex_bytes.extend([reversed_pair[:2].upper(), reversed_pair[2:].upper()])
    hex_bytes.extend(['00', '00'])  # Tambah '00 00' di akhir

    byte_length = len(hex_bytes) // 2
    length_bytes = 65536 - byte_length
    length_hex = format(length_bytes, '04x').upper()
    reversed_length_bytes = length_hex[2:] + length_hex[:2]

    return [reversed_length_bytes[:2], reversed_length_bytes[2:], 'FF', 'FF'] + hex_bytes

def process_line(line):
    """Memproses setiap baris dari input untuk menghasilkan output sesuai spesifikasi."""
    result = []
    
    # Jika ada kode khusus [B=n]
    if '[B=' in line:
        match = re.search(r'\[B=(\d+)\]', line)
        if match:
            num_zero_bytes = int(match.group(1))
            result.extend(['00'] * num_zero_bytes)  # Tambah n byte 00
            # Hentikan pemrosesan lebih lanjut pada bagian ini
            return " ".join(result)

    # Proses bagian sebelum dan sesudah tanda "|"
    if "|" in line:
        parts = line.split("|")
        
        # Ambil 4 byte awal
        initial_bytes = parts[0].strip()
        result.extend(initial_bytes.split(" "))

        # Proses tiap bagian setelah tanda "|"
        for part in parts[1:]:
            encoded_part = encode_text_segment(part.strip())
            result.extend(encoded_part)

    else:
        result.extend(line.strip().split(" ") + ['00', '00'])

    return " ".join(result)

def recover_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    result = []
    for line in lines:
        processed_line = process_line(line.strip())
        result.append(processed_line)

    # Menyimpan hasil output ke file
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in result:
            file.write(line + "\n")

# Main execution
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = input_file.replace('_decrypt_decode.txt', '_decrypt_encode.txt')
        recover_data(input_file, output_file)
        print(f"File output disimpan di: {output_file}")
    else:
        print("Nama file input tidak diberikan.")
