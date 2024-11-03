import os
import sys
import subprocess

def find_file(suffix):
    directory = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
    print(f"Memeriksa direktori: {directory} untuk file {suffix}")
    
    try:
        print(f"Isi direktori: {os.listdir(directory)}")
    except FileNotFoundError:
        print(f"Direktori tidak ditemukan: {directory}")
        return None
    
    return next((os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(suffix)), None)

def run_script(script_name, *args):
    try:
        script_path = os.path.join(sys._MEIPASS, script_name) if getattr(sys, 'frozen', False) else script_name
        command = ["python", script_path, *args]
        
        print(f"Executing command: {command}")
        subprocess.run(command, check=True, text=True)
        print(f"Sukses menjalankan {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error menjalankan {script_name}: {e}")

def run_encode():
    print("Memulai proses encode...")
    for suffix, scripts in {
        "_uasset_decode.txt": ["encode.py", "merge_1.py", "convert.py"],
        "_decrypt_decode.txt": ["encode.py", "merge_2.py", "convert.py"]
    }.items():
        file_path = find_file(suffix)
        if file_path:
            print(f"File {suffix} ditemukan: {file_path}")
            for script in scripts:
                if script == "convert.py":
                    # Cari file input .txt yang dihasilkan dan berikan ke convert.py
                    txt_file = next((os.path.join(os.path.dirname(file_path), f) 
                                     for f in os.listdir(os.path.dirname(file_path)) 
                                     if f.endswith("_hex.txt") or f.endswith("_decrypt_p.txt")), None)
                    run_script(script, txt_file) if txt_file else print("File .txt untuk convert.py tidak ditemukan.")
                else:
                    run_script(script, file_path if script == "encode.py" else "")
            print(f"Proses untuk {suffix} selesai.")
        else:
            print(f"File {suffix} tidak ditemukan di direktori script.")

    directory = os.path.dirname(find_file("_uasset_decode.txt") or find_file("_decrypt_decode.txt") or "")
    for suffix in ["_hex.txt", "_decrypt_p.txt"]:
        for file_name in filter(lambda f: f.endswith(suffix), os.listdir(directory)):
            delete_file(os.path.join(directory, file_name))

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")

if __name__ == "__main__":
    run_encode()
