# Simulasi Otomasi Perlintasan Kereta Api & Manajemen Lalu Lintas 3D
Disusun untuk memenuhi tugas UAS mata kuliah Grafika Komputer
Proyek ini adalah simulasi ruang tiga dimensi (3D) berbasis OpenGL yang memodelkan sistem otomasi perlintasan sebidang kereta api dan manajemen arus lalu lintas di lingkungan pedesaan. Simulasi ini dirancang sebagai laboratorium virtual untuk menguji algoritma *Finite State Machine* (FSM) dan logika antrean kendaraan.

## Fitur Utama
* **Otomasi Palang Pintu (FSM):** Palang pintu beroperasi secara otonom berdasarkan posisi kereta, dilengkapi dengan lampu peringatan merah yang berkedip dinamis menggunakan kalkulasi gelombang sinus.
* **Manajemen Antrean Lalu Lintas:** Menggunakan algoritma *Leader-Follower* dan *simple collision detection* agar kendaraan mengerem dan mengantre dengan tertib tanpa saling menembus (*clipping*).
* **Sistem Kontrol Masinis (Persistent):** Kendali pergerakan kereta menggunakan model "sekali klik" layaknya panel masinis sungguhan.
* **Siklus Waktu Dinamis (Day/Night Cycle):** Transisi warna langit dan pencahayaan yang berjalan secara *real-time* dengan penyesuaian kecepatan laju waktu antara siang dan malam.
* **Kamera Bebas (Free-Roam Camera):** Eksplorasi dunia 3D dari segala sudut pandang.

## Tech Stack
* **Bahasa:** Python 3
* **Grafika:** PyOpenGL, ModernGL
* **Matematika Matriks:** PyGLM, Numpy
* **Jendela & Input:** Pygame-ce

## Cara Menjalankan Program

1. Pastikan Python 3 sudah terinstal di sistem.
2. Instal semua *library* yang dibutuhkan:
   ```bash
   pip install pygame-ce PyOpenGL ModernGL pyglm numpy
3. Jalankan program
   ```bash
   python main.py
   
## Panduan Kontrol (Interaksi Pengguna)
Sistem telah dioptimalkan dengan berbagai interaksi keyboard dan mouse untuk mengontrol simulasi secara penuh:

### Kontrol Kereta Api 
Sistem menggunakan kontrol persistent (tekan sekali, kereta akan terus berjalan/berhenti).

* 1 + A : Menjalankan Kereta 1 ke arah Kiri (Utara).
* 1 + D : Menjalankan Kereta 1 ke arah Kanan (Selatan).
* 1 + S : Menghentikan pergerakan Kereta 1 (Stop).
* Tekan 1 + S untuk menghentikan Kereta 1.
* Tekan 2 + S untuk menghentikan Kereta 2

### Navigasi Kamera Bebas
Touchpad / Mouse Drag : Mengubah arah pandang kamera (Yaw & Pitch).
* W / S : Bergerak maju / mundur searah pandangan kamera.
* Q / E : Bergerak ke atas / bawah secara vertikal (Sumbu Y).
* A / D : Bergerak menyamping ke kanan / kiri (Strafing).

### Kontrol Lingkungan & Simulasi
* Spasi : Menambahkan (spawn) kendaraan baru ke jalan raya.
* (+ / -) : Mempercepat atau memperlambat siklus waktu siang/malam.
* ESC   : Keluar dari aplikasi.
