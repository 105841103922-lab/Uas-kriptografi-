"""
================================================
  APLIKASI ENKRIPSI FILE MENGGUNAKAN AES
================================================
  Nama  : SULTAN ALWI MAULANA H
  NIM   : 105841103922
  Materi: DES dan AES, Implementasi AES Python
================================================
"""

import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


# ─────────────────────────────────────────────
#  FUNGSI UTAMA
# ─────────────────────────────────────────────

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Menghasilkan kunci AES 256-bit dari password menggunakan PBKDF2-HMAC-SHA256.
    PBKDF2 (Password-Based Key Derivation Function 2) memperkuat password
    dengan iterasi hash sebanyak 100.000 kali sehingga tahan brute-force.
    """
    key = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=salt,
        iterations=100_000,
        dklen=32  # 32 byte = 256 bit
    )
    return key


def encrypt_file(input_path: str, output_path: str, password: str) -> dict:
    """
    Mengenkripsi file menggunakan AES-256 mode CBC.

    Struktur file terenkripsi:
      [SALT 16 byte][IV 16 byte][CIPHERTEXT]

    Returns dict berisi info proses enkripsi.
    """
    # 1. Baca file asli
    with open(input_path, 'rb') as f:
        plaintext = f.read()

    # 2. Buat salt acak & turunkan kunci dari password
    salt = get_random_bytes(16)
    key  = derive_key(password, salt)

    # 3. Buat IV (Initialization Vector) acak
    iv = get_random_bytes(16)

    # 4. Enkripsi dengan AES-CBC + PKCS7 padding
    cipher     = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    # 5. Tulis: SALT + IV + CIPHERTEXT
    with open(output_path, 'wb') as f:
        f.write(salt + iv + ciphertext)

    return {
        'ukuran_asli'      : len(plaintext),
        'ukuran_terenkripsi': len(ciphertext),
        'salt_hex'         : salt.hex(),
        'iv_hex'           : iv.hex(),
        'panjang_kunci_bit': len(key) * 8,
    }


def decrypt_file(input_path: str, output_path: str, password: str) -> dict:
    """
    Mendekripsi file yang sudah dienkripsi dengan encrypt_file().

    Returns dict berisi info proses dekripsi.
    """
    with open(input_path, 'rb') as f:
        data = f.read()

    # 1. Pisahkan SALT, IV, dan CIPHERTEXT
    salt       = data[:16]
    iv         = data[16:32]
    ciphertext = data[32:]

    # 2. Turunkan kunci yang sama dari password + salt
    key = derive_key(password, salt)

    # 3. Dekripsi AES-CBC lalu hapus padding
    cipher    = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    # 4. Tulis file hasil dekripsi
    with open(output_path, 'wb') as f:
        f.write(plaintext)

    return {
        'ukuran_ciphertext': len(ciphertext),
        'ukuran_hasil'     : len(plaintext),
    }


# ─────────────────────────────────────────────
#  DEMO / PENGUJIAN
# ─────────────────────────────────────────────

def cetak_separator(judul: str = ""):
    lebar = 55
    print("\n" + "═" * lebar)
    if judul:
        print(f"  {judul}")
        print("═" * lebar)


def demo():
    # ── Buat file TXT contoh ──────────────────────────────────
    isi_asli = (
        "Nama  : SULTAN ALWI MAULANA H\n"
        "NIM   : 105841103922\n\n"
        "Ini adalah file contoh yang akan dienkripsi\n"
        "menggunakan algoritma AES-256 mode CBC.\n\n"
        "Data sensitif:\n"
        "  - Nilai UTS   : 95\n"
        "  - Nilai UAS   : 90\n"
        "  - IPK         : 3.90\n"
    )

    file_asli       = "dokumen_asli.txt"
    file_enkripsi   = "dokumen_enkripsi.bin"
    file_dekripsi   = "dokumen_dekripsi.txt"
    password        = "Sultan@Secure2024"

    with open(file_asli, 'w') as f:
        f.write(isi_asli)

    # ── Tampilkan info ──────────────────────────────────────
    cetak_separator("APLIKASI ENKRIPSI FILE AES-256 CBC")
    print(f"  Nama  : SULTAN ALWI MAULANA H")
    print(f"  NIM   : 105841103922")

    cetak_separator("1. ISI FILE SEBELUM ENKRIPSI")
    print(isi_asli)

    # ── Enkripsi ────────────────────────────────────────────
    cetak_separator("2. PROSES ENKRIPSI")
    info_enc = encrypt_file(file_asli, file_enkripsi, password)
    print(f"  File input    : {file_asli}")
    print(f"  File output   : {file_enkripsi}")
    print(f"  Password      : {password}")
    print(f"  Algoritma     : AES-256 mode CBC")
    print(f"  Panjang kunci : {info_enc['panjang_kunci_bit']} bit")
    print(f"  SALT (hex)    : {info_enc['salt_hex']}")
    print(f"  IV (hex)      : {info_enc['iv_hex']}")
    print(f"  Ukuran asli   : {info_enc['ukuran_asli']} byte")
    print(f"  Ukuran enc    : {info_enc['ukuran_terenkripsi']} byte")

    # Tampilkan 32 byte pertama ciphertext sebagai representasi
    with open(file_enkripsi, 'rb') as f:
        raw = f.read()
    print(f"\n  Cuplikan file terenkripsi (32 byte pertama setelah SALT+IV):")
    print(f"  {raw[32:64].hex()}")

    # ── Dekripsi ────────────────────────────────────────────
    cetak_separator("3. PROSES DEKRIPSI")
    info_dec = decrypt_file(file_enkripsi, file_dekripsi, password)
    print(f"  File input    : {file_enkripsi}")
    print(f"  File output   : {file_dekripsi}")
    print(f"  Ukuran enc    : {info_dec['ukuran_ciphertext']} byte")
    print(f"  Ukuran hasil  : {info_dec['ukuran_hasil']} byte")

    cetak_separator("4. ISI FILE SETELAH DEKRIPSI")
    with open(file_dekripsi, 'r') as f:
        isi_dekripsi = f.read()
    print(isi_dekripsi)

    # ── Verifikasi ──────────────────────────────────────────
    cetak_separator("5. VERIFIKASI INTEGRITAS")
    cocok = isi_asli == isi_dekripsi
    print(f"  File asli == File dekripsi : {'✔  IDENTIK' if cocok else '✘  BERBEDA'}")

    # ── Uji password salah ──────────────────────────────────
    cetak_separator("6. UJI PASSWORD SALAH")
    try:
        decrypt_file(file_enkripsi, "gagal.txt", "password_salah")
        print("  Hasil: Berhasil didekripsi (tidak seharusnya!)")
    except Exception as e:
        print(f"  Hasil: Dekripsi GAGAL — {type(e).__name__}")
        print(f"  Pesan : {e}")
        print("  ✔  Password salah ditolak dengan benar")

    cetak_separator()
    print()


if __name__ == "__main__":
    demo()
