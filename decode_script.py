import os
import sys
import subprocess

def find_uasset_file():
    # Dapatkan direktori dari executable
    if getattr(sys, 'frozen', False):
        directory = os.path.dirname(os.path.abspath(sys.executable))  # Menggunakan sys.executable untuk mendapatkan jalur yang benar
    else:
        directory = os.path.dirname(os.path.abspath(__file__))

    # Debug print untuk melihat isi direktori
    print(f"Memeriksa direktori: {directory}")

    if directory:  # Pastikan direktori tidak kosong
        try:
            print(f"Isi direktori: {os.listdir(directory)}")  # Menampilkan isi direktori
        except FileNotFoundError:
            print(f"Direktori tidak ditemukan: {directory}")
            return None
    else:
        print("Direktori kosong, tidak dapat mencari file .uasset.")
        return None

    for file_name in os.listdir(directory):
        if file_name.endswith(".uasset"):
            return os.path.join(directory, file_name)
    return None

def run_script(script_name, *args):
    try:
        if getattr(sys, 'frozen', False):
            script_path = os.path.join(sys._MEIPASS, script_name)
        else:
            script_path = script_name

        # Jika di dalam executable, jalankan langsung dengan python.exe
        command = ["python", script_path] + list(args)
        
        # Debug print command
        print(f"Executing command: {command}")

        subprocess.run(command, check=True, text=True)
        print(f"Sukses menjalankan {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error menjalankan {script_name}: {e}")

def run_decode():
    print("Memulai proses decode...")
    uasset_file_path = find_uasset_file()  # Panggil fungsi yang telah dimodifikasi

    if not uasset_file_path:
        print("File .uasset tidak ditemukan di direktori script.")
    else:
        print(f"File .uasset ditemukan: {uasset_file_path}")
        # Panggil run_script untuk menjalankan script lainnya
        run_script("convert.py", uasset_file_path)
        run_script("separate.py")
        run_script("decode.py")
        print("Proses decode selesai.")

if __name__ == "__main__":
    run_decode()  # Pastikan fungsi ini dipanggil