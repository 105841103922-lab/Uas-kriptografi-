# 🔐 AES File Encryptor

Aplikasi enkripsi dan dekripsi file menggunakan **AES-256 mode CBC** berbasis Python.

> **UTS Keamanan Sistem Informasi**  
> Nama  : Sultan Alwi Maulana H  
> NIM   : 105841103922  

---

## 📋 Fitur

- ✅ Enkripsi file (TXT / PDF / DOCX)
- ✅ Dekripsi file dengan password yang sama
- ✅ Kunci 256-bit diturunkan dari password via **PBKDF2-HMAC-SHA256**
- ✅ Salt & IV acak setiap enkripsi (mencegah rainbow table attack)
- ✅ Validasi password — password salah langsung ditolak

---

## 🛠️ Teknologi

| Komponen | Detail |
|---|---|
| Bahasa | Python 3.8+ |
| Library | `pycryptodome` |
| Algoritma | AES-256 |
| Mode | CBC (Cipher Block Chaining) |
| Padding | PKCS7 |
| KDF | PBKDF2-HMAC-SHA256 (100.000 iterasi) |

---

## 📁 Struktur Repositori

```
105841103922/
├── .gitignore
├── README.md
├── aes_enkripsi.py      ← source code utama
├── contoh_file.txt      ← file sample untuk pengujian
└── requirements.txt     ← dependensi Python
```

---

## 🚀 Cara Penggunaan

### 1. Clone repositori

```bash
git clone https://github.com/105841103922/105841103922.git
cd 105841103922
```

### 2. Install dependensi

```bash
pip install -r requirements.txt
```

### 3. Jalankan demo otomatis

```bash
python aes_enkripsi.py
```

Program akan otomatis:
- Membuat file contoh `dokumen_asli.txt`
- Mengenkripsi → `dokumen_enkripsi.bin`
- Mendekripsi → `dokumen_dekripsi.txt`
- Verifikasi kecocokan file
- Menguji penolakan password salah

### 4. Gunakan fungsi secara langsung

```python
from aes_enkripsi import encrypt_file, decrypt_file

# Enkripsi
encrypt_file("data_saya.txt", "data_saya.enc", password="RahasiaKuat123!")

# Dekripsi
decrypt_file("data_saya.enc", "data_pulih.txt", password="RahasiaKuat123!")
```

---

## 🔑 Cara Kerja Enkripsi

```
Password ──┐
           ├── PBKDF2-HMAC-SHA256 (+ SALT acak) ──► KEY 256-bit
SALT acak ─┘                                           │
                                                       ▼
Plaintext ──────────────────────────────────── AES-256-CBC ──► Ciphertext
                                                   ▲
                                               IV acak (16B)

File output: [ SALT 16B ][ IV 16B ][ CIPHERTEXT ]
```

### Langkah detail:
1. **PBKDF2** mengubah password menjadi kunci 256-bit yang kuat (dengan salt acak)
2. **IV acak** dibuat untuk setiap enkripsi agar ciphertext selalu unik
3. **Plaintext** di-*pad* dengan PKCS7 agar panjangnya kelipatan 16 byte
4. **AES-CBC** mengenkripsi blok demi blok, tiap blok di-XOR dengan ciphertext sebelumnya
5. Output disimpan sebagai: `SALT + IV + CIPHERTEXT`

---

## 🧪 Contoh Output

```
═══════════════════════════════════════════════════════
  PROSES ENKRIPSI
═══════════════════════════════════════════════════════
  Algoritma     : AES-256 mode CBC
  Panjang kunci : 256 bit
  SALT (hex)    : ad6b8656f702104ee06d3e43ef870a3c
  IV (hex)      : 8e41a6753d54647c486cf237123e115a
  Ukuran asli   : 217 byte
  Ukuran enc    : 224 byte

═══════════════════════════════════════════════════════
  VERIFIKASI INTEGRITAS
═══════════════════════════════════════════════════════
  File asli == File dekripsi : ✔  IDENTIK

═══════════════════════════════════════════════════════
  UJI PASSWORD SALAH
═══════════════════════════════════════════════════════
  Hasil: Dekripsi GAGAL — ValueError: Padding is incorrect.
  ✔  Password salah ditolak dengan benar
```

---

## ⚠️ Catatan Keamanan

- Jangan hardcode password di dalam script
- Simpan file `.enc` dan password di tempat terpisah
- Untuk keamanan lebih tinggi, pertimbangkan **AES-256-GCM** (menambahkan autentikasi data)

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik (UTS Keamanan Sistem Informasi).
