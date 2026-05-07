from model import ColorCube
from pyglm import glm
import math
import random

class Vehicle:
    def __init__(self, app, color):
        self.app = app
        self.pos = glm.vec3(0, -10, 0) # Hidden
        self.color = color
        self.direction = 1 # 1: X+, -1: X-
        self.current_speed = 0.0
        self.wheel_rot = 0.0
        self.active = False
        
        # Pilih tipe kendaraan (0: Sedan, 1: Truk, 2: Hatchback, 3: Pick-up, 4: Pedesaan)
        self.v_type = random.choice([0, 1, 2, 3, 4])
        
        self.parts = []
        self.wheels = []
        
        # WARNA KACA: Putih kebiruan sangat terang agar terlihat bening/reflektif
        glass_color = (0.9, 0.95, 1.0) 

        if self.v_type == 0: # SEDAN
            self.length, self.orig_speed, self.safe_distance = 2.0, random.uniform(7, 9), 4.0
            self.body = ColorCube(app, color=color, scale=(1.0, 0.25, 0.5))
            self.body.relative_offset = glm.vec3(0, 0, 0)   # <-- TAMBAHKAN INI
            self.cabin = ColorCube(app, color=glass_color, scale=(0.5, 0.25, 0.45))
            self.cabin.relative_offset = glm.vec3(0.0, 0.5, 0)
            self.parts.extend([self.body, self.cabin])
            w_offs = [glm.vec3(0.6, -0.2, 0.45), glm.vec3(0.6, -0.2, -0.45), glm.vec3(-0.6, -0.2, 0.45), glm.vec3(-0.6, -0.2, -0.45)]

        elif self.v_type == 1: # TRUK BESAR
            self.length, self.orig_speed, self.safe_distance = 3.5, random.uniform(4, 6), 5.5
            self.cabin = ColorCube(app, color=color, scale=(0.6, 0.6, 0.5))
            self.cabin.relative_offset = glm.vec3(1.0, 0.4, 0)
            # TAMBAHAN: Kaca Depan Truk
            self.window = ColorCube(app, color=glass_color, scale=(0.1, 0.3, 0.45))
            self.window.relative_offset = glm.vec3(1.55, 0.6, 0)
            
            self.body = ColorCube(app, color=(0.3, 0.3, 0.3), scale=(1.2, 0.6, 0.55))
            self.body.relative_offset = glm.vec3(-0.6, 0.4, 0)
            self.parts.extend([self.cabin, self.window, self.body])
            w_offs = [glm.vec3(1.1, -0.2, 0.45), glm.vec3(1.1, -0.2, -0.45), glm.vec3(-0.4, -0.2, 0.45), glm.vec3(-0.4, -0.2, -0.45), glm.vec3(-1.2, -0.2, 0.45), glm.vec3(-1.2, -0.2, -0.45)]

        elif self.v_type == 2: # HATCHBACK
            self.length, self.orig_speed, self.safe_distance = 1.7, random.uniform(8, 10), 3.5
            self.body = ColorCube(app, color=color, scale=(0.85, 0.25, 0.5))
            self.body.relative_offset = glm.vec3(0, 0, 0)   # <-- TAMBAHKAN INI
            self.cabin = ColorCube(app, color=glass_color, scale=(0.4, 0.25, 0.45))
            self.cabin.relative_offset = glm.vec3(-0.1, 0.5, 0)
            self.parts.extend([self.body, self.cabin])
            w_offs = [glm.vec3(0.5, -0.2, 0.45), glm.vec3(0.5, -0.2, -0.45), glm.vec3(-0.5, -0.2, 0.45), glm.vec3(-0.5, -0.2, -0.45)]

        elif self.v_type == 3: # PICK-UP
            self.length, self.orig_speed, self.safe_distance = 2.2, random.uniform(6, 8), 4.5
            self.head = ColorCube(app, color=color, scale=(0.4, 0.45, 0.45))
            self.head.relative_offset = glm.vec3(0.6, 0.3, 0)
            # TAMBAHAN: Kaca Depan Pick-up
            self.window = ColorCube(app, color=glass_color, scale=(0.1, 0.25, 0.4))
            self.window.relative_offset = glm.vec3(0.95, 0.45, 0)
            
            self.bak_floor = ColorCube(app, color=(0.2, 0.2, 0.2), scale=(0.7, 0.1, 0.45))
            self.bak_floor.relative_offset = glm.vec3(-0.4, 0.05, 0)
            self.wall_l = ColorCube(app, color=color, scale=(0.7, 0.15, 0.05))
            self.wall_l.relative_offset = glm.vec3(-0.4, 0.2, 0.4)
            self.wall_r = ColorCube(app, color=color, scale=(0.7, 0.15, 0.05))
            self.wall_r.relative_offset = glm.vec3(-0.4, 0.2, -0.4)
            self.parts.extend([self.head, self.window, self.bak_floor, self.wall_l, self.wall_r])
            w_offs = [glm.vec3(0.6, -0.2, 0.45), glm.vec3(0.6, -0.2, -0.45), glm.vec3(-0.6, -0.2, 0.45), glm.vec3(-0.6, -0.2, -0.45)]

        elif self.v_type == 4: # MOBIL PEDESAAN
            self.length, self.orig_speed, self.safe_distance = 2.0, random.uniform(5, 7), 4.0
            self.body = ColorCube(app, color=color, scale=(1.0, 0.4, 0.55))
            self.body.relative_offset = glm.vec3(0, 0.3, 0)
            # TAMBAHAN: Jendela samping pedesaan (kiri & kanan)
            self.win_l = ColorCube(app, color=glass_color, scale=(0.6, 0.2, 0.01))
            self.win_l.relative_offset = glm.vec3(-0.1, 1.0, 0.55)
            self.win_r = ColorCube(app, color=glass_color, scale=(0.6, 0.2, 0.01))
            self.win_r.relative_offset = glm.vec3(-0.1, 1.0, -0.55)
            # Atap
            self.roof = ColorCube(app, color=color, scale=(0.8, 0.1, 0.5))
            self.roof.relative_offset = glm.vec3(-0.1, 1.3, 0)
            
            self.parts.extend([self.body, self.win_l, self.win_r, self.roof])
            w_offs = [glm.vec3(0.6, -0.2, 0.45), glm.vec3(0.6, -0.2, -0.45), glm.vec3(-0.6, -0.2, 0.45), glm.vec3(-0.6, -0.2, -0.45)]

        # Inisialisasi Roda
        for off in w_offs:
            wheel = ColorCube(app, color=(0.15, 0.15, 0.15), scale=(0.22, 0.22, 0.22))
            wheel.relative_offset = off
            self.wheels.append(wheel)
            
        self.all_parts = self.parts + self.wheels
        self.deceleration, self.accel_rate = 10.0, 8.0

    def update(self):
        if not self.active: return
        dt = self.app.delta_time
        self.wheel_rot += abs(self.current_speed) * dt * 6.0
        
        for part in self.parts:
            off_x = part.relative_offset.x * self.direction
            part.pos = self.pos + glm.vec3(off_x, part.relative_offset.y, part.relative_offset.z)
            part.m_model = part.get_model_matrix()
            
        for wheel in self.wheels:
            off_x = wheel.relative_offset.x * self.direction
            wheel.pos = self.pos + glm.vec3(off_x, wheel.relative_offset.y, wheel.relative_offset.z)
            wheel.rot.z = -self.wheel_rot * self.direction
            wheel.m_model = wheel.get_model_matrix()

    def render(self):
        if not self.active: return
        for part in self.all_parts:
            part.render()


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        
        # --- FINITE STATE MACHINE (FSM) ---
        # 90.0 = Tegak (Buka), 0.0 = Mendatar (Tutup)
        self.state = 'IDLE' 
        self.gate_angle = 90.0 
        self.gate_speed = 60.0 # Derajat per detik
        
        # Pengaturan Kereta (Sumbu Z)
        self.TRAIN_START_Z = -50.0
        self.TRAIN_END_Z = 50.0
        self.train_z = self.TRAIN_START_Z
        self.train_speed = 25.0
        
        # --- SISTEM KENDARAAN (Sumbu X) ---
        self.vehicles_pool = []
        self.active_count = 0
        self.max_pool = 10
        self.SAFE_DISTANCE = 3.5
        self.spawn_count = 0
        
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        

        def load(self):
            app = self.app
            add = self.add_object

        # ==========================================
        # 0 & 1. LINGKUNGAN JALAN & REL KERETA
        # ==========================================
        # Tanah / Rumput Utama (Hijau segar)
        add(ColorCube(app, pos=(0, -0.25, 0), scale=(50, 0.1, 50), color=(0.25, 0.45, 0.25)))

        # Jalan Raya Aspal
        add(ColorCube(app, pos=(0, -0.1, 0), scale=(50, 0.05, 5), color=(0.15, 0.15, 0.15)))
        
        # Trotoar (Kiri dan Kanan Jalan Raya)
        add(ColorCube(app, pos=(0, 0.0, 5.5), scale=(50, 0.1, 0.5), color=(0.6, 0.6, 0.6)))
        add(ColorCube(app, pos=(0, 0.0, -5.5), scale=(50, 0.1, 0.5), color=(0.6, 0.6, 0.6)))

        # Marka Jalan Putus-Putus
        for x_pos in range(-48, 52, 4):
            add(ColorCube(app, pos=(x_pos, -0.04, 0), scale=(1.0, 0.01, 0.15), color=(0.9, 0.9, 0.9)))

        # Batu Kerikil (Gravel) di Bawah Rel Kereta
        add(ColorCube(app, pos=(0, -0.05, 0), scale=(3.5, 0.1, 50), color=(0.35, 0.35, 0.35)))

        # Rel Kereta Besi
        add(ColorCube(app, pos=(-1.5, 0.15, 0), scale=(0.1, 0.1, 50), color=(0.7, 0.7, 0.7)))
        add(ColorCube(app, pos=(1.5, 0.15, 0), scale=(0.1, 0.1, 50), color=(0.7, 0.7, 0.7)))
        
        # Bantalan Rel Kayu (Dihapus di area persimpangan aspal)
        for i in range(50):
            z_pos = (i - 25) * 1.5
            if abs(z_pos) > 5.5: # Jangan pasang bantalan kayu di tengah jalan raya
                add(ColorCube(app, pos=(0, 0.05, z_pos), scale=(2.2, 0.05, 0.3), color=(0.4, 0.25, 0.1)))

        # Pos Penjaga Palang Pintu (Lebih Detail seperti Bangunan)
        add(ColorCube(app, pos=(7, 0.1, 7), scale=(1.5, 0.1, 1.5), color=(0.5, 0.5, 0.5)))    # Lantai/Pondasi
        add(ColorCube(app, pos=(7, 0.6, 7), scale=(1.2, 0.4, 1.2), color=(0.8, 0.8, 0.7)))    # Tembok Bawah
        add(ColorCube(app, pos=(7, 1.3, 7), scale=(1.1, 0.3, 1.1), color=(0.7, 0.9, 1.0)))    # Kaca Sian Terang
        add(ColorCube(app, pos=(7, 1.7, 7), scale=(1.4, 0.15, 1.4), color=(0.6, 0.2, 0.2)))   # Atap Merah bata
        
        # Tiang Antena di atas Pos
        add(ColorCube(app, pos=(7, 2.2, 7), scale=(0.02, 0.5, 0.02), color=(0.1, 0.1, 0.1)))

        # ==========================================
        # 4. DEKORASI LINGKUNGAN (Pohon, Tiang, Awan)
        # ==========================================
        
        # A. Tiang Lampu Jalan (Berjejer di sepanjang pinggir trotoar)
        for x_pos in range(-40, 41, 15):
            if abs(x_pos) > 5: # Jauhi area perlintasan rel
                add(ColorCube(app, pos=(x_pos, 2.0, -6.5), scale=(0.1, 2.0, 0.1), color=(0.3, 0.3, 0.3))) # Tiang Vertikal
                add(ColorCube(app, pos=(x_pos, 3.9, -5.8), scale=(0.08, 0.08, 0.8), color=(0.3, 0.3, 0.3))) # Lengan Horizontal
                add(ColorCube(app, pos=(x_pos, 3.8, -5.2), scale=(0.2, 0.1, 0.2), color=(1.0, 1.0, 0.6))) # Lampu (Kuning Terang)

        # B. Hutan / Pepohonan (Variasi Pohon Biasa dan Pohon Cemara)
        tree_positions = [
            (-15, -15), (-25, -10), (-35, -20), (-12, -30), (-45, -15), (-30, -35),
            (15, -15),  (25, -10),  (35, -20),  (12, -30),  (45, -15),  (30, -35),
            (-15, 15),  (-25, 10),  (-35, 20),  (-12, 30),  (-45, 15),  (-30, 35),
            (15, 15),   (25, 10),   (35, 20),   (12, 30),   (45, 15),   (30, 35)
        ]
        
        for tx, tz in tree_positions:
            # Randomize ukuran dan tipe pohon agar hutan terlihat organik
            tree_type = random.choice(['normal', 'pine'])
            scale_y = random.uniform(0.8, 1.5)
            
            # Batang Kayu
            add(ColorCube(app, pos=(tx, 0.5 * scale_y, tz), scale=(0.3, 0.8 * scale_y, 0.3), color=(0.4, 0.2, 0.1)))
            
            if tree_type == 'normal':
                # Daun Kotak Besar bertingkat
                add(ColorCube(app, pos=(tx, 1.5 * scale_y, tz), scale=(1.2, 1.0 * scale_y, 1.2), color=(0.15, 0.55, 0.2)))
                add(ColorCube(app, pos=(tx, 2.2 * scale_y, tz), scale=(0.8, 0.6 * scale_y, 0.8), color=(0.2, 0.6, 0.25)))
            else:
                # Daun Cemara (Tumpukan balok mengecil ke atas)
                add(ColorCube(app, pos=(tx, 1.2 * scale_y, tz), scale=(1.4, 0.5 * scale_y, 1.4), color=(0.1, 0.45, 0.15)))
                add(ColorCube(app, pos=(tx, 1.8 * scale_y, tz), scale=(1.0, 0.5 * scale_y, 1.0), color=(0.1, 0.45, 0.15)))
                add(ColorCube(app, pos=(tx, 2.4 * scale_y, tz), scale=(0.6, 0.5 * scale_y, 0.6), color=(0.1, 0.45, 0.15)))

        # C. Awan (Voxel Clouds di langit)
        cloud_positions = [
            (-20, 15, -30), (20, 16, -25), (0, 14, -40),
            (-30, 17, 20), (30, 15, 25), (10, 16, 35)
        ]
        for cx, cy, cz in cloud_positions:
            add(ColorCube(app, pos=(cx, cy, cz), scale=(3.0, 0.5, 2.0), color=(1.0, 1.0, 1.0)))
            add(ColorCube(app, pos=(cx+1.5, cy+0.3, cz+0.5), scale=(2.0, 0.6, 1.5), color=(0.95, 0.95, 0.95)))
            add(ColorCube(app, pos=(cx-1.0, cy+0.2, cz-0.5), scale=(2.5, 0.4, 1.8), color=(1.0, 1.0, 1.0)))

        # ==========================================
        # [PASTIKAN KODE KERETA, PALANG PINTU, & OBJECT POOL LU TETAP ADA DI BAWAH SINI]
        # ==========================================

        # ==========================================
        # 1. BUILD KERETA API (COMPOSITE DESIGN)
        # ==========================================
        self.train_parts = []
        
        # Palet Warna
        color_body = (0.1, 0.3, 0.7)    # Biru
        color_chassis = (0.1, 0.1, 0.1) # Hitam gelap
        color_roof = (0.15, 0.15, 0.15) # Abu-abu gelap
        color_window = (0.7, 0.8, 0.9)  # Biru muda kaca
        color_accent = (0.8, 0.1, 0.1)  # Merah aksen

        # A. Sasis Bawah (Panjang dan pipih)
        chassis = ColorCube(app, color=color_chassis, scale=(1.2, 0.3, 4.5))
        chassis.relative_offset = glm.vec3(0, 2.0, 0)
        
        # B. Boiler Mesin (Kotak tebal di depan)
        boiler = ColorCube(app, color=color_body, scale=(0.9, 0.8, 2.5))
        boiler.relative_offset = glm.vec3(0, 3.1, -1.0)
        
        # C. Kabin Masinis (Tinggi di belakang)
        cabin = ColorCube(app, color=color_body, scale=(1.1, 1.5, 1.5))
        cabin.relative_offset = glm.vec3(0, 3.8, 2.5)
        
        # D. Atap Kabin (Sedikit lebih lebar dari kabin)
        roof = ColorCube(app, color=color_roof, scale=(1.25, 0.1, 1.7))
        roof.relative_offset = glm.vec3(0, 5.4, 2.5)

        # E. Cerobong Asap (Kecil di ujung depan)
        chimney = ColorCube(app, color=color_chassis, scale=(0.3, 0.6, 0.3))
        chimney.relative_offset = glm.vec3(0, 4.5, -2.5)

        # F. Kaca Jendela (Kiri & Kanan kabin)
        window_l = ColorCube(app, color=color_window, scale=(0.05, 0.5, 0.6))
        window_l.relative_offset = glm.vec3(1.1, 3.8, 2.5)
        window_r = ColorCube(app, color=color_window, scale=(0.05, 0.5, 0.6))
        window_r.relative_offset = glm.vec3(-1.1, 3.8, 2.5)

        # G. Bemper Depan (Aksen Merah)
        bumper = ColorCube(app, color=color_accent, scale=(1.1, 0.4, 0.4))
        bumper.relative_offset = glm.vec3(0, 2.1, -4.5)

        # Masukkan semua bagian body ke list
        self.train_parts.extend([chassis, boiler, cabin, roof, chimney, window_l, window_r, bumper])

        # Set posisi awal X dan Y (karena Z akan selalu bergerak)
        for part in self.train_parts:
            part.pos.x = part.relative_offset.x
            part.pos.y = part.relative_offset.y

        # ==========================================
        # 2. RODA KERETA
        # ==========================================
        self.train_wheels = []
        # Kita pakai 4 pasang roda (posisi Z relatif terhadap pusat kereta)
        wheel_z_positions = [-3.0, -1.0, 1.0, 3.0]
        
        for z_off in wheel_z_positions:
            # Roda Kanan (X+)
            wheel_r = ColorCube(app, color=(0.2, 0.2, 0.2), scale=(0.4, 0.4, 0.4))
            wheel_r.relative_offset = glm.vec3(1.3, 0, 0)
            self.train_wheels.append((wheel_r, z_off))
            
            # Roda Kiri (X-)
            wheel_l = ColorCube(app, color=(0.2, 0.2, 0.2), scale=(0.4, 0.4, 0.4))
            wheel_l.relative_offset = glm.vec3(-1.3, 0, 0)
            self.train_wheels.append((wheel_l, z_off))

        # Gabungkan ke rendering pipeline
        self.objects.extend(self.train_parts)
        self.objects.extend([w[0] for w in self.train_wheels])
    
        # 3. PALANG PINTU
        self.gates = []
        self.signal_lights = []

        # Sisi Utara (Pindah ke pinggir jalan di Z=-5.5)
        add(ColorCube(app, pos=(-7, 0.65, -5.5), scale=(0.15, 0.8, 0.15), color=(0.2, 0.2, 0.2)))
        # Crossbuck Sign (X)
        add(ColorCube(app, pos=(-7, 2.2, -5.5), scale=(0.8, 0.1, 0.15), rot=(0, 0, 45), color=(0.9, 0.9, 0.9)))
        add(ColorCube(app, pos=(-7, 2.2, -5.5), scale=(0.8, 0.1, 0.15), rot=(0, 0, -45), color=(0.9, 0.9, 0.9)))
        
        # Palang Utara diperpanjang (scale.z=4.5 -> panjang 9)
        gate_n = ColorCube(app, pos=(-7, 1.35, -5.5), scale=(0.05, 0.05, 4.5), color=(0.8, 0.1, 0.1))
        gate_n.pivot_offset = glm.vec3(0, 0, 4.5)
        self.gates.append(gate_n)
        add(gate_n)
        light_n = ColorCube(app, pos=(-7, 1.7, -5.5), scale=(0.15, 0.15, 0.15), color=(0.4, 0, 0))
        self.signal_lights.append(light_n)
        add(light_n)

        # Sisi Selatan (Pindah ke pinggir jalan di Z=5.5)
        add(ColorCube(app, pos=(7, 0.65, 5.5), scale=(0.15, 0.8, 0.15), color=(0.2, 0.2, 0.2)))
        # Crossbuck Sign (X)
        add(ColorCube(app, pos=(7, 2.2, 5.5), scale=(0.8, 0.1, 0.15), rot=(0, 0, 45), color=(0.9, 0.9, 0.9)))
        add(ColorCube(app, pos=(7, 2.2, 5.5), scale=(0.8, 0.1, 0.15), rot=(0, 0, -45), color=(0.9, 0.9, 0.9)))

        # Palang Selatan diperpanjang (scale.z=4.5 -> panjang 9)
        gate_s = ColorCube(app, pos=(7, 1.35, 5.5), scale=(0.05, 0.05, 4.5), color=(0.8, 0.1, 0.1))
        gate_s.pivot_offset = glm.vec3(0, 0, -4.5)
        self.gates.append(gate_s)
        add(gate_s)
        light_s = ColorCube(app, pos=(7, 1.7, 5.5), scale=(0.15, 0.15, 0.15), color=(0.4, 0, 0))
        self.signal_lights.append(light_s)
        add(light_s)

        

        # 5. OBJECT POOL
        for _ in range(self.max_pool):
            color = (random.random(), random.random(), random.random())
            car = Vehicle(app, color=color)
            self.vehicles_pool.append(car)
            add(car)

        # Startup: 2 Mobil
        self._spawn_vehicle(1) # Lajur X+
        self._spawn_vehicle(-1) # Lajur X-

    def _spawn_vehicle(self, direction):
        for car in self.vehicles_pool:
            if not car.active:
                car.active = True
                car.direction = direction
                car.pos.y = 0.5
                car.pos.z = 2.0 if direction == 1 else -2.0
                car.pos.x = -48.0 if direction == 1 else 48.0
                car.current_speed = 7.0 * direction
                self.active_count += 1
                break

    def handle_input_enter(self):
        if self.state == 'IDLE':
            self.state = 'CLOSING'

    def handle_input_space(self):
        if self.active_count < self.max_pool:
            self.spawn_count += 1
            direction = 1 if self.spawn_count % 2 == 0 else -1
            self._spawn_vehicle(direction)

    def update(self):
        dt = self.app.delta_time
        
        # --- ATURAN FISIKA PENGEREMAN REALISTIK ---
        GATE_X_R = -7.0 # Posisi palang utara
        GATE_X_L = 7.0  # Posisi palang selatan
        
        # --- LOGIKA KENDARAAN (Sumbu X) ---
        active_list = [v for v in self.vehicles_pool if v.active]
        
        for lane_dir in [1, -1]:
            lane_cars = [v for v in active_list if v.direction == lane_dir]
            
            # Urutan: terdepan sesuai arah laju
            if lane_dir == 1: lane_cars.sort(key=lambda v: v.pos.x, reverse=True)
            else: lane_cars.sort(key=lambda v: v.pos.x, reverse=False)

            for i, car in enumerate(lane_cars):
                # Hitung Batas Geometri
                front_bumper_x = car.pos.x + (lane_dir * (car.length / 2.0))
                
                stop_line = GATE_X_R if lane_dir == 1 else GATE_X_L
                is_before_gate = (front_bumper_x < stop_line) if lane_dir == 1 else (front_bumper_x > stop_line)
                
                # Default: Laju Normal
                target_speed = car.orig_speed * lane_dir
                current_accel = car.accel_rate
                
                # 1. LOGIKA PENGEREMAN HALUS (Lead Car)
                if is_before_gate:
                    is_queue_leader = True
                    if i > 0:
                        leader = lane_cars[i-1]
                        leader_front = leader.pos.x + (lane_dir * (leader.length / 2.0))
                        if (leader_front < stop_line) if lane_dir == 1 else (leader_front > stop_line):
                            is_queue_leader = False
                    
                    if is_queue_leader:
                        # Respon terhadap Palang (Mulai rem saat CLOSING)
                        if self.gate_angle < 85:
                            dist_to_gate = abs(stop_line - front_bumper_x)
                            
                            if dist_to_gate < 0.1: # Berhenti Sempurna (Kiss the gate)
                                target_speed = 0.0
                                car.pos.x = stop_line - (lane_dir * (car.length / 2.0))
                            elif dist_to_gate < 10.0: # Zona Pengereman
                                # Formula Creep: Semakin dekat, semakin lambat (min 0.5 agar tidak beku tengah jalan)
                                creep = max(0.5, (dist_to_gate / 10.0) * abs(car.orig_speed))
                                target_speed = creep * lane_dir
                                current_accel = car.deceleration
                    else:
                        # 2. LOGIKA PENGEREMAN HALUS (Followers)
                        leader = lane_cars[i-1]
                        leader_back = leader.pos.x - (lane_dir * (leader.length / 2.0))
                        dist_to_leader = abs(leader_back - front_bumper_x)
                        
                        if dist_to_leader < 0.5: # Terlalu dekat
                            target_speed = 0.0
                        elif dist_to_leader < car.safe_distance + 5.0:
                            # Melambat mengikuti jarak aman
                            gap = max(0.0, dist_to_leader - car.safe_distance)
                            creep = max(0.5 if gap > 0 else 0.0, (gap / 5.0) * abs(car.orig_speed))
                            target_speed = creep * lane_dir
                            current_accel = car.deceleration
                
                # 3. Sinkronisasi Kecepatan (Interpolasi Fisika)
                if car.current_speed != target_speed:
                    diff = target_speed - car.current_speed
                    step = current_accel * dt
                    if abs(diff) < step:
                        car.current_speed = target_speed
                    else:
                        car.current_speed += step if diff > 0 else -step

                car.pos.x += car.current_speed * dt
                
                # Looping Mobil
                if lane_dir == 1 and car.pos.x > 50: car.pos.x = -50
                if lane_dir == -1 and car.pos.x < -50: car.pos.x = 50

        # --- FINITE STATE MACHINE (FSM) PALANG & KERETA ---
        if self.state == 'IDLE':
            # Palang tegak lurus sempurna, menunggu trigger
            self.gate_angle = 90.0
            self.train_z = self.TRAIN_START_Z

        elif self.state == 'CLOSING':
            # Proses Menurunkan Palang
            self.gate_angle -= self.gate_speed * dt
            # Aturan Clamping Ketat: 0.0
            if self.gate_angle <= 0.0:
                self.gate_angle = 0.0
                self.state = 'TRAIN_CROSSING'

        elif self.state == 'TRAIN_CROSSING':
            # Palang terkunci kaku mendatar
            self.gate_angle = 0.0
            # Pergerakan Kereta melintasi jalan
            self.train_z += self.train_speed * dt
            # Batas jarak aman perlintasan tercapai
            if self.train_z > self.TRAIN_END_Z:
                self.state = 'OPENING'

        elif self.state == 'OPENING':
            # Proses Menaikkan Palang
            self.gate_angle += self.gate_speed * dt
            # Aturan Clamping Ketat: 90.0
            if self.gate_angle >= 90.0:
                self.gate_angle = 90.0
                self.state = 'IDLE'

        # --- UPDATE MATRIX ---
        # Update Posisi Body Kereta
        for part in self.train_parts:
            # Z selalu diupdate berdasarkan titik pusat kereta + offset masing-masing part
            part.pos.z = self.train_z + part.relative_offset.z
            part.m_model = part.get_model_matrix()

        # Update Posisi Roda Kereta (Berputar Sinkron)
        wheel_rot_angle = self.train_z * 2.0
        for wheel, z_offset in self.train_wheels:
            # Posisi Y diset ke 1.4 agar menempel ke tanah / bawah sasis
            wheel.pos = glm.vec3(0, 1.4, self.train_z + z_offset) + wheel.relative_offset
            wheel.rot.x = wheel_rot_angle
            wheel.m_model = wheel.get_model_matrix()

        # Lampu Sinyal Berdenyut
        pulse = (math.sin(self.app.time * 15) + 1) * 0.5 if self.state != 'IDLE' else 0.0
        light_color = glm.vec3(0.4 + 0.6 * pulse, 0.0, 0.0)
        for light in self.signal_lights:
            light.color = light_color

        for i, gate in enumerate(self.gates):
            # i=0 (Sisi Utara/X-): Pivot di Z=-3, bar ke +Z. Rotate -90 to 0 around X.
            # i=1 (Sisi Selatan/X+): Pivot di Z=3, bar ke -Z. Rotate 90 to 0 around X.
            angle_rad = glm.radians(self.gate_angle)
            gate.rot.x = -angle_rad if i == 0 else angle_rad
            gate.m_model = gate.get_model_matrix()

        for obj in self.objects:
            obj.update()

    def trigger_crossing(self):
        if self.state == 'IDLE':
            self.state = 'CLOSING'
