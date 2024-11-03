import os
import sys

def encode_type_a(decoded_str):
    # Encode string back to hex as ASCII, including trailing spaces
    # Add '00 00' at the start and '00' at the end
    hex_bytes = [format(ord(char), '02x').upper() for char in decoded_str]
    hex_bytes.append('00')  # Add extra '00' byte at the end
    
    # Calculate the byte length (excluding the leading '00 00')
    byte_length = len(hex_bytes)
    length_bytes = format(byte_length, '04x').upper()  # Convert length to 4 hex digits
    reversed_length_bytes = length_bytes[2:] + length_bytes[:2]  # Reverse the byte order

    # Add '00 00' at the front and the reversed length bytes
    return [reversed_length_bytes[:2], reversed_length_bytes[2:], '00', '00'] + hex_bytes

def encode_type_b(decoded_str):
    hex_bytes = []
    for char in decoded_str:
        # Encode character back to Unicode hex
        unicode_val = format(ord(char), '04x')
        reversed_pair = unicode_val[2:] + unicode_val[:2]  # Reverse the byte order
        hex_bytes.extend([reversed_pair[:2].upper(), reversed_pair[2:].upper()])
    hex_bytes.extend(['00', '00'])  # Add extra '00 00' bytes at the end

    # Calculate the byte length (excluding the leading 'FF FF')
    byte_length = len(hex_bytes)
    length_bytes = 65536 - (byte_length // 2)  # Calculate the special length value
    length_hex = format(length_bytes, '04x').upper()  # Convert length to 4 hex digits
    reversed_length_bytes = length_hex[2:] + length_hex[:2]  # Reverse the byte order

    # Add 'FF FF' at the front and the reversed length bytes
    return [reversed_length_bytes[:2], reversed_length_bytes[2:], 'FF', 'FF'] + hex_bytes

def restore_parts(parts, remaining):
    restored_hex = []
    for type_, decoded in parts:
        if type_ == 'A':
            # Restore ASCII with byte length indicator and '00 00' at the start
            restored_hex.extend(encode_type_a(decoded))
        elif type_ == 'B':
            # Restore Unicode with byte length indicator and 'FF FF' at the start
            restored_hex.extend(encode_type_b(decoded))
        else:
            continue
    restored_hex.extend(remaining)
    return restored_hex

def recover_data(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    result = []
    for line in lines:
        line = line.strip()
        if line.startswith('"'):
            # Treat this as a title or identifier
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

    # Write the restored hex data to output file using utf-8 encoding
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in result:
            file.write(line + '\n')

# Main execution
if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = input_file.replace('_uasset_decode.txt', '_encode.txt')
        recover_data(input_file, output_file)
        print(f"File output disimpan di: {output_file}")
    else:
        print("Nama file input tidak diberikan.")
