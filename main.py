import os
import sys
from decode_script import run_decode
from encode_script import run_encode

def main():
    # Setel direktori kerja ke lokasi executable
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))  # Ubah direktori ke lokasi UTEX.exe
    else:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Jalankan encode atau decode sesuai argumen
    if len(sys.argv) > 1 and sys.argv[1] == "-decode":
        run_decode()
    elif len(sys.argv) > 1 and sys.argv[1] == "-encode":
        run_encode()

if __name__ == "__main__":
    main()
