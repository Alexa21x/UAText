import os
import sys

def uasset_to_hex(uasset_file):
    print(f"Converting .uasset: {uasset_file}")
    try:
        with open(uasset_file, 'rb') as f:
            data = f.read()
        hex_data = data.hex()
        print("Conversion to hex successful")
        return hex_data
    except Exception as e:
        print(f"Error: Failed to convert .uasset: {e}")

def hex_to_uasset(hex_data, uasset_file):
    print(f"Converting to .uasset: {uasset_file}")
    try:
        binary_data = bytes.fromhex(hex_data)
        with open(uasset_file, 'wb') as f:
            f.write(binary_data)
        print("Conversion to .uasset successful")
    except Exception as e:
        print(f"Error: Failed to convert .txt to .uasset: {e}")

def process_file(file_path):
    if file_path.endswith('.uasset'):
        hex_data = uasset_to_hex(file_path)
        if hex_data is not None:
            txt_file_path = file_path + '.txt'
            with open(txt_file_path, 'w') as f:
                f.write(hex_data)
            print(f"Converted to: {txt_file_path}")
    elif file_path.endswith('_hex.txt'):
        try:
            with open(file_path, 'r') as f:
                hex_data = f.read()
            uasset_file = os.path.splitext(file_path)[0].replace('_hex', '_NEW') + '.uasset'
            hex_to_uasset(hex_data, uasset_file)
            print(f"Converted to: {uasset_file}")
        except Exception as e:
            print(f"Error: Failed to read .txt file: {e}")
    else:
        print("Invalid file type. Please provide a .uasset or .txt file.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        hex_files = [f for f in os.listdir('.') if f.endswith('_hex.txt')]
        if hex_files:
            file_path = hex_files[0]
            print(f"Automatically found and processing: {file_path}")
            process_file(file_path)
        else:
            print("Please provide the path of the .uasset or .txt file to convert.")
    else:
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            process_file(file_path)
        else:
            print("File not found. Please check the file path and try again.")
