import os
import sys
import subprocess

def find_decode_file():
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
        print("Direktori kosong, tidak dapat mencari file _decode.txt.")
        return None

    for file_name in os.listdir(directory):
        if file_name.endswith("_decode.txt"):
            return os.path.join(directory, file_name)
    return None

def run_script(script_name, *args):
    try:
        if getattr(sys, 'frozen', False):
            script_path = os.path.join(sys._MEIPASS, script_name)  # Ambil dari direktori sementara
        else:
            script_path = script_name  # Jalur untuk mode pengembangan

        # Jika di dalam executable, jalankan langsung dengan python.exe
        command = ["python", script_path] + list(args)
        
        # Debug print command
        print(f"Executing command: {command}")

        subprocess.run(command, check=True, text=True)
        print(f"Sukses menjalankan {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error menjalankan {script_name}: {e}")

def run_encode():
    print("Memulai proses encode...")
    decode_file_path = find_decode_file()  # Mencari file _decode.txt

    if not decode_file_path:
        print("File _decode.txt tidak ditemukan di direktori script.")
    else:
        print(f"File _decode.txt ditemukan: {decode_file_path}")
        # Panggil run_script untuk menjalankan script lainnya
        run_script("encode.py", decode_file_path)
        run_script("merge.py")
        run_script("convert.py")
        print("Proses encode selesai.")

        # Mencari dan menghapus file yang diakhiri dengan '_hex.txt' di direktori
        directory = os.path.dirname(decode_file_path)
        for file_name in os.listdir(directory):
            if file_name.endswith("_hex.txt"):
                hex_file_path = os.path.join(directory, file_name)
                delete_hex_file(hex_file_path)

def delete_hex_file(hex_file):
    try:
        os.remove(hex_file)
        print(f"Deleted file: {hex_file}")
    except OSError as e:
        print(f"Error deleting file {hex_file}: {e}")

if __name__ == "__main__":
    run_encode()  # Pastikan fungsi ini dipanggil
