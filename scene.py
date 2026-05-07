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
        
        # WARNA KACA
        glass_color = (0.9, 0.95, 1.0) 

        # --- SETTING UKURAN KENDARAAN (PROPORSIONAL REALISTIS) ---

        if self.v_type == 0: # SEDAN (Kecil & Ceper)
            self.length, self.orig_speed, self.safe_distance = 2.5, random.uniform(8, 10), 4.5
            self.body = ColorCube(app, color=color, scale=(1.2, 0.25, 0.5))
            self.body.relative_offset = glm.vec3(0, 0, 0)
            self.cabin = ColorCube(app, color=glass_color, scale=(0.5, 0.25, 0.45))
            self.cabin.relative_offset = glm.vec3(0.0, 0.5, 0)
            self.parts.extend([self.body, self.cabin])
            w_offs = [glm.vec3(0.7, -0.2, 0.5), glm.vec3(0.7, -0.2, -0.5), glm.vec3(-0.7, -0.2, 0.5), glm.vec3(-0.7, -0.2, -0.5)]
            w_size = 0.25

        elif self.v_type == 1: # TRUK BESAR (Raksasa Jalanan)
            self.length, self.orig_speed, self.safe_distance = 6.0, random.uniform(4, 6), 8.0
            self.cabin = ColorCube(app, color=color, scale=(1.0, 1.2, 1.1))
            self.cabin.relative_offset = glm.vec3(2.0, 0.8, 0)
            self.window = ColorCube(app, color=glass_color, scale=(0.1, 0.5, 1.0))
            self.window.relative_offset = glm.vec3(3.05, 1.2, 0)
            # Bak kargo truk jauh lebih besar dan tinggi
            self.body = ColorCube(app, color=(0.3, 0.3, 0.3), scale=(3.5, 1.6, 1.2))
            self.body.relative_offset = glm.vec3(-1.5, 1.2, 0)
            self.parts.extend([self.cabin, self.window, self.body])
            # Roda truk lebih banyak dan lebih besar
            w_offs = [glm.vec3(2.0, -0.2, 1.0), glm.vec3(2.0, -0.2, -1.0), 
                    glm.vec3(-1.0, -0.2, 1.0), glm.vec3(-1.0, -0.2, -1.0), 
                    glm.vec3(-2.8, -0.2, 1.0), glm.vec3(-2.8, -0.2, -1.0)]
            w_size = 0.45 

        elif self.v_type == 2: # HATCHBACK (Paling Kecil/Kompak)
            self.length, self.orig_speed, self.safe_distance = 2.0, random.uniform(8, 10), 4.0
            self.body = ColorCube(app, color=color, scale=(0.9, 0.25, 0.5))
            self.body.relative_offset = glm.vec3(0, 0, 0)
            self.cabin = ColorCube(app, color=glass_color, scale=(0.4, 0.25, 0.45))
            self.cabin.relative_offset = glm.vec3(-0.1, 0.5, 0)
            self.parts.extend([self.body, self.cabin])
            w_offs = [glm.vec3(0.5, -0.2, 0.5), glm.vec3(0.5, -0.2, -0.5), glm.vec3(-0.5, -0.2, 0.5), glm.vec3(-0.5, -0.2, -0.5)]
            w_size = 0.22

        elif self.v_type == 3: # PICK-UP (Sedang)
            self.length, self.orig_speed, self.safe_distance = 3.0, random.uniform(6, 8), 5.0
            self.head = ColorCube(app, color=color, scale=(0.6, 0.5, 0.55))
            self.head.relative_offset = glm.vec3(0.8, 0.3, 0)
            self.window = ColorCube(app, color=glass_color, scale=(0.1, 0.3, 0.5))
            self.window.relative_offset = glm.vec3(1.35, 0.5, 0)
            self.bak_floor = ColorCube(app, color=(0.2, 0.2, 0.2), scale=(1.2, 0.1, 0.55))
            self.bak_floor.relative_offset = glm.vec3(-0.6, 0.05, 0)
            self.wall_l = ColorCube(app, color=color, scale=(1.2, 0.2, 0.05))
            self.wall_l.relative_offset = glm.vec3(-0.6, 0.3, 0.5)
            self.wall_r = ColorCube(app, color=color, scale=(1.2, 0.2, 0.05))
            self.wall_r.relative_offset = glm.vec3(-0.6, 0.3, -0.5)
            self.parts.extend([self.head, self.window, self.bak_floor, self.wall_l, self.wall_r])
            w_offs = [glm.vec3(0.8, -0.2, 0.55), glm.vec3(0.8, -0.2, -0.55), glm.vec3(-0.8, -0.2, 0.55), glm.vec3(-0.8, -0.2, -0.55)]
            w_size = 0.28

        elif self.v_type == 4: # MOBIL PEDESAAN (Besar, tapi masih di bawah Truk)
            self.length, self.orig_speed, self.safe_distance = 3.8, random.uniform(5, 7), 6.0
            self.body = ColorCube(app, color=color, scale=(1.4, 0.6, 0.65))
            self.body.relative_offset = glm.vec3(0, 0.5, 0)
            self.win_l = ColorCube(app, color=glass_color, scale=(0.8, 0.3, 0.01))
            self.win_l.relative_offset = glm.vec3(-0.1, 1.2, 0.65)
            self.win_r = ColorCube(app, color=glass_color, scale=(0.8, 0.3, 0.01))
            self.win_r.relative_offset = glm.vec3(-0.1, 1.2, -0.65)
            self.roof = ColorCube(app, color=color, scale=(1.0, 0.1, 0.6))
            self.roof.relative_offset = glm.vec3(-0.1, 1.6, 0)
            self.parts.extend([self.body, self.win_l, self.win_r, self.roof])
            w_offs = [glm.vec3(0.9, -0.25, 0.65), glm.vec3(0.9, -0.25, -0.65), glm.vec3(-0.9, -0.25, 0.65), glm.vec3(-0.9, -0.25, -0.65)]
            w_size = 0.32

        # --- PEMBUATAN RODA SEGI-8 (OKTAGON) ---
        for off in w_offs:
            # Kubus 1 (Lurus)
            w1 = ColorCube(app, color=(0.15, 0.15, 0.15), scale=(w_size, w_size, 0.15))
            w1.relative_offset = off
            w1.base_rot = 0.0
            
            # Kubus 2 (Miring 45 derajat)
            w2 = ColorCube(app, color=(0.15, 0.15, 0.15), scale=(w_size, w_size, 0.15))
            w2.relative_offset = off
            w2.base_rot = 0.785398
            
            self.wheels.extend([w1, w2])
            
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
            # Gabungkan rotasi dasar segi-8 dengan putaran roda jalan
            wheel.rot.z = (-self.wheel_rot * self.direction) + wheel.base_rot
            wheel.m_model = wheel.get_model_matrix()

    def render(self):
        if not self.active: return
        for part in self.all_parts:
            part.render()

