import os
import re
import sys

def encode_type_a(decoded_str):
    """Mengencode string sebagai Type A dengan format hex ASCII dan tambahan byte panjang."""
    hex_bytes = [format(ord(char), '02x').upper() for char in decoded_str]
    hex_bytes.append('00')  # Tambahkan '00' di akhir
    
    # Hitung panjang byte (tidak termasuk '00 00' di awal)
    byte_length = len(hex_bytes)
    length_bytes = format(byte_length, '04x').upper()
    reversed_length_bytes = length_bytes[2:] + length_bytes[:2]  # Balik urutan byte
    
    return [reversed_length_bytes[:2], reversed_length_bytes[2:], '00', '00'] + hex_bytes

def encode_type_b(decoded_str):
    """Mengencode string sebagai Type B dengan format hex Unicode dan tambahan byte panjang."""
    hex_bytes = []
    for char in decoded_str:
        unicode_val = format(ord(char), '04x')
        reversed_pair = unicode_val[2:] + unicode_val[:2]  # Balik urutan byte
        hex_bytes.extend([reversed_pair[:2].upper(), reversed_pair[2:].upper()])
    hex_bytes.extend(['00', '00'])  # Tambahkan '00 00' di akhir
    
    # Hitung panjang byte (tidak termasuk 'FF FF' di awal)
    byte_length = len(hex_bytes)
    length_bytes = 65536 - (byte_length // 2)  # Perhitungan panjang khusus
    length_hex = format(length_bytes, '04x').upper()
    reversed_length_bytes = length_hex[2:] + length_hex[:2]  # Balik urutan byte
    
    return [reversed_length_bytes[:2], reversed_length_bytes[2:], 'FF', 'FF'] + hex_bytes

def encode_text_segment(text):
    """Mengencode teks menjadi format hex dengan tambahan byte di depan (seperti Type B)."""
    hex_bytes = []
    for char in text:
        unicode_val = format(ord(char), '04x')
        reversed_pair = unicode_val[2:] + unicode_val[:2]
        hex_bytes.extend([reversed_pair[:2].upper(), reversed_pair[2:].upper()])
    hex_bytes.extend(['00', '00'])
    
    byte_length = len(hex_bytes) // 2
    length_bytes = 65536 - byte_length
    length_hex = format(length_bytes, '04x').upper()
    reversed_length_bytes = length_hex[2:] + length_hex[:2]
    
    return [reversed_length_bytes[:2], reversed_length_bytes[2:], 'FF', 'FF'] + hex_bytes

def restore_parts(parts, remaining):
    restored_hex = []
    for type_, decoded in parts:
        if type_ == 'A':
            restored_hex.extend(encode_type_a(decoded))
        elif type_ == 'B':
            restored_hex.extend(encode_type_b(decoded))
    restored_hex.extend(remaining)
    return restored_hex

def process_line(line, is_decrypt_file=False):
    """Memproses setiap baris dari input berdasarkan tipe file."""
    result = []
    
    if '[B=' in line:
        match = re.search(r'\[B=(\d+)\]', line)
        if match:
            num_zero_bytes = int(match.group(1))
            result.extend(['00'] * num_zero_bytes)
            return " ".join(result)

    if "|" in line:
        parts = line.split("|")
        initial_bytes = parts[0].strip()
        result.extend(initial_bytes.split(" "))

        for part in parts[1:]:
            encoded_part = encode_text_segment(part.strip()) if is_decrypt_file else encode_type_b(part.strip())
            result.extend(encoded_part)
    else:
        result.extend(line.strip().split(" ") + ['00', '00'])

    return " ".join(result)

def recover_data(input_file, output_file):
    is_uasset_file = "_uasset_decode.txt" in input_file
    is_decrypt_file = "_decrypt_decode.txt" in input_file
    
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    result = []
    for line in lines:
        line = line.strip()
        if is_uasset_file:
            if line.startswith('"'):
                result.append(line)
            else:
                parts = []
                hex_data = line.split('|')
                for part in hex_data:
                    if part.startswith('[A]'):
                        parts.append(('A', part[4:]))
                    elif part.startswith('[B]'):
                        parts.append(('B', part[4:]))
                remaining = hex_data[-1].split() if len(hex_data[-1].split()) > 0 else []
                restored_hex = restore_parts(parts, remaining)
                result.append(' '.join(restored_hex))
        elif is_decrypt_file:
            processed_line = process_line(line, is_decrypt_file=True)
            result.append(processed_line)

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in result:
            file.write(line + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if "_uasset_decode.txt" in input_file:
            output_file = input_file.replace('_uasset_decode.txt', '_encode.txt')
        elif "_decrypt_decode.txt" in input_file:
            output_file = input_file.replace('_decrypt_decode.txt', '_decrypt_encode.txt')
        else:
            print("Format nama file input tidak dikenali.")
            sys.exit(1)

        recover_data(input_file, output_file)
        print(f"File output disimpan di: {output_file}")
    else:
        print("Nama file input tidak diberikan.")
