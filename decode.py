import os
import re

def get_value(bytes_list):
    if len(bytes_list) < 4:
        return None, None
    if bytes_list[2:4] == [0, 0]:  # Type A
        return (bytes_list[1] * 256) + bytes_list[0], 'A'
    elif bytes_list[2:4] == [255, 255]:  # Type B
        B = (bytes_list[1] * 256) + bytes_list[0]
        return (65536 - B) * 2, 'B'
    return None, None

def decode_type_a(hex_bytes):
    return ''.join(chr(int(byte, 16)) for byte in hex_bytes).strip('\x00')

def decode_type_b(hex_bytes):
    unicode_chars = ''.join(
        chr(int(hex_bytes[i + 1] + hex_bytes[i], 16)) for i in range(0, len(hex_bytes) - 1, 2)
    )
    return unicode_chars.rstrip('\x00')

def is_8_byte_sequence(bytes_list):
    if len(bytes_list) >= 8:
        if bytes_list[-6:] == [0x00] * 6:
            return True
    return False

def extract_parts_uasset(hex_bytes, num_parts=14):
    parts = []
    while len(hex_bytes) > 8 and len(parts) < num_parts:
        bytes_list = [int(byte, 16) for byte in hex_bytes[:4]]
        value, type_ = get_value(bytes_list)
        if value is not None:
            part = hex_bytes[4:4 + value]
            hex_bytes = hex_bytes[4 + value:]

            if type_ == 'A':
                decoded = decode_type_a(part)
            elif type_ == 'B':
                decoded = decode_type_b(part)
            else:
                decoded = 'Unknown'

            parts.append((type_, decoded))
        else:
            break

    if is_8_byte_sequence([int(byte, 16) for byte in hex_bytes[-8:]]):
        remaining = hex_bytes[-8:]
    else:
        remaining = hex_bytes

    return parts, remaining

def extract_parts_bin(hex_data):
    parts = []
    i = 0
    while i <= len(hex_data) - 4:
        bytes_list = [int(hex_data[i + j], 16) for j in range(4)]
        value, type_ = get_value(bytes_list)

        if type_ == 'A':
            i += 4
            b_parts = []
            while i <= len(hex_data) - 4:
                b_bytes_list = [int(hex_data[i + j], 16) for j in range(4)]
                b_value, b_type = get_value(b_bytes_list)

                if b_type == 'B' and b_value:
                    b_part = hex_data[i + 4:i + 4 + b_value]
                    i += 4 + b_value
                    b_parts.append(decode_type_b(b_part))
                else:
                    break

            if b_parts:
                parts.append((bytes_list, b_parts))
        else:
            i += 4  # Skip non-Type A bytes

    special_code = re.search(r'\[B=(\d+)\]', ' '.join(hex_data[i:]))
    return parts, special_code.group(0) if special_code else None

def process_uasset_data(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    result = []
    hex_data = []
    
    def process_hex_data(hex_data):
        title = hex_data.pop(0)
        result.append(title)
        hex_bytes = ' '.join(hex_data).split()
        parts, remaining = extract_parts_uasset(hex_bytes)
        part_strs = [f'[{t}] {d}' for t, d in parts]
        result.append('|'.join(part_strs) + (f'|{" ".join(remaining)}' if remaining else ''))

    for line in lines:
        line = line.strip()
        if line.startswith('"'):
            if hex_data:
                process_hex_data(hex_data)
            hex_data = [line]
        elif line:
            hex_data.append(line)

    if hex_data:
        process_hex_data(hex_data)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(result))

def process_bin_data(input_file, output_file):
    with open(input_file, 'r') as file:
        hex_data = [byte for line in file for byte in line.strip().split()]

    parts, special_code = extract_parts_bin(hex_data)

    with open(output_file, 'w', encoding='utf-8') as file:
        for bytes_list, decoded_parts in parts:
            decoded_string = ' | '.join(decoded_parts)
            file.write(f"{' '.join(f'{byte:02X}' for byte in bytes_list)} | {decoded_string}\n")
        if special_code:
            file.write(f"{special_code}\n")

def process_files():
    for filename in os.listdir():
        if filename.endswith('.uasset_formatted.txt'):
            input_file = filename
            output_file = filename.replace('.uasset_formatted.txt', '_uasset_decode.txt')
            print(f"Processing .uasset file: {input_file} -> {output_file}")
            process_uasset_data(input_file, output_file)
            os.remove(input_file)
            print(f"Input file '{input_file}' has been deleted after processing.")
        elif filename.endswith('.bin_formatted.txt'):
            input_file = filename
            output_file = filename.replace('.bin_formatted.txt', '_decode.txt')
            print(f"Processing .bin file: {input_file} -> {output_file}")
            process_bin_data(input_file, output_file)
            os.remove(input_file)
            print(f"Input file '{input_file}' has been deleted after processing.")

# Jalankan proses
process_files()
