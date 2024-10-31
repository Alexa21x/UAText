import os

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
    unicode_chars = ''
    for i in range(0, len(hex_bytes) - 1, 2):
        pair = hex_bytes[i:i + 2]
        reversed_pair = pair[::-1]
        unicode_value = int(''.join(reversed_pair), 16)
        unicode_chars += chr(unicode_value)
    return unicode_chars.rstrip('\x00')

def is_8_byte_sequence(bytes_list):
    if len(bytes_list) >= 8:
        if bytes_list[-6:] == [0x00] * 6:
            return True
    return False

def extract_parts(hex_bytes, num_parts=14):
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

def process_data(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    result = []
    hex_data = []
    
    def process_hex_data(hex_data):
        title = hex_data.pop(0)
        result.append(title)
        hex_bytes = ' '.join(hex_data).split()
        parts, remaining = extract_parts(hex_bytes)
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

# Mencari dan memproses semua file .uasset_formatted.txt
for filename in os.listdir():
    if filename.endswith('.uasset_formatted.txt'):
        input_file = filename
        output_file = filename.replace('.uasset_formatted.txt', '_decode.txt')
        print(f"Processing file: {input_file} -> {output_file}")
        process_data(input_file, output_file)
        os.remove(input_file)
        print(f"Input file '{input_file}' has been deleted after processing.")
