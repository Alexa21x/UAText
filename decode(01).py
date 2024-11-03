import os
import re

def get_value(bytes_list):
    if bytes_list[2:4] == [0, 0]:  # Type A
        return (bytes_list[1] << 8) + bytes_list[0], 'A'
    elif bytes_list[2:4] == [255, 255]:  # Type B
        B = (bytes_list[1] << 8) + bytes_list[0]
        return (65536 - B) * 2, 'B'
    return None, None

def decode_type_b(hex_bytes):
    unicode_chars = ''.join(
        chr(int(hex_bytes[i + 1] + hex_bytes[i], 16)) for i in range(0, len(hex_bytes) - 1, 2)
    )
    return unicode_chars.rstrip('\x00')

def extract_parts(hex_data):
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

def process_data(input_file, output_file):
    with open(input_file, 'r') as file:
        hex_data = [byte for line in file for byte in line.strip().split()]

    parts, special_code = extract_parts(hex_data)

    with open(output_file, 'w', encoding='utf-8') as file:
        for bytes_list, decoded_parts in parts:
            decoded_string = ' | '.join(decoded_parts)
            file.write(f"{' '.join(f'{byte:02X}' for byte in bytes_list)} | {decoded_string}\n")
        if special_code:
            file.write(f"{special_code}\n")

# Process all .bin_formatted.txt files
for filename in os.listdir():
    if filename.endswith('.bin_formatted.txt'):
        input_file = filename
        output_file = filename.replace('.bin_formatted.txt', '_decode.txt')
        print(f"Processing file: {input_file} -> {output_file}")
        process_data(input_file, output_file)
        os.remove(input_file)
        print(f"Input file '{input_file}' has been deleted after processing.")
