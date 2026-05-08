from model import ColorCube, ColorPyramid
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
        
        # ==========================================================
        # PETA KOORDINAT UTAMA - RURAL VILLAGE ENVIRONMENT
        # ==========================================================
        # Project ini memakai ukuran map 200 x 0.2 x 200 unit.
        #
        # Catatan penting:
        # - ColorCube memakai mesh dasar dari -1 sampai 1.
        # - Jadi scale=(100, 0.1, 100) menghasilkan ukuran aktual:
        #   X = 200 unit, Y = 0.2 unit, Z = 200 unit.
        #
        # Sistem koordinat:
        # - X negatif  = sisi kiri map
        # - X positif  = sisi kanan map
        # - Z positif  = area atas/belakang map
        # - Z negatif  = area bawah/depan map
        # - Y          = tinggi objek dari permukaan tanah
        #
        # Layout utama:
        # - Tanah utama       : X -100 s/d 100, Z -100 s/d 100
        # - Jalan raya        : memanjang arah X, berada di Z sekitar -8 s/d 8
        # - Rel kereta        : memanjang arah Z, berada di X sekitar -3 s/d 3
        # - Crossing utama    : pusat map, sekitar X -10 s/d 10 dan Z -10 s/d 10
        #
        # Zona rural village berdasarkan sketsa:
        # - Rumah kiri atas   : X -90 s/d -20, Z 20 s/d 90
        # - Rumah kanan atas  : X 20 s/d 95,  Z 20 s/d 90
        # - Sawah kiri bawah  : X -95 s/d -25, Z -95 s/d -25
        # - Kebun kanan bawah : X 25 s/d 65,  Z -95 s/d -25
        # - Sawah air kanan   : X 70 s/d 95,  Z -95 s/d -35
        # - Tunnel rel atas   : X -8 s/d 8,   Z 85 s/d 100
        #
        # Zona larangan untuk objek environment:
        # - Jangan taruh pohon/rumah di area rel: X -4 s/d 4
        # - Jangan taruh pohon/rumah di area jalan: Z -10 s/d 10
        # - Jangan taruh objek besar di crossing: X -12 s/d 12, Z -12 s/d 12
        #
        # Tujuan komentar ini:
        # - Memudahkan pembagian kerja GitHub antar branch.
        # - Menghindari objek lingkungan menabrak kereta, jalan, kendaraan, dan palang.
        # - Menjaga semua objek tetap sesuai sketsa 200 x 200 unit.
        # ==========================================================
        
        # ==========================================================
        # KONSTANTA ZONA MAP
        # ==========================================================
        # Konstanta ini dipakai sebagai panduan posisi objek environment.
        # Belum semua langsung dipakai di tahap ini, tetapi akan dipakai
        # pada tahap rumah, sawah, pagar, pohon, dan tunnel.

        MAP_HALF_SIZE = 100.0

        ROAD_CENTER_Z = 0.0
        ROAD_HALF_WIDTH = 8.0
        ROAD_SAFE_MARGIN = 10.0

        RAIL_CENTER_X = 0.0
        RAIL_HALF_WIDTH = 3.5
        RAIL_SAFE_MARGIN = 4.0

        CROSSING_SAFE_X = 12.0
        CROSSING_SAFE_Z = 12.0

        LEFT_HOUSE_ZONE = {
            "x_min": -90.0,
            "x_max": -20.0,
            "z_min": 20.0,
            "z_max": 90.0,
        }

        RIGHT_HOUSE_ZONE = {
            "x_min": 20.0,
            "x_max": 95.0,
            "z_min": 20.0,
            "z_max": 90.0,
        }

        LEFT_FARM_ZONE = {
            "x_min": -95.0,
            "x_max": -25.0,
            "z_min": -95.0,
            "z_max": -25.0,
        }

        RIGHT_FARM_ZONE = {
            "x_min": 25.0,
            "x_max": 65.0,
            "z_min": -95.0,
            "z_max": -25.0,
        }

        RIGHT_RICE_PADDY_ZONE = {
            "x_min": 70.0,
            "x_max": 95.0,
            "z_min": -95.0,
            "z_max": -35.0,
        }

        TUNNEL_ZONE = {
            "x_min": -8.0,
            "x_max": 8.0,
            "z_min": 85.0,
            "z_max": 100.0,
        }
        
        def is_inside_crossing_safe_area(x, z):
            # Mengecek apakah posisi objek masuk area crossing utama.
            # Jika True, objek besar seperti rumah/pohon sebaiknya tidak ditaruh di sini.
            return abs(x) <= CROSSING_SAFE_X and abs(z) <= CROSSING_SAFE_Z

        def is_inside_road_safe_area(z):
            # Mengecek apakah posisi objek terlalu dekat dengan jalan raya.
            # Jalan berada di sekitar Z = 0, jadi environment besar perlu menjauh.
            return abs(z - ROAD_CENTER_Z) <= ROAD_SAFE_MARGIN

        def is_inside_rail_safe_area(x):
            # Mengecek apakah posisi objek terlalu dekat dengan rel kereta.
            # Rel berada di sekitar X = 0, jadi pohon/rumah jangan masuk area ini.
            return abs(x - RAIL_CENTER_X) <= RAIL_SAFE_MARGIN

        def is_safe_environment_position(x, z):
            # Fungsi bantu untuk memastikan posisi objek environment aman.
            # Dipakai nanti saat menaruh pohon, rumah, pagar, dan sawah.
            if is_inside_crossing_safe_area(x, z):
                return False
            if is_inside_road_safe_area(z):
                return False
            if is_inside_rail_safe_area(x):
                return False
            if x < -MAP_HALF_SIZE or x > MAP_HALF_SIZE:
                return False
            if z < -MAP_HALF_SIZE or z > MAP_HALF_SIZE:
                return False
            return True

        # ==========================================================
        # HELPER FUNCTION - RURAL VILLAGE ENVIRONMENT
        # ==========================================================
        # Semua fungsi bantu environment ditaruh di sini agar kode utama
        # di bagian bawah lebih pendek, rapi, dan mudah dibaca anggota tim.
        #
        # Catatan:
        # - Semua ukuran memakai satuan unit OpenGL project ini.
        # - pos=(x, y, z), scale=(sx, sy, sz).
        # - ColorCube memakai ukuran dasar -1 sampai 1, jadi scale akan
        #   menghasilkan ukuran aktual 2x dari nilai scale.
        # ==========================================================

        def add_box(
            name,
            x,
            y,
            z,
            sx,
            sy,
            sz,
            color,
            rot=(0, 0, 0),
            check_safe=False,
        ):
            # Helper dasar untuk membuat objek kubus berwarna.
            # Parameter name hanya untuk dokumentasi/comment saat membaca kode.
            # check_safe=True dipakai untuk objek besar seperti rumah/pohon,
            # supaya tidak masuk area rel, jalan raya, atau crossing.
            if check_safe and not is_safe_environment_position(x, z):
                return None

            obj = ColorCube(
                app,
                pos=(x, y, z),
                rot=rot,
                scale=(sx, sy, sz),
                color=color,
            )
            add(obj)
            return obj

        def add_pine_tree(x, z, height=1.0, check_safe=True):
            # Pohon cemara low-poly.
            # Dibuat dari batang kubus dan 3 tumpuk daun piramida.
            # Cocok untuk area desa dan pinggir rel, tetapi tidak boleh
            # masuk jalur rel/jalan/crossing.
            if check_safe and not is_safe_environment_position(x, z):
                return

            trunk_color = (0.32, 0.18, 0.08)
            leaf_dark = (0.07, 0.32, 0.10)
            leaf_mid = (0.10, 0.45, 0.13)
            leaf_light = (0.14, 0.58, 0.16)

            # Batang pohon
            add_box(
                "pine tree trunk",
                x,
                0.55 * height,
                z,
                0.18 * height,
                0.55 * height,
                0.18 * height,
                trunk_color,
            )

            # Daun bawah
            add(
                ColorPyramid(
                    app,
                    pos=(x, 1.55 * height, z),
                    scale=(1.25 * height, 0.90 * height, 1.25 * height),
                    color=leaf_dark,
                )
            )

            # Daun tengah
            add(
                ColorPyramid(
                    app,
                    pos=(x, 2.25 * height, z),
                    scale=(0.95 * height, 0.80 * height, 0.95 * height),
                    color=leaf_mid,
                )
            )

            # Daun atas
            add(
                ColorPyramid(
                    app,
                    pos=(x, 2.90 * height, z),
                    scale=(0.65 * height, 0.70 * height, 0.65 * height),
                    color=leaf_light,
                )
            )

        def add_dirt_path(x, z, sx, sz, rot_y=0):
            # Jalan tanah tipis di atas permukaan rumput.
            # Posisi Y dibuat sedikit di atas tanah agar tidak z-fighting.
            add_box(
                "dirt path",
                x,
                -0.125,
                z,
                sx,
                0.015,
                sz,
                (0.47, 0.34, 0.16),
                rot=(0, rot_y, 0),
            )

        def add_fence_line(x1, z1, x2, z2, post_gap=4.0):
            # Membuat pagar lurus dari titik awal ke titik akhir.
            # Pagar terdiri dari tiang vertikal dan dua bilah horizontal.
            fence_post_color = (0.30, 0.16, 0.06)
            fence_rail_color = (0.42, 0.22, 0.08)

            dx = x2 - x1
            dz = z2 - z1
            length = math.sqrt(dx * dx + dz * dz)

            if length <= 0.01:
                return

            angle_y = math.degrees(math.atan2(dx, dz))
            count = max(2, int(length / post_gap) + 1)

            # Tiang pagar
            for i in range(count):
                t = i / (count - 1)
                px = x1 + dx * t
                pz = z1 + dz * t

                add_box(
                    "fence post",
                    px,
                    0.55,
                    pz,
                    0.12,
                    0.55,
                    0.12,
                    fence_post_color,
                )

            # Bilah pagar atas dan bawah
            mid_x = (x1 + x2) * 0.5
            mid_z = (z1 + z2) * 0.5

            add_box(
                "upper fence rail",
                mid_x,
                0.75,
                mid_z,
                0.08,
                0.08,
                length * 0.5,
                fence_rail_color,
                rot=(0, angle_y, 0),
            )
            add_box(
                "lower fence rail",
                mid_x,
                0.38,
                mid_z,
                0.07,
                0.07,
                length * 0.5,
                fence_rail_color,
                rot=(0, angle_y, 0),
            )

        def add_fence_rect(cx, zc, sx, sz):
            # Membuat pagar kotak mengelilingi area.
            # cx, zc = titik tengah area.
            # sx, sz = setengah ukuran area, bukan ukuran penuh.
            x_min = cx - sx
            x_max = cx + sx
            z_min = zc - sz
            z_max = zc + sz

            add_fence_line(x_min, z_min, x_max, z_min)
            add_fence_line(x_max, z_min, x_max, z_max)
            add_fence_line(x_max, z_max, x_min, z_max)
            add_fence_line(x_min, z_max, x_min, z_min)

        def add_house(x, z, roof_color=(0.75, 0.18, 0.08), body_color=(0.72, 0.64, 0.45), scale=1.0):
            # Rumah desa sederhana.
            # Terdiri dari pondasi, badan rumah, atap, pintu, dan jendela.
            if not is_safe_environment_position(x, z):
                return

            # Pondasi
            add_box(
                "house foundation",
                x,
                0.12 * scale,
                z,
                3.2 * scale,
                0.12 * scale,
                2.6 * scale,
                (0.42, 0.42, 0.38),
            )

            # Badan rumah
            add_box(
                "house body",
                x,
                1.05 * scale,
                z,
                2.8 * scale,
                0.95 * scale,
                2.2 * scale,
                body_color,
            )

            # Atap utama
            add_box(
                "house roof block",
                x,
                2.25 * scale,
                z,
                3.2 * scale,
                0.35 * scale,
                2.6 * scale,
                roof_color,
            )

            # Nok/puncak atap sederhana
            add_box(
                "house roof ridge",
                x,
                2.75 * scale,
                z,
                0.18 * scale,
                0.45 * scale,
                2.7 * scale,
                roof_color,
            )

            # Pintu depan menghadap jalan raya/crossing
            add_box(
                "house door",
                x,
                0.65 * scale,
                z - 2.22 * scale,
                0.38 * scale,
                0.65 * scale,
                0.04 * scale,
                (0.22, 0.11, 0.04),
            )

            # Jendela depan kiri dan kanan
            add_box(
                "house front left window",
                x - 1.0 * scale,
                1.20 * scale,
                z - 2.25 * scale,
                0.35 * scale,
                0.28 * scale,
                0.04 * scale,
                (0.08, 0.13, 0.16),
            )
            add_box(
                "house front right window",
                x + 1.0 * scale,
                1.20 * scale,
                z - 2.25 * scale,
                0.35 * scale,
                0.28 * scale,
                0.04 * scale,
                (0.08, 0.13, 0.16),
            )

        def add_small_shed(x, z, roof_color=(0.65, 0.25, 0.10), scale=1.0):
            # Gubuk kecil/pos kecil untuk detail area desa.
            if not is_safe_environment_position(x, z):
                return

            add_box(
                "small shed body",
                x,
                0.65 * scale,
                z,
                1.0 * scale,
                0.65 * scale,
                0.9 * scale,
                (0.62, 0.50, 0.32),
            )
            add_box(
                "small shed roof",
                x,
                1.42 * scale,
                z,
                1.2 * scale,
                0.22 * scale,
                1.1 * scale,
                roof_color,
            )
            add_box(
                "small shed door",
                x,
                0.45 * scale,
                z - 0.92 * scale,
                0.25 * scale,
                0.45 * scale,
                0.04 * scale,
                (0.20, 0.10, 0.04),
            )

        def add_crop_field(cx, zc, sx, sz, crop_rows=7, crop_cols=10):
            # Petak kebun/sawah kering.
            # sx dan sz adalah setengah ukuran bidang.
            soil_color = (0.36, 0.24, 0.10)
            crop_color = (0.13, 0.50, 0.12)

            # Tanah petak
            add_box(
                "crop field soil",
                cx,
                -0.09,
                zc,
                sx,
                0.025,
                sz,
                soil_color,
            )

            # Pagar keliling petak
            add_fence_rect(cx, zc, sx + 1.2, sz + 1.2)

            # Tanaman grid
            if crop_rows <= 1 or crop_cols <= 1:
                return

            for r in range(crop_rows):
                for c in range(crop_cols):
                    px = cx - sx + 2.0 + (c * ((sx * 2.0 - 4.0) / (crop_cols - 1)))
                    pz = zc - sz + 2.0 + (r * ((sz * 2.0 - 4.0) / (crop_rows - 1)))

                    add_box(
                        "crop plant stem",
                        px,
                        0.20,
                        pz,
                        0.08,
                        0.20,
                        0.08,
                        crop_color,
                    )
                    add(
                        ColorPyramid(
                            app,
                            pos=(px, 0.55, pz),
                            scale=(0.28, 0.35, 0.28),
                            color=(0.10, 0.45, 0.10),
                        )
                    )

        def add_rice_paddy(cx, zc, sx, sz, rows=6, cols=5):
            # Sawah basah/berair.
            # Dibuat dari bidang tanah, lapisan air, dan bibit padi.
            mud_color = (0.30, 0.21, 0.10)
            water_color = (0.25, 0.48, 0.55)
            rice_color = (0.25, 0.65, 0.18)

            # Lumpur sawah
            add_box(
                "rice paddy mud",
                cx,
                -0.10,
                zc,
                sx,
                0.025,
                sz,
                mud_color,
            )

            # Air sawah tipis
            add_box(
                "rice paddy water",
                cx,
                -0.055,
                zc,
                sx - 0.4,
                0.010,
                sz - 0.4,
                water_color,
            )

            # Pagar keliling sawah
            add_fence_rect(cx, zc, sx + 1.0, sz + 1.0)

            # Bibit padi
            for r in range(rows):
                for c in range(cols):
                    px = cx - sx + 1.5 + (c * ((sx * 2.0 - 3.0) / max(1, cols - 1)))
                    pz = zc - sz + 1.5 + (r * ((sz * 2.0 - 3.0) / max(1, rows - 1)))

                    add_box(
                        "rice seedling vertical leaf",
                        px,
                        0.22,
                        pz,
                        0.04,
                        0.28,
                        0.04,
                        rice_color,
                    )
                    add_box(
                        "rice seedling side leaf",
                        px + 0.08,
                        0.25,
                        pz,
                        0.12,
                        0.035,
                        0.035,
                        rice_color,
                        rot=(0, 0, 20),
                    )

        def add_sunflower_row(start_x, z, count=8, gap=2.0):
            # Deretan bunga matahari sebagai detail dekat kebun.
            stem_color = (0.12, 0.42, 0.08)
            petal_color = (0.95, 0.70, 0.05)
            center_color = (0.28, 0.14, 0.04)

            for i in range(count):
                x = start_x + i * gap

                if not is_safe_environment_position(x, z):
                    continue

                add_box(
                    "sunflower stem",
                    x,
                    0.45,
                    z,
                    0.04,
                    0.45,
                    0.04,
                    stem_color,
                )
                add_box(
                    "sunflower petal block vertical",
                    x,
                    1.05,
                    z,
                    0.20,
                    0.28,
                    0.04,
                    petal_color,
                )
                add_box(
                    "sunflower petal block horizontal",
                    x,
                    1.05,
                    z,
                    0.04,
                    0.28,
                    0.20,
                    petal_color,
                )
                add_box(
                    "sunflower center",
                    x,
                    1.05,
                    z - 0.05,
                    0.09,
                    0.09,
                    0.03,
                    center_color,
                )

        def add_tunnel(x=0.0, z=94.0):
            # Terowongan rel sederhana di ujung atas map.
            # Dibuat dari blok beton kiri, kanan, atas, dan belakang.
            # Area tengah tetap kosong untuk jalur rel.
            concrete = (0.48, 0.48, 0.48)
            dark_opening = (0.05, 0.06, 0.06)

            # Dinding kiri
            add_box(
                "tunnel left wall",
                x - 4.0,
                2.0,
                z,
                1.2,
                2.2,
                4.5,
                concrete,
            )

            # Dinding kanan
            add_box(
                "tunnel right wall",
                x + 4.0,
                2.0,
                z,
                1.2,
                2.2,
                4.5,
                concrete,
            )

            # Atap utama
            add_box(
                "tunnel top block",
                x,
                4.3,
                z,
                5.2,
                1.0,
                4.5,
                concrete,
            )

            # Back wall gelap agar terlihat seperti mulut tunnel
            add_box(
                "tunnel dark opening",
                x,
                2.0,
                z + 4.55,
                2.6,
                1.9,
                0.10,
                dark_opening,
            )

            # Bibir beton depan
            add_box(
                "tunnel front cap",
                x,
                4.9,
                z - 4.7,
                5.6,
                0.35,
                0.25,
                concrete,
            )

         # ==========================================================
        # 1. BASE MAP, JALAN RAYA, REL, DAN CROSSING
        # ==========================================================
        # Ukuran map mengikuti sketsa:
        # X = 200 unit, Y = 0.2 unit, Z = 200 unit.
        #
        # Karena ColorCube memakai bentuk dasar -1 sampai 1,
        # scale=(100, 0.1, 100) berarti ukuran aktual:
        # X = 200, Y = 0.2, Z = 200.
        #
        # Layout:
        # - Jalan raya memanjang arah X di tengah map, Z = 0.
        # - Rel kereta memanjang arah Z di tengah map, X = 0.
        # - Crossing berada di pusat map, X sekitar -10 s/d 10 dan Z sekitar -10 s/d 10.
        # ==========================================================

        # ----------------------------------------------------------
        # TANAH UTAMA 200 x 200 UNIT
        # ----------------------------------------------------------
        add_box(
            "main grass terrain 200x200",
            0,
            -0.25,
            0,
            100,
            0.1,
            100,
            (0.34, 0.56, 0.25),
        )

        # Sisi tebal bawah map agar terlihat seperti miniatur/diorama.
        add_box(
            "front terrain side wall",
            0,
            -0.62,
            -100.35,
            100,
            0.32,
            0.35,
            (0.20, 0.32, 0.12),
        )
        add_box(
            "back terrain side wall",
            0,
            -0.62,
            100.35,
            100,
            0.32,
            0.35,
            (0.20, 0.32, 0.12),
        )
        add_box(
            "left terrain side wall",
            -100.35,
            -0.62,
            0,
            0.35,
            0.32,
            100,
            (0.20, 0.32, 0.12),
        )
        add_box(
            "right terrain side wall",
            100.35,
            -0.62,
            0,
            0.35,
            0.32,
            100,
            (0.20, 0.32, 0.12),
        )

        # ----------------------------------------------------------
        # JALAN RAYA UTAMA
        # ----------------------------------------------------------
        # Jalan dibuat lebar agar mobil kecil, pickup, dan truk tetap aman.
        # Jalan memanjang dari X -100 sampai 100.
        # Lebar jalan aktual sekitar 16 unit karena scale Z = 8.
        add_box(
            "main asphalt road",
            0,
            -0.09,
            0,
            100,
            0.055,
            8.0,
            (0.14, 0.14, 0.14),
        )

        # Bahu/trotoar tipis sisi atas dan bawah jalan.
        add_box(
            "north road shoulder",
            0,
            -0.055,
            8.65,
            100,
            0.035,
            0.45,
            (0.48, 0.48, 0.46),
        )
        add_box(
            "south road shoulder",
            0,
            -0.055,
            -8.65,
            100,
            0.035,
            0.45,
            (0.48, 0.48, 0.46),
        )

        # Garis tepi jalan putih.
        add_box(
            "north road white edge line",
            0,
            -0.010,
            7.65,
            100,
            0.006,
            0.045,
            (0.92, 0.92, 0.88),
        )
        add_box(
            "south road white edge line",
            0,
            -0.010,
            -7.65,
            100,
            0.006,
            0.045,
            (0.92, 0.92, 0.88),
        )

        # Marka tengah putus-putus.
        # Area dekat rel dikosongkan agar crossing tidak terlalu penuh.
        for x_pos in range(-92, 100, 8):
            if abs(x_pos) < 8:
                continue

            add_box(
                "dashed center road marking",
                x_pos,
                -0.005,
                0,
                2.0,
                0.006,
                0.055,
                (0.92, 0.92, 0.88),
            )

        # ----------------------------------------------------------
        # REL KERETA UTAMA
        # ----------------------------------------------------------
        # Rel memanjang arah Z dari -100 sampai 100.
        # X = 0 adalah tengah jalur rel.
        # Area kerikil dibuat lebih lebar agar rel terlihat jelas dari kamera atas.
        add_box(
            "railway gravel bed",
            0,
            -0.040,
            0,
            3.2,
            0.060,
            100,
            (0.34, 0.34, 0.32),
        )

        # Garis tepi kerikil kiri dan kanan, agar jalur rel terlihat punya batas.
        add_box(
            "left gravel border",
            -3.35,
            0.000,
            0,
            0.10,
            0.035,
            100,
            (0.46, 0.46, 0.43),
        )
        add_box(
            "right gravel border",
            3.35,
            0.000,
            0,
            0.10,
            0.035,
            100,
            (0.46, 0.46, 0.43),
        )

        # Rel besi kiri dan kanan.
        # Posisi rel tidak boleh terlalu lebar agar kereta tetap terlihat pas di tengah.
        add_box(
            "left steel rail",
            -1.45,
            0.145,
            0,
            0.08,
            0.075,
            100,
            (0.72, 0.72, 0.70),
        )
        add_box(
            "right steel rail",
            1.45,
            0.145,
            0,
            0.08,
            0.075,
            100,
            (0.72, 0.72, 0.70),
        )

        # Bantalan rel kayu.
        # Bagian yang berpotongan langsung dengan jalan dikosongkan,
        # karena area crossing akan memakai pelat beton.
        for z_pos in range(-96, 98, 2):
            if abs(z_pos) <= 9:
                continue

            add_box(
                "wooden railway sleeper",
                0,
                0.050,
                z_pos,
                2.15,
                0.045,
                0.18,
                (0.36, 0.20, 0.08),
            )

        # ----------------------------------------------------------
        # PELAT BETON CROSSING
        # ----------------------------------------------------------
        # Pelat beton dibuat di area jalan yang dilintasi rel.
        # Dibagi 3 bagian agar rel besi tetap terlihat.
        add_box(
            "center concrete crossing slab",
            0,
            0.018,
            0,
            1.05,
            0.030,
            4.45,
            (0.48, 0.48, 0.45),
        )
        add_box(
            "left concrete crossing slab",
            -2.40,
            0.010,
            0,
            0.55,
            0.030,
            4.45,
            (0.48, 0.48, 0.45),
        )
        add_box(
            "right concrete crossing slab",
            2.40,
            0.010,
            0,
            0.55,
            0.030,
            4.45,
            (0.48, 0.48, 0.45),
        )

        # Garis sambungan beton crossing.
        add_box(
            "north concrete slab joint line",
            0,
            0.055,
            4.45,
            3.00,
            0.006,
            0.035,
            (0.24, 0.24, 0.22),
        )
        add_box(
            "south concrete slab joint line",
            0,
            0.055,
            -4.45,
            3.00,
            0.006,
            0.035,
            (0.24, 0.24, 0.22),
        )

        # ----------------------------------------------------------
        # GARIS STOP KENDARAAN DI DEKAT PALANG
        # ----------------------------------------------------------
        # Kendaraan dari kiri memakai lajur Z = 4.
        # Kendaraan dari kanan memakai lajur Z = -4.
        # Garis stop dibuat sebelum area palang.
        add_box(
            "west vehicle stop line before railway gate",
            -9.50,
            -0.002,
            4.0,
            0.08,
            0.006,
            2.20,
            (0.95, 0.95, 0.92),
        )
        add_box(
            "east vehicle stop line before railway gate",
            9.50,
            -0.002,
            -4.0,
            0.08,
            0.006,
            2.20,
            (0.95, 0.95, 0.92),
        )

        # Garis pendek tambahan dekat crossing agar jalan terlihat lebih resmi.
        add_box(
            "short north crossing guide line",
            -6.0,
            -0.002,
            4.0,
            1.00,
            0.006,
            0.045,
            (0.95, 0.95, 0.92),
        )
        add_box(
            "short south crossing guide line",
            6.0,
            -0.002,
            -4.0,
            1.00,
            0.006,
            0.045,
            (0.95, 0.95, 0.92),
        )

        # Pos Penjaga (Diperbesar Proporsional & Digeser)
        add(ColorCube(app, pos=(12, 0.2, 12), scale=(2.2, 0.2, 2.2), color=(0.5, 0.5, 0.5)))    
        add(ColorCube(app, pos=(12, 1.2, 12), scale=(1.8, 0.8, 1.8), color=(0.8, 0.8, 0.7)))    
        add(ColorCube(app, pos=(12, 2.6, 12), scale=(1.6, 0.6, 1.6), color=(0.7, 0.9, 1.0)))    
        add(ColorCube(app, pos=(12, 3.4, 12), scale=(2.0, 0.3, 2.0), color=(0.6, 0.2, 0.2)))   
        add(ColorCube(app, pos=(12, 4.4, 12), scale=(0.04, 1.0, 0.04), color=(0.1, 0.1, 0.1)))

        # 2. LINGKUNGAN DESA BERDASARKAN ACUAN FINAL
        # Fokus job ini: sawah, rumah, toko, kolam, pagar, pohon, dan jalan tanah.

        # POHON AREA DEPAN REL - SESUAI LINGKARAN BIRU ACUAN
        # Posisi dibuat menjauh dari rel agar tidak menabrak kereta.
        
        # ==========================================
        # JALAN TANAH AREA DESA
        # ==========================================

        add_dirt_path(-24, 22, 3.0, 22.0, -18)
        add_dirt_path(24, 22, 3.0, 22.0, 18)
        add_dirt_path(12, 22, 2.2, 12.0, 0)
        add_dirt_path(14, -60, 2.6, 36.0, 0)
        add_dirt_path(8, -92, 8.0, 2.0, 0)
        
        front_rail_trees = [
            (-12, 15, 1.15),
            (-15, 21, 1.35),
            (-10, 28, 1.05),
            (-16, 36, 1.25),
            (-8, 42, 0.95),

            (8, 14, 1.05),
            (13, 20, 1.35),
            (9, 27, 1.10),
            (15, 34, 1.25),
            (11, 42, 0.95),
        ]

        for x, z, h in front_rail_trees:
            add_pine_tree(x, z, height=h)

        # ==========================================
        # STASIUN KECIL PEDESAAN
        # ==========================================
        # Stasiun dibuat kecil dan ringan agar tetap cocok dengan tema desa.
        # Posisi di ujung jalur rel, tidak mengganggu perlintasan utama.
        st_z = -105

        # Peron kiri dan kanan rel
        # Area tengah X -3 sampai 3 dibiarkan kosong untuk jalur kereta.
        add(
            ColorCube(
                app,
                pos=(-5.8, 0.18, st_z),
                scale=(2.4, 0.35, 24.0),
                color=(0.48, 0.48, 0.46),
            )
        )
        add(
            ColorCube(
                app,
                pos=(5.8, 0.18, st_z),
                scale=(2.4, 0.35, 24.0),
                color=(0.48, 0.48, 0.46),
            )
        )

        # Garis tepi peron warna kuning
        add(
            ColorCube(
                app,
                pos=(-3.4, 0.58, st_z),
                scale=(0.08, 0.04, 23.0),
                color=(0.95, 0.80, 0.15),
            )
        )
        add(
            ColorCube(
                app,
                pos=(3.4, 0.58, st_z),
                scale=(0.08, 0.04, 23.0),
                color=(0.95, 0.80, 0.15),
            )
        )

        # Tiang atap stasiun
        for z_pole in range(st_z - 18, st_z + 19, 9):
            add(
                ColorCube(
                    app,
                    pos=(-7.2, 2.3, z_pole),
                    scale=(0.18, 2.2, 0.18),
                    color=(0.28, 0.28, 0.28),
                )
            )
            add(
                ColorCube(
                    app,
                    pos=(7.2, 2.3, z_pole),
                    scale=(0.18, 2.2, 0.18),
                    color=(0.28, 0.28, 0.28),
                )
            )

        # Atap stasiun kecil
        add(
            ColorCube(
                app,
                pos=(0.0, 4.7, st_z),
                scale=(8.5, 0.18, 24.5),
                color=(0.20, 0.34, 0.24),
            )
        )

        # Bangunan kecil stasiun di sisi kanan
        add(
            ColorCube(
                app,
                pos=(13.0, 0.55, st_z + 4.0),
                scale=(2.6, 0.75, 2.0),
                color=(0.78, 0.70, 0.58),
            )
        )
        add(
            ColorCube(
                app,
                pos=(13.0, 1.45, st_z + 4.0),
                scale=(2.9, 0.18, 2.3),
                color=(0.55, 0.20, 0.08),
            )
        )

        # Pintu dan jendela bangunan stasiun
        add(
            ColorCube(
                app,
                pos=(13.0, 0.42, st_z + 6.05),
                scale=(0.38, 0.48, 0.05),
                color=(0.24, 0.12, 0.05),
            )
        )
        add(
            ColorCube(
                app,
                pos=(12.1, 0.78, st_z + 6.08),
                scale=(0.30, 0.25, 0.05),
                color=(0.08, 0.13, 0.16),
            )
        )
        add(
            ColorCube(
                app,
                pos=(13.9, 0.78, st_z + 6.08),
                scale=(0.30, 0.25, 0.05),
                color=(0.08, 0.13, 0.16),
            )
        )

        # Papan nama stasiun
        add(
            ColorCube(
                app,
                pos=(0.0, 2.2, st_z + 20.5),
                scale=(2.4, 0.35, 0.10),
                color=(0.95, 0.92, 0.75),
            )
        )
        add(
            ColorCube(
                app,
                pos=(0.0, 2.55, st_z + 20.45),
                scale=(0.08, 0.50, 0.08),
                color=(0.20, 0.20, 0.20),
            )
        )

        # Bangku tunggu sederhana
        for bench_z in [st_z - 10, st_z, st_z + 10]:
            add(
                ColorCube(
                    app,
                    pos=(-6.0, 0.75, bench_z),
                    scale=(1.2, 0.12, 0.28),
                    color=(0.38, 0.22, 0.10),
                )
            )
            add(
                ColorCube(
                    app,
                    pos=(6.0, 0.75, bench_z),
                    scale=(1.2, 0.12, 0.28),
                    color=(0.38, 0.22, 0.10),
                )
            )

        # Lampu kecil stasiun
        for lamp_z in [st_z - 15, st_z, st_z + 15]:
            add(
                ColorCube(
                    app,
                    pos=(-7.4, 4.2, lamp_z),
                    scale=(0.35, 0.08, 0.35),
                    color=(1.0, 0.95, 0.65),
                )
            )
            add(
                ColorCube(
                    app,
                    pos=(7.4, 4.2, lamp_z),
                    scale=(0.35, 0.08, 0.35),
                    color=(1.0, 0.95, 0.65),
                )
            )
        
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