class SmokeParticle:
    def __init__(self, app):
        self.app = app
        # Pakai warna abu-abu / putih awan
        self.cube = ColorCube(app, color=(0.8, 0.8, 0.85), scale=(0.2, 0.2, 0.2))
        self.cube.pos = glm.vec3(0, -100, 0) # Sembunyikan di bawah tanah
        self.active = False
        self.life = 0.0
        self.max_life = 1.0
        self.vel = glm.vec3(0)
        self.base_scale = 0.15

    def spawn(self, pos):
        self.active = True
        self.life = self.max_life
        self.cube.pos = glm.vec3(pos)
        # Asap menyebar ke X sedikit, naik ke Y cepat, dan tertinggal di Z karena angin
        self.vel = glm.vec3(random.uniform(-0.5, 0.5), random.uniform(1.5, 3.0), random.uniform(1.0, 2.5))
        self.cube.scale = glm.vec3(self.base_scale)

    def update(self, dt):
        if not self.active: return
        self.life -= dt
        if self.life <= 0:
            self.active = False
            self.cube.pos = glm.vec3(0, -100, 0) # Sembunyikan lagi
            return
        
        # Gerakkan asap
        self.cube.pos += self.vel * dt
        # Efek membesar lalu mengecil saat akan hilang
        progress = self.life / self.max_life
        s = self.base_scale * (progress * 3.0) 
        self.cube.scale = glm.vec3(s, s, s)
        self.cube.m_model = self.cube.get_model_matrix()

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        
        self.state = 'IDLE' 
        self.gate_angle = 90.0 
        self.gate_speed = 60.0 
        
        
        # Pengaturan Kereta 
        self.TRAIN_START_Z = 100.0
        self.TRAIN_END_Z = -150.0
        self.train_z = self.TRAIN_START_Z
        self.train_speed = 7.0
        
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

        # 1. LINGKUNGAN JALAN, TANAH LUAS & REL PANJANG
        # Tanah Hijau (Lebar 100, Panjang 400)
        add(ColorCube(app, pos=(0, -0.25, 0), scale=(100, 0.1, 400), color=(0.25, 0.45, 0.25)))
        
        # Jalan Raya (Lebar untuk mobil besar)
        add(ColorCube(app, pos=(0, -0.1, 0), scale=(100, 0.05, 8.0), color=(0.15, 0.15, 0.15))) 
        add(ColorCube(app, pos=(0, 0.0, 9.0), scale=(100, 0.1, 1.0), color=(0.6, 0.6, 0.6)))    # Trotoar
        add(ColorCube(app, pos=(0, 0.0, -9.0), scale=(100, 0.1, 1.0), color=(0.6, 0.6, 0.6)))

        # Marka Jalan Putus-putus
        for x_pos in range(-48, 52, 4):
            add(ColorCube(app, pos=(x_pos, -0.04, 0), scale=(1.5, 0.01, 0.3), color=(0.9, 0.9, 0.9))) 

        # --- REL TUNGGAL PANJANG MEMBELAH JALAN (Z = 400) ---
        add(ColorCube(app, pos=(0, -0.05, 0), scale=(3.5, 0.1, 400), color=(0.35, 0.35, 0.35))) # Kerikil
        add(ColorCube(app, pos=(-1.5, 0.15, 0), scale=(0.1, 0.1, 400), color=(0.7, 0.7, 0.7))) # Rel Kiri
        add(ColorCube(app, pos=(1.5, 0.15, 0), scale=(0.1, 0.1, 400), color=(0.7, 0.7, 0.7))) # Rel Kanan
        
        # Bantalan Rel Kayu
        for i in range(-130, 130):
            z_pos = i * 1.5
            if abs(z_pos) > 9.0: # Dikosongkan pas di jalan aspal
                add(ColorCube(app, pos=(0, 0.05, z_pos), scale=(2.2, 0.05, 0.3), color=(0.4, 0.25, 0.1)))

        # Pos Penjaga (Diperbesar Proporsional & Digeser)
        add(ColorCube(app, pos=(12, 0.2, 12), scale=(2.2, 0.2, 2.2), color=(0.5, 0.5, 0.5)))    
        add(ColorCube(app, pos=(12, 1.2, 12), scale=(1.8, 0.8, 1.8), color=(0.8, 0.8, 0.7)))    
        add(ColorCube(app, pos=(12, 2.6, 12), scale=(1.6, 0.6, 1.6), color=(0.7, 0.9, 1.0)))    
        add(ColorCube(app, pos=(12, 3.4, 12), scale=(2.0, 0.3, 2.0), color=(0.6, 0.2, 0.2)))   
        add(ColorCube(app, pos=(12, 4.4, 12), scale=(0.04, 1.0, 0.04), color=(0.1, 0.1, 0.1)))

        # 2. DEKORASI LINGKUNGAN (UKURAN POHON DISEIMBANGKAN)
        for x_pos in range(-40, 41, 15):
            if abs(x_pos) > 5: 
                add(ColorCube(app, pos=(x_pos, 2.0, -10.5), scale=(0.1, 2.0, 0.1), color=(0.3, 0.3, 0.3)))
                add(ColorCube(app, pos=(x_pos, 3.9, -9.8), scale=(0.08, 0.08, 0.8), color=(0.3, 0.3, 0.3)))
                add(ColorCube(app, pos=(x_pos, 3.8, -9.2), scale=(0.2, 0.1, 0.2), color=(1.0, 1.0, 0.6)))

        tree_positions = [
            (-15, -18), (-25, -12), (-35, -22), (-12, -32), (-45, -18), (-30, -38),
            (15, -18),  (25, -12),  (35, -22),  (12, -32),  (45, -18),  (30, -38),
            (-15, 18),  (-25, 12),  (-35, 22),  (-12, 32),  (-45, 18),  (-30, 38),
            (15, 18),   (25, 12),   (35, 22),   (12, 32),   (45, 18),   (30, 38)
        ]
        
        for tx, tz in tree_positions:
            tree_type = random.choice(['normal', 'pine'])
            scale_y = random.uniform(1.1, 1.8) # Ukuran diturunkan biar seimbang
            
            # Batang Pohon
            add(ColorCube(app, pos=(tx, 0.8 * scale_y, tz), scale=(0.4, 1.2 * scale_y, 0.4), color=(0.4, 0.2, 0.1)))
            if tree_type == 'normal':
                add(ColorCube(app, pos=(tx, 2.2 * scale_y, tz), scale=(1.6, 1.4 * scale_y, 1.6), color=(0.15, 0.55, 0.2)))
                add(ColorCube(app, pos=(tx, 3.4 * scale_y, tz), scale=(1.2, 0.8 * scale_y, 1.2), color=(0.2, 0.6, 0.25)))
            else:
                add(ColorCube(app, pos=(tx, 1.8 * scale_y, tz), scale=(1.8, 0.8 * scale_y, 1.8), color=(0.1, 0.45, 0.15)))
                add(ColorCube(app, pos=(tx, 2.8 * scale_y, tz), scale=(1.2, 0.8 * scale_y, 1.2), color=(0.1, 0.45, 0.15)))
                add(ColorCube(app, pos=(tx, 3.8 * scale_y, tz), scale=(0.6, 0.8 * scale_y, 0.6), color=(0.1, 0.45, 0.15)))

        cloud_positions = [
            (-20, 15, -30), (20, 16, -25), (0, 14, -40),
            (-30, 17, 20), (30, 15, 25), (10, 16, 35)
        ]
        for cx, cy, cz in cloud_positions:
            add(ColorCube(app, pos=(cx, cy, cz), scale=(3.0, 0.5, 2.0), color=(1.0, 1.0, 1.0)))
            add(ColorCube(app, pos=(cx+1.5, cy+0.3, cz+0.5), scale=(2.0, 0.6, 1.5), color=(0.95, 0.95, 0.95)))
            add(ColorCube(app, pos=(cx-1.0, cy+0.2, cz-0.5), scale=(2.5, 0.4, 1.8), color=(1.0, 1.0, 1.0)))
        
        # ==========================================
        # STASIUN PEMBERHENTIAN & TUGU RAKSASA
        # ==========================================
        st_z = -110
        
        # 1. PERON (LANTAI STASIUN) DIBELAH DUA SANGAT LEBAR
        # Digeser jauh ke X = -6 dan X = 6. 
        # Tengahnya (X = -4 sampai 4) KOSONG TOTAL untuk jalur rel dan Thomas!
        add(ColorCube(app, pos=(-7.0, 0.2, st_z), scale=(4.0, 0.4, 60.0), color=(0.45, 0.45, 0.45))) # Peron Kiri
        add(ColorCube(app, pos=(7.0, 0.2, st_z), scale=(4.0, 0.4, 60.0), color=(0.45, 0.45, 0.45)))  # Peron Kanan
        
        # 2. ATAP & TIANG (Sangat tinggi ke atas, Y = 9.0)
        add(ColorCube(app, pos=(0.0, 9.0, st_z), scale=(20.0, 0.2, 60.0), color=(0.15, 0.25, 0.15))) 
        
        for i in range(6):
            z_light = st_z - 25 + (i * 10)
            # Tiang digeser lebih jauh ke samping biar lega
            add(ColorCube(app, pos=(-7.5, 4.6, z_light), scale=(0.4, 9.0, 0.4), color=(0.25, 0.25, 0.25)))
            add(ColorCube(app, pos=(7.5, 4.6, z_light), scale=(0.4, 9.0, 0.4), color=(0.25, 0.25, 0.25)))
            
            # 3. PENCAHAYAAN (Lampu Plafon Kuning Terang)
            add(ColorCube(app, pos=(0.0, 8.8, z_light), scale=(4.0, 0.2, 4.0), color=(1.0, 1.0, 0.9)))
            add(ColorCube(app, pos=(-5.0, 8.8, z_light), scale=(2.5, 0.2, 2.5), color=(1.0, 1.0, 0.8)))
            add(ColorCube(app, pos=(5.0, 8.8, z_light), scale=(2.5, 0.2, 2.5), color=(1.0, 1.0, 0.8)))

        # 4. TUGU KERETA TUA (Aman di Peron Kanan)
        tx, ty, tz = 7.0, 0.4, st_z - 5
        add(ColorCube(app, pos=(tx, ty+0.3, tz), scale=(4.0, 0.6, 8.0), color=(0.3, 0.3, 0.3))) # Dudukan
        add(ColorCube(app, pos=(tx, ty+2.0, tz), scale=(2.5, 2.5, 6.0), color=(0.1, 0.1, 0.1))) # Boiler
        add(ColorCube(app, pos=(tx, ty+3.2, tz+2.0), scale=(2.8, 3.5, 2.5), color=(0.15, 0.1, 0.1))) # Kabin
        add(ColorCube(app, pos=(tx, ty+4.5, tz-1.5), scale=(0.6, 2.5, 0.6), color=(0.05, 0.05, 0.05))) # Cerobong
        for rz in [-2.0, 0.0, 2.0]:
            add(ColorCube(app, pos=(tx-1.4, ty+1.2, tz+rz), scale=(0.2, 2.0, 2.0), color=(0.25, 0.1, 0.1)))
            add(ColorCube(app, pos=(tx+1.4, ty+1.2, tz+rz), scale=(0.2, 2.0, 2.0), color=(0.25, 0.1, 0.1)))
        
        # 3. KERETA API (THOMAS THE TANK ENGINE & CARRIAGES)
        self.train_parts = []
        self.train_wheels = []
        
        # Palet Warna Thomas
        color_thomas_blue = (0.1, 0.4, 0.8)   # Biru cerah Thomas
        color_thomas_red = (0.8, 0.1, 0.1)    # Merah sasis/bemper
        color_face = (0.75, 0.75, 0.75)       # Wajah abu-abu pucat
        color_black = (0.1, 0.1, 0.1)         # Hitam cerobong/atap
        color_coach = (0.8, 0.5, 0.2)         # Oranye kecoklatan (Annie/Clarabel)
        color_glass = (0.7, 0.9, 1.0)         # Kaca

        y_base = 0.8    # Sasis
        y_wheel = 0.4   # Roda (lebih rendah)

        # --- LOKOMOTIF (THOMAS) ---
        # 1. Sasis Bawah & Bemper (Merah)
        loco_base = ColorCube(app, pos=(0, y_base, self.train_z), scale=(1.6, 0.2, 3.0), color=color_thomas_red)
        loco_base.relative_offset = glm.vec3(0, 0, 0)
        
        # 2. Boiler / Tabung Mesin Tengah (Biru)
        loco_boiler = ColorCube(app, pos=(0, 1.4, self.train_z - 0.4), scale=(1.0, 1.0, 2.0), color=color_thomas_blue)
        loco_boiler.relative_offset = glm.vec3(0, 0.6, -0.4)
        
        # 3. Kotak Air Samping / Side Tanks (Biru)
        loco_tank = ColorCube(app, pos=(0, 1.2, self.train_z - 0.1), scale=(1.45, 0.6, 1.6), color=color_thomas_blue)
        loco_tank.relative_offset = glm.vec3(0, 0.4, -0.1)
        
        # 4. Kabin Masinis di Belakang (Biru)
        loco_cabin = ColorCube(app, pos=(0, 1.7, self.train_z + 1.0), scale=(1.45, 1.6, 1.0), color=color_thomas_blue)
        loco_cabin.relative_offset = glm.vec3(0, 0.9, 1.0)
        
        # 5. Atap Kabin (Hitam)
        loco_roof = ColorCube(app, pos=(0, 2.55, self.train_z + 1.0), scale=(1.55, 0.1, 1.2), color=color_black)
        loco_roof.relative_offset = glm.vec3(0, 1.75, 1.0)
        
        # 6. Wajah Thomas (Plat Abu-abu di depan)
        loco_face = ColorCube(app, pos=(0, 1.4, self.train_z - 1.45), scale=(0.8, 0.8, 0.1), color=color_face)
        loco_face.relative_offset = glm.vec3(0, 0.6, -1.45)
        
        # 7. Cerobong Asap (Hitam di moncong depan)
        loco_chimney = ColorCube(app, pos=(0, 2.2, self.train_z - 1.1), scale=(0.2, 0.8, 0.2), color=color_black)
        loco_chimney.relative_offset = glm.vec3(0, 1.4, -1.1)
        
        # 8. Kubah Kecil / Dome di atas boiler (Hitam)
        loco_dome = ColorCube(app, pos=(0, 2.0, self.train_z - 0.4), scale=(0.3, 0.2, 0.3), color=color_black)
        loco_dome.relative_offset = glm.vec3(0, 1.2, -0.4)
        
        # 9. Jendela Depan Kabin (Kaca)
        loco_win = ColorCube(app, pos=(0, 1.8, self.train_z + 0.45), scale=(1.1, 0.4, 0.1), color=color_glass)
        loco_win.relative_offset = glm.vec3(0, 1.0, 0.45)

        self.train_parts.extend([loco_base, loco_boiler, loco_tank, loco_cabin, loco_roof, loco_face, loco_chimney, loco_dome, loco_win])
        for p in self.train_parts[-9:]: add(p)

        # --- 2 GERBONG (ANNIE & CLARABEL) ---
        for g in range(1, 5): 
            z_off = g * 6.5
            
            g_base = ColorCube(app, pos=(0, 0.8, self.train_z + z_off), scale=(1.6, 0.2, 2.8), color=color_black)
            g_base.relative_offset = glm.vec3(0, 0, z_off)
            
            g_body = ColorCube(app, pos=(0, 1.7, self.train_z + z_off), scale=(1.5, 1.6, 2.8), color=color_coach)
            g_body.relative_offset = glm.vec3(0, 0.9, z_off)
            
            g_roof = ColorCube(app, pos=(0, 2.55, self.train_z + z_off), scale=(1.6, 0.1, 2.9), color=(0.4, 0.4, 0.4))
            g_roof.relative_offset = glm.vec3(0, 1.75, z_off)
            
            # Deretan Jendela Gerbong
            for side in [-1, 1]:
                x_win = 1.51 * side
                for z_w in [-1.0, -0.33, 0.33, 1.0]: 
                    total_win_z = z_off + z_w
                    win = ColorCube(app, pos=(x_win, 1.9, self.train_z + total_win_z), scale=(0.01, 0.5, 0.4), color=color_glass)
                    win.relative_offset = glm.vec3(x_win, 1.1, total_win_z)
                    self.train_parts.append(win); add(win)

            # Sambungan
            g_link = ColorCube(app, pos=(0, 0.8, self.train_z + z_off - 3.25), scale=(0.15, 0.05, 0.8), color=color_black)
            g_link.relative_offset = glm.vec3(0, 0, z_off - 3.25)
            
            self.train_parts.extend([g_base, g_body, g_roof, g_link])
            for p in [g_base, g_body, g_roof, g_link]: add(p)

        # --- RODA KERETA SEGI-8 ---
        all_units_z = [0] + [i * 6.5 for i in range(1, 5)]
        for i, base_z in enumerate(all_units_z):
            w_color = color_black 
            for side in [-1, 1]:
                for f_b in [-1.2, 0, 1.2]: 
                    total_z = base_z + f_b
                    
                    # Kubus Lurus
                    w1 = ColorCube(app, pos=(side * 1.5, y_wheel, self.train_z + total_z), scale=(0.1, 0.25, 0.25), color=w_color)
                    w1.relative_offset = glm.vec3(side * 1.5, 0, total_z)
                    self.train_wheels.append((w1, total_z, 0.0))
                    add(w1)
                    
                    # Kubus Miring 45 derajat
                    w2 = ColorCube(app, pos=(side * 1.5, y_wheel, self.train_z + total_z), scale=(0.1, 0.25, 0.25), color=w_color)
                    w2.relative_offset = glm.vec3(side * 1.5, 0, total_z)
                    self.train_wheels.append((w2, total_z, 0.785398))
                    add(w2)
                    
        # 4. PALANG PINTU (Disesuaikan jalan lebar)
        self.gates = []
        self.signal_lights = []

        # Utara
        add(ColorCube(app, pos=(-8, 0.8, -10), scale=(0.25, 1.5, 0.25), color=(0.2, 0.2, 0.2)))
        add(ColorCube(app, pos=(-8, 2.8, -10), scale=(1.2, 0.15, 0.2), rot=(0, 0, 45), color=(0.9, 0.9, 0.9)))
        add(ColorCube(app, pos=(-8, 2.8, -10), scale=(1.2, 0.15, 0.2), rot=(0, 0, -45), color=(0.9, 0.9, 0.9)))
        gate_n = ColorCube(app, pos=(-8, 1.5, -10), scale=(0.1, 0.1, 9.0), color=(0.8, 0.1, 0.1))
        gate_n.pivot_offset = glm.vec3(0, 0, 9.0)
        self.gates.append(gate_n)
        add(gate_n)
        light_n = ColorCube(app, pos=(-8, 2.0, -10), scale=(0.25, 0.25, 0.25), color=(0.4, 0, 0))
        self.signal_lights.append(light_n)
        add(light_n)

        # Selatan
        add(ColorCube(app, pos=(8, 0.8, 10), scale=(0.25, 1.5, 0.25), color=(0.2, 0.2, 0.2)))
        add(ColorCube(app, pos=(8, 2.8, 10), scale=(1.2, 0.15, 0.2), rot=(0, 0, 45), color=(0.9, 0.9, 0.9)))
        add(ColorCube(app, pos=(8, 2.8, 10), scale=(1.2, 0.15, 0.2), rot=(0, 0, -45), color=(0.9, 0.9, 0.9)))
        gate_s = ColorCube(app, pos=(8, 1.5, 10), scale=(0.1, 0.1, 9.0), color=(0.8, 0.1, 0.1))
        gate_s.pivot_offset = glm.vec3(0, 0, -9.0)
        self.gates.append(gate_s)
        add(gate_s)
        light_s = ColorCube(app, pos=(8, 2.0, 10), scale=(0.25, 0.25, 0.25), color=(0.4, 0, 0))
        self.signal_lights.append(light_s)
        add(light_s)

        # 5. OBJECT POOL KENDARAAN
        for _ in range(self.max_pool):
            color = (random.random(), random.random(), random.random())
            car = Vehicle(app, color=color)
            self.vehicles_pool.append(car)
            add(car)

        self._spawn_vehicle(1) 
        self._spawn_vehicle(-1)
        
        # 6. PARTIKEL ASAP THOMAS
        self.smoke_pool = []
        for _ in range(30):
            smoke = SmokeParticle(app)
            self.smoke_pool.append(smoke)
            add(smoke.cube)

    def _spawn_vehicle(self, direction):
        spawn_x = -48.0 if direction == 1 else 48.0
        for v in self.vehicles_pool:
            if v.active and v.direction == direction:
                if abs(v.pos.x - spawn_x) < 8.0:
                    return 
                    
        for car in self.vehicles_pool:
            if not car.active:
                car.active = True
                car.direction = direction
                car.pos.y = 0.8  # Dinaikkan agar ban tidak tenggelam ke aspal
                car.pos.z = 4.0 if direction == 1 else -4.0 # Lajur digeser lebih lebar
                car.pos.x = spawn_x
                car.current_speed = car.orig_speed * direction
                self.active_count += 1
                break

    def handle_input_space(self):
        if self.active_count < self.max_pool:
            self.spawn_count += 1
            direction = 1 if self.spawn_count % 2 == 0 else -1
            self._spawn_vehicle(direction)
            
    def handle_input_enter(self):    
        if self.state == 'IDLE':
            self.state = 'CLOSING'

    def update(self):
        dt = self.app.delta_time
        GATE_X_R = -8.0 
        GATE_X_L = 8.0  
        
        # --- LOGIKA KENDARAAN ---
        active_list = [v for v in self.vehicles_pool if v.active]
        for lane_dir in [1, -1]:
            lane_cars = [v for v in active_list if v.direction == lane_dir]
            if lane_dir == 1: lane_cars.sort(key=lambda v: v.pos.x, reverse=True)
            else: lane_cars.sort(key=lambda v: v.pos.x, reverse=False)

            for i, car in enumerate(lane_cars):
                front_bumper_x = car.pos.x + (lane_dir * (car.length / 2.0))
                stop_line = GATE_X_R if lane_dir == 1 else GATE_X_L
                is_before_gate = (front_bumper_x < stop_line) if lane_dir == 1 else (front_bumper_x > stop_line)
                
                target_speed = car.orig_speed * lane_dir
                current_accel = car.accel_rate
                
                is_queue_leader = True
                if is_before_gate and i > 0:
                    leader = lane_cars[i-1]
                    leader_front = leader.pos.x + (lane_dir * (leader.length / 2.0))
                    if (leader_front < stop_line) if lane_dir == 1 else (leader_front > stop_line):
                        is_queue_leader = False
                
                if is_before_gate and is_queue_leader:
                    if self.gate_angle < 85: 
                        dist_to_gate = abs(stop_line - front_bumper_x)
                        if dist_to_gate < 0.2:
                            target_speed = 0.0
                            car.current_speed = 0.0 
                        elif dist_to_gate < 10.0:
                            creep = max(0.5, (dist_to_gate / 10.0) * abs(car.orig_speed))
                            target_speed = creep * lane_dir
                            current_accel = car.deceleration

                if i > 0:
                    leader = lane_cars[i-1]
                    leader_back = leader.pos.x - (lane_dir * (leader.length / 2.0))
                    dist_to_leader = abs(leader_back - front_bumper_x)
                    
                    if dist_to_leader < car.safe_distance:
                        target_speed = 0.0
                        car.current_speed = 0.0 
                        car.pos.x = leader_back - (lane_dir * car.safe_distance)
                    elif dist_to_leader < car.safe_distance + 6.0:
                        gap = dist_to_leader - car.safe_distance
                        creep = (gap / 6.0) * abs(car.orig_speed)
                        target_speed = creep * lane_dir
                        current_accel = car.deceleration * 1.5 

                if car.current_speed != target_speed:
                    diff = target_speed - car.current_speed
                    step = current_accel * dt
                    if abs(diff) < step:
                        car.current_speed = target_speed
                    else:
                        car.current_speed += step if diff > 0 else -step

                car.pos.x += car.current_speed * dt
                
                if lane_dir == 1 and car.pos.x > 50: car.pos.x = -50
                if lane_dir == -1 and car.pos.x < -50: car.pos.x = 50

        # --- FSM PALANG & KERETA (UPDATE JEDA LEBIH CEPAT) ---
        if self.state == 'IDLE':
            self.gate_angle = 90.0
            self.train_z = self.TRAIN_START_Z

        elif self.state == 'CLOSING':
            self.gate_angle -= self.gate_speed * dt
            if self.gate_angle <= 0.0:
                self.gate_angle = 0.0
                self.state = 'TRAIN_CROSSING'

        elif self.state == 'TRAIN_CROSSING':
            self.gate_angle = 0.0
            self.train_z -= self.train_speed * dt
            
            # TRIGGER BUKA PALANG: Begitu gerbong terakhir lewat jalan (Z = -45)
            if self.train_z < -45.0:
                self.state = 'OPENING'

        elif self.state == 'OPENING':
            self.gate_angle += self.gate_speed * dt
            self.train_z -= self.train_speed * dt # Kereta tetap meluncur
            if self.gate_angle >= 90.0:
                self.gate_angle = 90.0
                self.state = 'TRAIN_LEAVING' # Transisi agar kereta lanjut ke ujung stasiun

        elif self.state == 'TRAIN_LEAVING':
            self.train_z -= self.train_speed * dt # Lanjut meluncur ke stasiun
            if self.train_z < self.TRAIN_END_Z:
                self.state = 'IDLE' # Sampai stasiun ujung, baru hilang/reset

        # --- UPDATE MATRIX KERETA ---
        for part in self.train_parts:
            part.pos.z = self.train_z + part.relative_offset.z
            part.m_model = part.get_model_matrix()

        # Update Rotasi Roda Mundur Kereta
        wheel_rot_angle = -self.train_z * 2.0
        for wheel, total_z, base_rot in self.train_wheels:
            wheel.pos = glm.vec3(wheel.relative_offset.x, 0.4, self.train_z + total_z)
            # Putar roda ditambah offset kemiringan 45 derajatnya
            wheel.rot.x = wheel_rot_angle + base_rot
            wheel.m_model = wheel.get_model_matrix()

        # Lampu Sinyal
        pulse = (math.sin(self.app.time * 15) + 1) * 0.5 if self.state != 'IDLE' else 0.0
        light_color = glm.vec3(0.4 + 0.6 * pulse, 0.0, 0.0)
        for light in self.signal_lights:
            light.color = light_color

        for i, gate in enumerate(self.gates):
            angle_rad = glm.radians(self.gate_angle)
            gate.rot.x = -angle_rad if i == 0 else angle_rad
            gate.m_model = gate.get_model_matrix()

        for obj in self.objects:
            obj.update()
        
        # --- UPDATE ASAP KERETA ---
        # Asap akan terus ngebul selama kereta tidak IDLE (sedang jalan)
        if self.state in ['CLOSING', 'TRAIN_CROSSING', 'OPENING', 'TRAIN_LEAVING']:
            if random.random() < 0.4:
                for smoke in self.smoke_pool:
                    if not smoke.active:
                        smoke.spawn((0, 2.6, self.train_z - 1.1))
                        break
        
        for smoke in self.smoke_pool:
            smoke.update(dt)
        
        for smoke in self.smoke_pool:
            smoke.update(dt)