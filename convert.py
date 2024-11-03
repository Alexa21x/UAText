import os
import sys

def uasset_to_hex(file_path):
    print(f"Converting file to hex: {file_path}")
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        hex_data = data.hex()
        print("Conversion to hex successful")
        return hex_data
    except Exception as e:
        print(f"Error: Failed to convert file to hex: {e}")

def hex_to_uasset(hex_data, output_file):
    print(f"Converting hex to file: {output_file}")
    try:
        binary_data = bytes.fromhex(hex_data)
        with open(output_file, 'wb') as f:
            f.write(binary_data)
        print("Conversion to binary file successful")
    except Exception as e:
        print(f"Error: Failed to convert hex to binary file: {e}")

def process_file(file_path):
    # Memproses file .uasset atau .bin menjadi file .txt
    if file_path.endswith('.uasset') or file_path.endswith('.bin'):
        hex_data = uasset_to_hex(file_path)
        if hex_data is not None:
            txt_file_path = file_path + '.txt'
            with open(txt_file_path, 'w') as f:
                f.write(hex_data)
            print(f"Converted to: {txt_file_path}")
    
    # Memproses file .txt menjadi file .uasset atau .bin
    elif file_path.endswith('_hex.txt') or file_path.endswith('_decrypt_p.txt'):
        try:
            with open(file_path, 'r') as f:
                hex_data = f.read()
            
            # Menentukan output berdasarkan nama file
            if file_path.endswith('_hex.txt'):
                output_file = os.path.splitext(file_path)[0].replace('_hex', '_NEW') + '.uasset'
            elif file_path.endswith('_decrypt_p.txt'):
                output_file = os.path.splitext(file_path)[0].replace('_decrypt_p', '_decrypt_NEW') + '.bin'
            
            hex_to_uasset(hex_data, output_file)
            print(f"Converted to: {output_file}")
        except Exception as e:
            print(f"Error: Failed to read .txt file: {e}")
    else:
        print("Invalid file type. Please provide a .uasset, .bin, or .txt file.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Mencari file yang berakhiran _hex.txt atau _decrypt_p.txt
        txt_files = [f for f in os.listdir('.') if f.endswith('_hex.txt') or f.endswith('_decrypt_p.txt')]
        if txt_files:
            file_path = txt_files[0]
            print(f"Automatically found and processing: {file_path}")
            process_file(file_path)
        else:
            print("Please provide the path of the .uasset, .bin, or .txt file to convert.")
    else:
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            process_file(file_path)
        else:
            print("File not found. Please check the file path and try again.")
