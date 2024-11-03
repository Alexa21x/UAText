import os
import sys
import subprocess

def find_file_with_extension(extension):
    directory = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
    print(f"Memeriksa direktori: {directory}")
    
    try:
        print(f"Isi direktori: {os.listdir(directory)}")
    except FileNotFoundError:
        print(f"Direktori tidak ditemukan: {directory}")
        return None
    
    return next((os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)), None)

def run_script(script_name, *args):
    try:
        script_path = os.path.join(sys._MEIPASS, script_name) if getattr(sys, 'frozen', False) else script_name
        command = ["python", script_path, *args]
        
        print(f"Executing command: {command}")
        subprocess.run(command, check=True, text=True)
        print(f"Sukses menjalankan {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error menjalankan {script_name}: {e}")

def run_decode():
    print("Memulai proses decode...")
    for ext, scripts in {".uasset": ["convert.py", "separate_1.py", "decode.py"], 
                         ".bin": ["convert.py", "separate_2.py", "decode.py"]}.items():
        file_path = find_file_with_extension(ext)
        if file_path:
            print(f"File {ext} ditemukan: {file_path}")
            for script in scripts:
                run_script(script, file_path if script == "convert.py" else "")
            print(f"Proses decode untuk {ext} selesai.")
            return
    print("File .uasset atau .bin tidak ditemukan di direktori script.")

if __name__ == "__main__":
    run_decode()
