from model import ColorCube, ColorPyramid, TexturedCube
from pyglm import glm
import math
import random

class Vehicle:
    def __init__(self, app, color):
        self.app = app
        self.pos = glm.vec3(0, -10, 0) # Hidden
        self.color = color
        self.direction = 1 # 1: X+, -1: X-
        self.orig_speed = 7.0
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
        # Diperbesar 1.6x dari ukuran sebelumnya agar lebih presisi dengan lebar jalan

        if self.v_type == 0: # SEDAN (Kecil & Ceper)
            self.length, self.orig_speed, self.safe_distance = 4.0, random.uniform(8, 10), 7.0
            self.body = ColorCube(app, color=color, scale=(1.92, 0.4, 0.8))
            self.body.relative_offset = glm.vec3(0, 0, 0)
            self.cabin = ColorCube(app, color=glass_color, scale=(0.8, 0.4, 0.72))
            self.cabin.relative_offset = glm.vec3(0.0, 0.8, 0)
            self.parts.extend([self.body, self.cabin])
            w_offs = [glm.vec3(1.12, -0.32, 0.8), glm.vec3(1.12, -0.32, -0.8), glm.vec3(-1.12, -0.32, 0.8), glm.vec3(-1.12, -0.32, -0.8)]
            w_size = 0.4

        elif self.v_type == 1: # TRUK BESAR (Raksasa Jalanan)
            self.length, self.orig_speed, self.safe_distance = 9.6, random.uniform(4, 6), 12.8
            self.cabin = ColorCube(app, color=color, scale=(1.6, 1.92, 1.76))
            self.cabin.relative_offset = glm.vec3(3.2, 1.28, 0)
            self.window = ColorCube(app, color=glass_color, scale=(0.16, 0.8, 1.6))
            self.window.relative_offset = glm.vec3(4.8, 1.92, 0)
            # Bak kargo truk jauh lebih besar dan tinggi
            self.body = ColorCube(app, color=(0.3, 0.3, 0.3), scale=(5.6, 2.56, 1.92))
            self.body.relative_offset = glm.vec3(-2.4, 1.92, 0)
            self.parts.extend([self.cabin, self.window, self.body])
            # Roda truk lebih banyak dan lebih besar
            w_offs = [glm.vec3(3.2, -0.32, 1.6), glm.vec3(3.2, -0.32, -1.6), 
                    glm.vec3(-1.6, -0.32, 1.6), glm.vec3(-1.6, -0.32, -1.6), 
                    glm.vec3(-4.48, -0.32, 1.6), glm.vec3(-4.48, -0.32, -1.6)]
            w_size = 0.72 

        elif self.v_type == 2: # HATCHBACK (Paling Kecil/Kompak)
            self.length, self.orig_speed, self.safe_distance = 3.2, random.uniform(8, 10), 6.4
            self.body = ColorCube(app, color=color, scale=(1.44, 0.4, 0.8))
            self.body.relative_offset = glm.vec3(0, 0, 0)
            self.cabin = ColorCube(app, color=glass_color, scale=(0.64, 0.4, 0.72))
            self.cabin.relative_offset = glm.vec3(-0.16, 0.8, 0)
            self.parts.extend([self.body, self.cabin])
            w_offs = [glm.vec3(0.8, -0.32, 0.8), glm.vec3(0.8, -0.32, -0.8), glm.vec3(-0.8, -0.32, 0.8), glm.vec3(-0.8, -0.32, -0.8)]
            w_size = 0.35

        elif self.v_type == 3: # PICK-UP (Sedang)
            self.length, self.orig_speed, self.safe_distance = 4.8, random.uniform(6, 8), 8.0
            self.head = ColorCube(app, color=color, scale=(0.96, 0.8, 0.88))
            self.head.relative_offset = glm.vec3(1.28, 0.48, 0)
            self.window = ColorCube(app, color=glass_color, scale=(0.16, 0.48, 0.8))
            self.window.relative_offset = glm.vec3(2.16, 0.8, 0)
            self.bak_floor = ColorCube(app, color=(0.2, 0.2, 0.2), scale=(1.92, 0.16, 0.88))
            self.bak_floor.relative_offset = glm.vec3(-0.96, 0.08, 0)
            self.wall_l = ColorCube(app, color=color, scale=(1.92, 0.32, 0.08))
            self.wall_l.relative_offset = glm.vec3(-0.96, 0.48, 0.8)
            self.wall_r = ColorCube(app, color=color, scale=(1.92, 0.32, 0.08))
            self.wall_r.relative_offset = glm.vec3(-0.96, 0.48, -0.8)
            self.parts.extend([self.head, self.window, self.bak_floor, self.wall_l, self.wall_r])
            w_offs = [glm.vec3(1.28, -0.32, 0.88), glm.vec3(1.28, -0.32, -0.88), glm.vec3(-1.28, -0.32, 0.88), glm.vec3(-1.28, -0.32, -0.88)]
            w_size = 0.45

        elif self.v_type == 4: # MOBIL PEDESAAN (Besar, tapi masih di bawah Truk)
            self.length, self.orig_speed, self.safe_distance = 6.08, random.uniform(5, 7), 9.6
            self.body = ColorCube(app, color=color, scale=(2.24, 0.96, 1.04))
            self.body.relative_offset = glm.vec3(0, 0.8, 0)
            self.win_l = ColorCube(app, color=glass_color, scale=(1.28, 0.48, 0.016))
            self.win_l.relative_offset = glm.vec3(-0.16, 1.92, 1.04)
            self.win_r = ColorCube(app, color=glass_color, scale=(1.28, 0.48, 0.016))
            self.win_r.relative_offset = glm.vec3(-0.16, 1.92, -1.04)
            self.roof = ColorCube(app, color=color, scale=(1.6, 0.16, 0.96))
            self.roof.relative_offset = glm.vec3(-0.16, 2.56, 0)
            self.parts.extend([self.body, self.win_l, self.win_r, self.roof])
            w_offs = [glm.vec3(1.44, -0.4, 1.04), glm.vec3(1.44, -0.4, -1.04), glm.vec3(-1.44, -0.4, 1.04), glm.vec3(-1.44, -0.4, -1.04)]
            w_size = 0.51

        # --- PEMBUATAN RODA SEGI-8 (OKTAGON) ---
        w_thick = 0.24
        for off in w_offs:
            # Kubus 1 (Lurus)
            w1 = ColorCube(app, color=(0.15, 0.15, 0.15), scale=(w_size, w_size, w_thick))
            w1.relative_offset = off
            w1.base_rot = 0.0
            
            # Kubus 2 (Miring 45 derajat)
            w2 = ColorCube(app, color=(0.15, 0.15, 0.15), scale=(w_size, w_size, w_thick))
            w2.relative_offset = off
            w2.base_rot = 0.785398

            
            self.wheels.extend([w1, w2])
            
        self.all_parts = self.parts + self.wheels
        self.deceleration, self.accel_rate = 10.0, 8.0

    def update(self):
        if not self.active: return
        dt = self.app.delta_time
        self.wheel_rot += abs(self.current_speed) * dt * 5.0
        
        # Update Body
        self.body.pos = glm.vec3(self.pos)
        self.body.m_model = self.body.get_model_matrix()
        
        # Update Cabin
        self.cabin.pos = self.pos + glm.vec3(0, 0.45, 0)
        self.cabin.m_model = self.cabin.get_model_matrix()
        
        # Update Wheels (Relative to X-axis forward)
        w_offsets = [
            glm.vec3(0.6, -0.2, 0.4), glm.vec3(0.6, -0.2, -0.4),
            glm.vec3(-0.6, -0.2, 0.4), glm.vec3(-0.6, -0.2, -0.4)
        ]
        for i, wheel in enumerate(self.wheels):
            wheel.pos = self.pos + w_offsets[i]
            wheel.rot.z = -self.wheel_rot * self.direction # Putar roda di sumbu Z
            wheel.m_model = wheel.get_model_matrix()

    def render(self):
        if not self.active: return
        for part in self.parts:
            part.render()


class GradeCrossingSignal:
    def __init__(self, scene, pos, rotation_y, gate_pivot_side):
        self.scene, self.app, self.pos = scene, scene.app, glm.vec3(pos)
        self.rotation_y, self.gate_pivot_side = rotation_y, gate_pivot_side
        self.parts, self.mast_lights, self.arm_lights = [], [], []        

        # 1. Concrete Base
        self.parts.append(ColorCube(self.app, pos=self.pos + glm.vec3(0, 0.1, 0), scale=(0.5, 0.1, 0.5), color=(0.5, 0.5, 0.5)))

        # 2. Main Mast
        self.parts.append(TexturedCube(self.app, pos=self.pos + glm.vec3(0, 1.5, 0), scale=(0.15, 1.5, 0.15), texture_id=0, uv_offset=(0, 0), uv_scale=(1, 0.5)))

        # 3. Gate Mechanism Box
        self.parts.append(ColorCube(self.app, pos=self.pos + glm.vec3(0, 1.0, 0), scale=(0.25, 0.25, 0.25), color=(0.1, 0.1, 0.1)))

        # 4. Barrier Gate Arm
        self.gate_arm = TexturedCube(self.app, pos=self.pos + glm.vec3(0, 1.0, 0), scale=(0.1, 0.1, 9.0), texture_id=0, uv_offset=(0, 0), uv_scale=(1, 0.5))
        self.gate_arm.pivot_offset = glm.vec3(0, 0, gate_pivot_side * 9.0)
        self.parts.append(self.gate_arm)

        # 5. Crossbuck blades (Detailed, facing traffic)
        # Use yaw = rotation_y + 90 to face traffic. Offset slightly to avoid mast overlap.
        cb_yaw = rotation_y + 90
        offset_dir = glm.vec3(math.sin(glm.radians(rotation_y)), 0, math.cos(glm.radians(rotation_y)))
        cb_pos = self.pos + glm.vec3(0, 2.8, 0) + offset_dir * 0.22       
        # Crossbuck size 4-5x wider than mast (mast diam=0.3, width=1.5 is 5x)
        cb1 = TexturedCube(self.app, pos=cb_pos, scale=(1.5, 0.25, 0.05), rot=(0, cb_yaw, 45), texture_id=0, uv_offset=(0, 0.5), uv_scale=(1, 0.5)) 
        cb2 = TexturedCube(self.app, pos=cb_pos, scale=(1.5, 0.25, 0.05), rot=(0, cb_yaw, -45), texture_id=0, uv_offset=(0, 0.5), uv_scale=(1, 0.5))
        self.parts.extend([cb1, cb2])

        # 6. Lights Housing & Main Warning Lights (Facing traffic)        
        housing_pos = self.pos + glm.vec3(0, 2.1, 0) + offset_dir * 0.22  
        housing = ColorCube(self.app, pos=housing_pos, scale=(1.0, 0.2, 0.1), rot=(0, cb_yaw, 0), color=(0.1, 0.1, 0.1))
        self.parts.append(housing)

        # Place large red circles/boxes on housing
        side_dir = glm.vec3(math.sin(glm.radians(cb_yaw)), 0, math.cos(glm.radians(cb_yaw)))
        for side in [-1, 1]:
            lp = housing_pos + side_dir * (side * 0.7) + offset_dir * 0.12
            l = ColorCube(self.app, pos=lp, scale=(0.35, 0.35, 0.05), rot=(0, cb_yaw, 0), color=(0.4, 0, 0))
            self.mast_lights.append(l); self.parts.append(l)

        # 7. Gray Bell Cap
        self.parts.append(ColorCube(self.app, pos=self.pos + glm.vec3(0, 3.2, 0), scale=(0.2, 0.15, 0.2), color=(0.4, 0.4, 0.4)))

        # Add 3 sequential arm lights (Near hinge, middle, tip)
        for i in range(3):
            al = ColorCube(self.app, scale=(0.12, 0.12, 0.12), rot=(0, cb_yaw, 0), color=(0.4, 0, 0))
            self.arm_lights.append(al); self.parts.append(al)

        for p in self.parts: scene.add_object(p)

    def update(self, gate_angle, emissive_val):
        angle_rad = glm.radians(gate_angle)
        self.gate_arm.rot.x = -angle_rad if self.gate_pivot_side > 0 else angle_rad
        self.gate_arm.m_model = self.gate_arm.get_model_matrix()

        # Update Arm Lights world position
        arm_model = self.gate_arm.m_model
        # Local Z offsets for serial lights (gate is 18 units long, local Z is -9 to 9)
        # Hinge is at -9 if side=-1, or 9 if side=1.
        light_local_zs = [7.0, 0, -8.0] if self.gate_pivot_side > 0 else [-7.0, 0, 8.0]
        for i, lz in enumerate(light_local_zs):
            # Calculate world position based on arm matrix
            pos_w = arm_model * glm.vec4(0, 0.2, lz, 1.0) # slightly above arm (Y+0.2 local)
            self.arm_lights[i].pos = glm.vec3(pos_w)
            # Match pitch of the arm, maintain yaw facing traffic
            self.arm_lights[i].rot.x = self.gate_arm.rot.x
            self.arm_lights[i].emissive = glm.vec3(emissive_val, 0, 0)    
            self.arm_lights[i].m_model = self.arm_lights[i].get_model_matrix()

        light_emissive = glm.vec3(emissive_val, 0.0, 0.0)
        for l in self.mast_lights: l.emissive = light_emissive



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
        # Zona rural village berdasarkan tampilan kamera atas:
        # - Rumah kiri atas   : X -90 s/d -20, Z -90 s/d -20
        # - Rumah kanan atas  : X 20 s/d 95,  Z -90 s/d -20
        # - Sawah kiri bawah  : X -95 s/d -25, Z 25 s/d 95
        # - Kebun kanan bawah : X 25 s/d 65,  Z 25 s/d 95
        # - Sawah air kanan   : X 70 s/d 95,  Z 35 s/d 95
        # - Tunnel rel atas   : X -8 s/d 8,   Z -100 s/d -85
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
            "z_min": -90.0,
            "z_max": -20.0,
        }

        RIGHT_HOUSE_ZONE = {
            "x_min": 20.0,
            "x_max": 95.0,
            "z_min": -90.0,
            "z_max": -20.0,
        }

        LEFT_FARM_ZONE = {
            "x_min": -95.0,
            "x_max": -25.0,
            "z_min": 25.0,
            "z_max": 95.0,
        }

        RIGHT_FARM_ZONE = {
            "x_min": 25.0,
            "x_max": 65.0,
            "z_min": 25.0,
            "z_max": 95.0,
        }

        RIGHT_RICE_PADDY_ZONE = {
            "x_min": 70.0,
            "x_max": 95.0,
            "z_min": 35.0,
            "z_max": 95.0,
        }

        TUNNEL_ZONE = {
            "x_min": -8.0,
            "x_max": 8.0,
            "z_min": -100.0,
            "z_max": -85.0,
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

        def add_village_house_facing(
            x,
            z,
            roof_color=(0.75, 0.18, 0.08),
            body_color=(0.72, 0.64, 0.45),
            scale=1.0,
            front_dir=1,
        ):
            # Rumah desa dengan arah pintu bisa diatur.
            # front_dir = 1  berarti pintu menghadap Z positif / arah jalan raya untuk area atas.
            # front_dir = -1 berarti pintu menghadap Z negatif / arah jalan raya untuk area bawah.
            if not is_safe_environment_position(x, z):
                return

            # Pondasi rumah
            add_box(
                "village house foundation",
                x,
                0.12 * scale,
                z,
                3.4 * scale,
                0.12 * scale,
                2.7 * scale,
                (0.42, 0.42, 0.38),
            )

            # Badan rumah
            add_box(
                "village house body",
                x,
                1.05 * scale,
                z,
                2.9 * scale,
                0.95 * scale,
                2.2 * scale,
                body_color,
            )

            # Atap utama model low-poly kotak
            add_box(
                "village house roof main",
                x,
                2.25 * scale,
                z,
                3.4 * scale,
                0.35 * scale,
                2.7 * scale,
                roof_color,
            )

            # Nok/puncak atap sederhana
            add_box(
                "village house roof ridge",
                x,
                2.75 * scale,
                z,
                0.20 * scale,
                0.45 * scale,
                2.8 * scale,
                roof_color,
            )

            # Posisi sisi depan rumah
            front_z = z + front_dir * 2.24 * scale

            # Pintu depan
            add_box(
                "village house front door",
                x,
                0.65 * scale,
                front_z,
                0.38 * scale,
                0.65 * scale,
                0.04 * scale,
                (0.22, 0.11, 0.04),
            )

            # Jendela depan kiri
            add_box(
                "village house front left window",
                x - 1.0 * scale,
                1.20 * scale,
                front_z,
                0.35 * scale,
                0.28 * scale,
                0.04 * scale,
                (0.08, 0.13, 0.16),
            )

            # Jendela depan kanan
            add_box(
                "village house front right window",
                x + 1.0 * scale,
                1.20 * scale,
                front_z,
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
        # ==========================================================
        # 2A. AREA SAWAH / LADANG KIRI BAWAH
        # ==========================================================
        # Area ini mengikuti sketsa:
        # - Berada di kiri bawah map.
        # - Tidak masuk area jalan raya.
        # - Tidak masuk area rel.
        # - Dibuat menjadi 2 petak besar berpagar.
        #
        # Koordinat aman:
        # - X sekitar -90 sampai -30
        # - Z sekitar -95 sampai -30
        # ==========================================================

        def add_left_farmland_crop(x, z, height=1.0):
            # Tanaman kecil untuk ladang kiri bawah.
            # Dibuat dari batang kubus dan daun piramida agar tetap low-poly.
            add_box(
                "left farmland crop stem",
                x,
                0.16 * height,
                z,
                0.055 * height,
                0.16 * height,
                0.055 * height,
                (0.15, 0.45, 0.10),
            )

            add(
                ColorPyramid(
                    app,
                    pos=(x, 0.46 * height, z),
                    scale=(0.22 * height, 0.30 * height, 0.22 * height),
                    color=(0.10, 0.52, 0.12),
                )
            )

        def add_left_farmland_plot(
            center_x,
            center_z,
            half_x,
            half_z,
            rows,
            cols,
            soil_color,
            crop_color_variant=0,
        ):
            # Petak sawah/kebun kiri bawah.
            # center_x, center_z = titik tengah petak.
            # half_x, half_z = setengah ukuran petak.
            # rows, cols = jumlah baris dan kolom tanaman.

            # Dasar tanah petak.
            add_box(
                "left farmland soil base",
                center_x,
                -0.085,
                center_z,
                half_x,
                0.025,
                half_z,
                soil_color,
            )

            # Area sedikit lebih gelap di tengah agar terlihat seperti lahan siap tanam.
            add_box(
                "left farmland inner soil shade",
                center_x,
                -0.052,
                center_z,
                half_x - 1.4,
                0.010,
                half_z - 1.4,
                (0.30, 0.21, 0.09),
            )

            # Pagar keliling petak.
            # Sedikit dilebihkan supaya pagar tidak menindih tanaman.
            add_fence_rect(center_x, center_z, half_x + 1.2, half_z + 1.2)

            # Tanaman dibuat grid rapi seperti acuan.
            # Batas 3 unit dari pinggir agar tidak menabrak pagar.
            if rows <= 1 or cols <= 1:
                return

            usable_x = (half_x * 2.0) - 6.0
            usable_z = (half_z * 2.0) - 6.0

            for r in range(rows):
                for c in range(cols):
                    px = center_x - half_x + 3.0 + (c * (usable_x / (cols - 1)))
                    pz = center_z - half_z + 3.0 + (r * (usable_z / (rows - 1)))

                    # Variasi kecil agar tanaman tidak terlalu kaku.
                    h = 0.85 + ((r + c) % 3) * 0.08

                    if crop_color_variant == 1:
                        # Varian tanaman lebih rendah untuk petak bawah.
                        add_box(
                            "low vegetable crop",
                            px,
                            0.17 * h,
                            pz,
                            0.10 * h,
                            0.17 * h,
                            0.10 * h,
                            (0.12, 0.42, 0.10),
                        )
                        add_box(
                            "low vegetable leaf",
                            px,
                            0.38 * h,
                            pz,
                            0.22 * h,
                            0.06 * h,
                            0.22 * h,
                            (0.13, 0.55, 0.13),
                        )
                    else:
                        add_left_farmland_crop(px, pz, height=h)

        # ----------------------------------------------------------
        # PETAK LADANG ATAS KIRI BAWAH
        # ----------------------------------------------------------
        # Petak ini dibuat lebih besar dan berisi tanaman berbaris.
        # Posisi tidak terlalu dekat jalan raya, sehingga aman dari kendaraan.
        add_left_farmland_plot(
            center_x=-64.0,
            center_z=47.0,
            half_x=28.0,
            half_z=16.0,
            rows=7,
            cols=12,
            soil_color=(0.38, 0.26, 0.11),
            crop_color_variant=0,
        )


        # ----------------------------------------------------------
        # PETAK LADANG BAWAH KIRI
        # ----------------------------------------------------------
        # Petak bawah dibuat lebih hijau agar tidak monoton.
        add_left_farmland_plot(
            center_x=-64.0,
            center_z=82.0,
            half_x=28.0,
            half_z=12.0,
            rows=5,
            cols=12,
            soil_color=(0.28, 0.38, 0.13),
            crop_color_variant=1,
        )

        # ----------------------------------------------------------
        # JALUR TANAH PEMISAH PETAK
        # ----------------------------------------------------------
        # Jalur ini berada di antara petak atas dan bawah.
        # Bentuknya rapi, bukan dirt_patch acak.
        add_box(
            "left farmland horizontal dirt divider",
            -64.0,
            -0.040,
            66.5,
            29.0,
            0.018,
            0.70,
            (0.45, 0.31, 0.13),
        )

        # Jalur kecil di sisi kanan ladang, mengarah ke jalan raya.
        add_box(
            "left farmland side dirt path",
            -31.5,
            -0.040,
            63.0,
            0.75,
            0.018,
            29.0,
            (0.45, 0.31, 0.13),
        )

        # ----------------------------------------------------------
        # POHON CEMARA DI TEPI LADANG KIRI
        # ----------------------------------------------------------
        # Pohon ditaruh di tepi luar ladang agar visual lebih hidup,
        # tetapi tidak masuk ke jalan raya, rel, atau crossing.
        left_farm_trees = [
            (-92, 32, 1.10),
            (-94, 55, 0.95),
            (-91, 89, 1.20),
            (-28, 36, 1.05),
            (-26, 72, 0.90),
            (-35, 96, 1.15),
        ]

        for x, z, h in left_farm_trees:
            add_pine_tree(x, z, height=h)

        # ==========================================================
        # 2B. AREA KEBUN DAN SAWAH AIR KANAN BAWAH
        # ==========================================================
        # Area ini mengikuti sketsa bagian kanan bawah:
        # - X positif karena berada di sisi kanan layar.
        # - Z positif karena berada di bawah jalan raya pada tampilan kamera atas.
        # - Berisi kebun kering, sawah air, bunga matahari, pagar, dan pohon tepi.
        #
        # Koordinat aman:
        # - Kebun kanan bawah : X 25 s/d 65, Z 25 s/d 95
        # - Sawah air kanan   : X 70 s/d 95, Z 35 s/d 95
        # ==========================================================

        # ----------------------------------------------------------
        # KEBUN KERING KANAN BAWAH - PETAK ATAS
        # ----------------------------------------------------------
        # Petak ini berada di kanan bawah dekat jalan, tetapi tetap aman
        # karena Z sudah lebih dari 25 dan tidak masuk area jalan raya.
        add_crop_field(
            cx=48.0,
            zc=48.0,
            sx=18.0,
            sz=13.0,
            crop_rows=6,
            crop_cols=8,
        )

        # ----------------------------------------------------------
        # KEBUN KERING KANAN BAWAH - PETAK BAWAH
        # ----------------------------------------------------------
        # Petak kedua dibuat tepat di bawah petak atas agar mirip sketsa.
        add_crop_field(
            cx=48.0,
            zc=78.0,
            sx=18.0,
            sz=12.0,
            crop_rows=6,
            crop_cols=8,
        )

        # ----------------------------------------------------------
        # SAWAH AIR KANAN BAWAH - PETAK ATAS
        # ----------------------------------------------------------
        # Sawah air dibuat di sisi kanan paling pinggir.
        # Warna air sudah ditangani oleh helper add_rice_paddy().
        add_rice_paddy(
            cx=83.0,
            zc=48.0,
            sx=10.5,
            sz=13.0,
            rows=7,
            cols=4,
        )

        # ----------------------------------------------------------
        # SAWAH AIR KANAN BAWAH - PETAK BAWAH
        # ----------------------------------------------------------
        add_rice_paddy(
            cx=83.0,
            zc=80.0,
            sx=10.5,
            sz=12.0,
            rows=7,
            cols=4,
        )

        # ----------------------------------------------------------
        # JALUR TANAH PEMISAH AREA KANAN BAWAH
        # ----------------------------------------------------------
        # Jalur vertikal memisahkan kebun kering dan sawah air.
        add_box(
            "right farm vertical dirt divider",
            67.0,
            -0.040,
            64.0,
            0.70,
            0.018,
            32.0,
            (0.45, 0.31, 0.13),
        )

        # Jalur horizontal memisahkan petak atas dan bawah pada kebun kering.
        add_box(
            "right dry field horizontal dirt divider",
            48.0,
            -0.040,
            63.5,
            18.5,
            0.018,
            0.65,
            (0.45, 0.31, 0.13),
        )

        # Jalur horizontal memisahkan sawah air atas dan bawah.
        add_box(
            "right rice paddy horizontal dirt divider",
            83.0,
            -0.040,
            64.5,
            10.8,
            0.018,
            0.65,
            (0.45, 0.31, 0.13),
        )

        # ----------------------------------------------------------
        # BUNGA MATAHARI DEKAT JALAN
        # ----------------------------------------------------------
        # Bunga matahari diletakkan di atas kebun kanan bawah,
        # dekat jalan raya tetapi tidak masuk area aman jalan.
        add_sunflower_row(
            start_x=56.0,
            z=18.0,
            count=8,
            gap=2.6,
        )

        # ----------------------------------------------------------
        # POHON CEMARA TEPI KANAN BAWAH
        # ----------------------------------------------------------
        # Pohon diletakkan di pinggir map dan antar-petak agar area tidak kosong.
        # Tidak dibuat terlalu banyak supaya tetap rapi dan tidak berat.
        right_farm_trees = [
            (24, 34, 1.05),
            (24, 70, 0.95),
            (28, 96, 1.15),
            (66, 26, 1.05),
            (96, 36, 1.20),
            (97, 70, 1.05),
            (96, 94, 1.15),
        ]

        for x, z, h in right_farm_trees:
            add_pine_tree(x, z, height=h)

        # ==========================================================
        # 2C. AREA RUMAH DESA KIRI ATAS
        # ==========================================================
        # Area ini mengikuti sketsa bagian kiri atas:
        # - X negatif karena berada di sisi kiri layar.
        # - Z negatif karena berada di atas jalan raya pada tampilan kamera atas.
        # - Rumah dibuat menghadap ke arah jalan raya, yaitu ke Z positif.
        #
        # Koordinat aman:
        # - X sekitar -90 sampai -20
        # - Z sekitar -90 sampai -20
        # ==========================================================

        def add_yard_fence_with_front_gate(cx, zc, sx, sz, gate_x, gate_width=5.0):
            # Pagar halaman dengan celah/gapura di sisi depan.
            # Untuk area rumah atas, sisi depan adalah z_max karena mengarah ke jalan raya Z=0.
            x_min = cx - sx
            x_max = cx + sx
            z_min = zc - sz
            z_max = zc + sz

            gate_left = gate_x - gate_width * 0.5
            gate_right = gate_x + gate_width * 0.5

            # Pagar belakang
            add_fence_line(x_min, z_min, x_max, z_min)

            # Pagar kiri dan kanan
            add_fence_line(x_min, z_min, x_min, z_max)
            add_fence_line(x_max, z_min, x_max, z_max)

            # Pagar depan kiri, diberi gap untuk jalan masuk
            if gate_left > x_min:
                add_fence_line(x_min, z_max, gate_left, z_max)

            # Pagar depan kanan, diberi gap untuk jalan masuk
            if gate_right < x_max:
                add_fence_line(gate_right, z_max, x_max, z_max)

        def add_simple_greenhouse(x, z, scale=1.0):
            # Greenhouse kecil seperti di sketsa.
            # Dibuat dari alas, rangka putih, dan atap kaca warna biru muda.
            if not is_safe_environment_position(x, z):
                return

            # Alas greenhouse
            add_box(
                "greenhouse foundation",
                x,
                0.08 * scale,
                z,
                2.1 * scale,
                0.08 * scale,
                3.0 * scale,
                (0.50, 0.50, 0.45),
            )

            # Badan kaca
            add_box(
                "greenhouse glass body",
                x,
                0.85 * scale,
                z,
                1.9 * scale,
                0.75 * scale,
                2.7 * scale,
                (0.70, 0.88, 0.92),
            )

            # Atap greenhouse
            add_box(
                "greenhouse roof",
                x,
                1.70 * scale,
                z,
                2.0 * scale,
                0.25 * scale,
                2.8 * scale,
                (0.82, 0.92, 0.95),
            )

            # Rangka tengah
            add_box(
                "greenhouse center frame",
                x,
                0.95 * scale,
                z,
                0.06 * scale,
                0.85 * scale,
                2.9 * scale,
                (0.90, 0.90, 0.88),
            )

            # Rangka depan
            add_box(
                "greenhouse front frame",
                x,
                0.95 * scale,
                z + 2.75 * scale,
                2.0 * scale,
                0.85 * scale,
                0.05 * scale,
                (0.90, 0.90, 0.88),
            )

        # ----------------------------------------------------------
        # HALAMAN DAN RUMAH BESAR ATAP MERAH
        # ----------------------------------------------------------
        add_yard_fence_with_front_gate(
            cx=-60.0,
            zc=-72.0,
            sx=18.0,
            sz=13.0,
            gate_x=-60.0,
            gate_width=5.5,
        )

        add_village_house_facing(
            x=-60.0,
            z=-73.0,
            roof_color=(0.82, 0.22, 0.08),
            body_color=(0.74, 0.68, 0.50),
            scale=1.25,
            front_dir=1,
        )

        # Jalan masuk dari rumah besar menuju jalan raya
        add_dirt_path(
            x=-60.0,
            z=-43.0,
            sx=1.0,
            sz=18.5,
            rot_y=0,
        )

        # Halaman depan rumah besar
        add_box(
            "large red roof house yard floor",
            -60.0,
            -0.070,
            -59.0,
            7.0,
            0.012,
            4.0,
            (0.42, 0.50, 0.25),
        )

        # ----------------------------------------------------------
        # RUMAH KECIL ATAP COKELAT KIRI
        # ----------------------------------------------------------
        add_yard_fence_with_front_gate(
            cx=-82.0,
            zc=-42.0,
            sx=11.0,
            sz=10.0,
            gate_x=-82.0,
            gate_width=4.5,
        )

        add_village_house_facing(
            x=-82.0,
            z=-43.0,
            roof_color=(0.42, 0.24, 0.12),
            body_color=(0.68, 0.60, 0.42),
            scale=0.90,
            front_dir=1,
        )

        add_dirt_path(
            x=-82.0,
            z=-24.0,
            sx=0.8,
            sz=8.0,
            rot_y=0,
        )

        # ----------------------------------------------------------
        # RUMAH ATAP BIRU KIRI-TENGAH
        # ----------------------------------------------------------
        add_yard_fence_with_front_gate(
            cx=-36.0,
            zc=-42.0,
            sx=11.5,
            sz=10.0,
            gate_x=-36.0,
            gate_width=4.5,
        )

        add_village_house_facing(
            x=-36.0,
            z=-43.0,
            roof_color=(0.05, 0.22, 0.70),
            body_color=(0.70, 0.66, 0.48),
            scale=0.95,
            front_dir=1,
        )

        add_dirt_path(
            x=-36.0,
            z=-24.0,
            sx=0.8,
            sz=8.0,
            rot_y=0,
        )

        # ----------------------------------------------------------
        # GREENHOUSE KECIL DI ANTARA RUMAH KIRI
        # ----------------------------------------------------------
        add_simple_greenhouse(
            x=-58.0,
            z=-42.0,
            scale=0.95,
        )

        # ----------------------------------------------------------
        # GUBUK KECIL / SHED DEKAT AREA RUMAH
        # ----------------------------------------------------------
        add_small_shed(
            x=-46.0,
            z=-82.0,
            roof_color=(0.70, 0.20, 0.08),
            scale=0.85,
        )

        # ----------------------------------------------------------
        # POHON CEMARA AREA RUMAH KIRI ATAS
        # ----------------------------------------------------------
        # Pohon dibuat menyebar di tepi halaman, bukan di tengah jalan.
        left_upper_house_trees = [
            (-92, -78, 1.15),
            (-91, -55, 1.00),
            (-94, -28, 1.10),
            (-74, -88, 0.95),
            (-45, -88, 1.20),
            (-24, -72, 1.00),
            (-24, -50, 1.15),
            (-25, -28, 0.90),
            (-68, -24, 1.05),
        ]

        for x, z, h in left_upper_house_trees:
            add_pine_tree(x, z, height=h)

        # ==========================================================
        # 2D. AREA RUMAH DESA KANAN ATAS
        # ==========================================================
        # Area ini mengikuti sketsa bagian kanan atas:
        # - X positif karena berada di sisi kanan layar.
        # - Z negatif karena berada di atas jalan raya pada tampilan kamera atas.
        # - Rumah dibuat menghadap ke arah jalan raya, yaitu ke Z positif.
        #
        # Koordinat aman:
        # - X sekitar 20 sampai 95
        # - Z sekitar -90 sampai -20
        # ==========================================================

        # ----------------------------------------------------------
        # HALAMAN DAN RUMAH BESAR ATAP ABU/HITAM
        # ----------------------------------------------------------
        # Rumah ini menjadi objek dominan di kanan atas seperti acuan.
        add_yard_fence_with_front_gate(
            cx=58.0,
            zc=-72.0,
            sx=16.0,
            sz=13.0,
            gate_x=58.0,
            gate_width=5.5,
        )

        add_village_house_facing(
            x=58.0,
            z=-73.0,
            roof_color=(0.18, 0.18, 0.18),
            body_color=(0.68, 0.64, 0.46),
            scale=1.25,
            front_dir=1,
        )

        # Teras kecil di depan rumah besar kanan atas
        add_box(
            "right upper dark roof house front terrace",
            58.0,
            -0.055,
            -58.5,
            5.5,
            0.015,
            2.5,
            (0.44, 0.48, 0.32),
        )

        # Jalan tanah dari rumah besar kanan atas menuju jalan raya
        add_dirt_path(
            x=58.0,
            z=-43.0,
            sx=1.0,
            sz=18.0,
            rot_y=0,
        )

        # ----------------------------------------------------------
        # RUMAH ATAP MERAH KANAN TENGAH
        # ----------------------------------------------------------
        add_yard_fence_with_front_gate(
            cx=45.0,
            zc=-42.0,
            sx=11.5,
            sz=10.0,
            gate_x=45.0,
            gate_width=4.5,
        )

        add_village_house_facing(
            x=45.0,
            z=-43.0,
            roof_color=(0.66, 0.22, 0.10),
            body_color=(0.70, 0.64, 0.45),
            scale=0.98,
            front_dir=1,
        )

        add_dirt_path(
            x=45.0,
            z=-24.0,
            sx=0.8,
            sz=8.0,
            rot_y=0,
        )

        # Gubuk kecil di halaman rumah atap merah
        add_small_shed(
            x=36.5,
            z=-31.0,
            roof_color=(0.65, 0.22, 0.08),
            scale=0.75,
        )

        # ----------------------------------------------------------
        # RUMAH ATAP BIRU KANAN
        # ----------------------------------------------------------
        add_yard_fence_with_front_gate(
            cx=78.0,
            zc=-42.0,
            sx=12.0,
            sz=10.0,
            gate_x=78.0,
            gate_width=4.5,
        )

        add_village_house_facing(
            x=78.0,
            z=-43.0,
            roof_color=(0.04, 0.20, 0.72),
            body_color=(0.70, 0.67, 0.50),
            scale=1.02,
            front_dir=1,
        )

        add_dirt_path(
            x=78.0,
            z=-24.0,
            sx=0.8,
            sz=8.0,
            rot_y=0,
        )

        # ----------------------------------------------------------
        # GUBUK KECIL DEKAT SISI KANAN ATAS
        # ----------------------------------------------------------
        # Objek ini mengisi area kanan dekat tepi map, seperti bangunan kecil
        # di sketsa acuan.
        add_small_shed(
            x=92.0,
            z=-23.0,
            roof_color=(0.60, 0.28, 0.12),
            scale=0.80,
        )

        # Pagar pendek untuk gubuk kecil kanan
        add_fence_line(87.0, -28.0, 97.0, -28.0)
        add_fence_line(97.0, -28.0, 97.0, -18.0)
        add_fence_line(97.0, -18.0, 87.0, -18.0)
        add_fence_line(87.0, -18.0, 87.0, -28.0)

        # ----------------------------------------------------------
        # JALAN TANAH SISI KANAN ATAS
        # ----------------------------------------------------------
        # Jalur ini dibuat seperti akses kecil di kanan atas map.
        # Tidak terlalu lebar agar tidak mengganggu rumah.
        add_dirt_path(
            x=91.0,
            z=-58.0,
            sx=0.9,
            sz=25.0,
            rot_y=0,
        )

        # ----------------------------------------------------------
        # POHON CEMARA AREA RUMAH KANAN ATAS
        # ----------------------------------------------------------
        # Pohon dibuat di tepi halaman agar area kanan atas tidak kosong,
        # tetapi tetap menjauh dari rel dan jalan raya.
        right_upper_house_trees = [
            (24, -82, 1.10),
            (26, -58, 0.95),
            (25, -28, 1.05),
            (40, -88, 1.15),
            (72, -88, 1.00),
            (95, -82, 1.20),
            (96, -58, 1.05),
            (96, -36, 0.95),
            (68, -24, 1.00),
        ]

        for x, z, h in right_upper_house_trees:
            add_pine_tree(x, z, height=h)

        # ==========================================================
        # 2E. GUA / TUNNEL DI UJUNG ATAS REL
        # ==========================================================
        # Pada tampilan kamera saat ini:
        # - bagian atas layar = Z negatif
        # Jadi gua/tunnel diletakkan di ujung atas rel.
        add_tunnel(
            x=0.0,
            z=-94.0,
        )

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
        # STASIUN KECIL PEDESAAN - AREA AWAL KERETA
        # ==========================================
        # Stasiun sengaja ditempatkan di area awal kereta (bagian bawah map),
        # sedangkan ujung atas rel dipakai untuk gua/tunnel.
        st_z = 88

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

        def add_train_part(local_offset, scale, color, rot=(0, 0, 0)):
            """
            Membuat bagian kereta relatif terhadap titik anchor kereta.
            Anchor kereta: glm.vec3(0, 1.75, self.train_z)
            """
            train_anchor = glm.vec3(0, 1.75, self.train_z)
            obj = ColorCube(
                app,
                pos=train_anchor + glm.vec3(local_offset),
                rot=rot,
                scale=scale,
                color=color
            )
            obj.relative_offset = glm.vec3(local_offset)
            self.train_parts.append(obj)
            add(obj)
            return obj

        def add_train_wheel(local_offset):
            """
            Roda/bogie kereta dibuat terpisah agar bisa diputar saat kereta bergerak.
            """
            train_anchor = glm.vec3(0, 1.75, self.train_z)
            wheel = ColorCube(
                app,
                pos=train_anchor + glm.vec3(local_offset),
                scale=(0.28, 0.28, 0.28),
                color=(0.04, 0.04, 0.04)
            )
            wheel.relative_offset = glm.vec3(local_offset)
            self.train_wheels.append((wheel, 0.0))
            add(wheel)
            return wheel

        # =========================
        # A. LOKOMOTIF
        # =========================
        # Arah depan kereta berada di sisi +Z
        loco_center_z = 2.2

        # Body utama lokomotif putih
        add_train_part(
            local_offset=(0.0, -0.05, loco_center_z),
            scale=(1.55, 1.05, 2.70),
            color=(0.92, 0.92, 0.88)
        )

        # Atap lokomotif abu-abu
        add_train_part(
            local_offset=(0.0, 1.05, loco_center_z),
            scale=(1.35, 0.18, 2.35),
            color=(0.72, 0.72, 0.70)
        )

        # Bagian bawah lokomotif merah seperti foto
        add_train_part(
            local_offset=(0.0, -1.00, loco_center_z + 1.65),
            scale=(1.52, 0.22, 0.75),
            color=(0.72, 0.05, 0.03)
        )

        # Muka depan lokomotif putih
        add_train_part(
            local_offset=(0.0, 0.10, loco_center_z + 2.72),
            scale=(1.50, 0.90, 0.08),
            color=(0.95, 0.95, 0.92)
        )

        # Kaca depan lokomotif
        add_train_part(
            local_offset=(-0.45, 0.48, loco_center_z + 2.82),
            scale=(0.36, 0.30, 0.04),
            color=(0.05, 0.08, 0.12)
        )
        add_train_part(
            local_offset=(0.45, 0.48, loco_center_z + 2.82),
            scale=(0.36, 0.30, 0.04),
            color=(0.05, 0.08, 0.12)
        )

        # Lampu depan lokomotif
        add_train_part(
            local_offset=(-0.65, 0.88, loco_center_z + 2.86),
            scale=(0.13, 0.13, 0.04),
            color=(1.00, 0.95, 0.65)
        )
        add_train_part(
            local_offset=(0.65, 0.88, loco_center_z + 2.86),
            scale=(0.13, 0.13, 0.04),
            color=(1.00, 0.95, 0.65)
        )
        add_train_part(
            local_offset=(0.0, 0.88, loco_center_z + 2.86),
            scale=(0.13, 0.13, 0.04),
            color=(1.00, 0.95, 0.65)
        )

        # Strip oranye dan biru di sisi lokomotif
        for side_x in [-1.60, 1.60]:
            add_train_part(
                local_offset=(side_x, -0.05, loco_center_z),
                scale=(0.035, 0.10, 2.25),
                color=(1.00, 0.38, 0.02)
            )
            add_train_part(
                local_offset=(side_x, -0.23, loco_center_z),
                scale=(0.035, 0.055, 2.10),
                color=(0.02, 0.18, 0.65)
            )

            # Panel kecil biru-oranye sebagai pengganti logo tekstual
            add_train_part(
                local_offset=(side_x, 0.35, loco_center_z + 0.75),
                scale=(0.04, 0.23, 0.22),
                color=(0.02, 0.18, 0.65)
            )
            add_train_part(
                local_offset=(side_x, 0.15, loco_center_z + 0.98),
                scale=(0.04, 0.12, 0.20),
                color=(1.00, 0.38, 0.02)
            )

        # Ventilasi samping lokomotif
        for side_x in [-1.61, 1.61]:
            for z in [1.05, 1.35, 1.65]:
                add_train_part(
                    local_offset=(side_x, 0.45, z),
                    scale=(0.035, 0.07, 0.16),
                    color=(0.12, 0.12, 0.12)
                )

        # Box/mesin kecil di atas atap
        for z in [0.8, 1.7, 2.6]:
            add_train_part(
                local_offset=(0.0, 1.28, z),
                scale=(0.45, 0.12, 0.28),
                color=(0.20, 0.20, 0.20)
            )

        # Roda lokomotif
        for z in [0.45, 1.55, 2.65, 3.75]:
            add_train_wheel((-0.88, -1.23, z))
            add_train_wheel((0.88, -1.23, z))

        # =========================
        # B. GERBONG PENUMPANG
        # =========================
        coach_centers = [-4.8, -12.2, -19.6]

        for coach_z in coach_centers:
            # Body gerbong putih
            add_train_part(
                local_offset=(0.0, -0.02, coach_z),
                scale=(1.45, 0.95, 3.35),
                color=(0.94, 0.94, 0.91)
            )

            # Atap gerbong abu-abu terang
            add_train_part(
                local_offset=(0.0, 0.95, coach_z),
                scale=(1.35, 0.18, 3.10),
                color=(0.78, 0.78, 0.76)
            )

            # Bagian bawah gerbong abu gelap
            add_train_part(
                local_offset=(0.0, -0.93, coach_z),
                scale=(1.45, 0.17, 3.20),
                color=(0.16, 0.16, 0.16)
            )

            # Strip oranye dan biru di kedua sisi gerbong
            for side_x in [-1.50, 1.50]:
                add_train_part(
                    local_offset=(side_x, -0.10, coach_z),
                    scale=(0.035, 0.075, 3.05),
                    color=(1.00, 0.38, 0.02)
                )
                add_train_part(
                    local_offset=(side_x, -0.25, coach_z),
                    scale=(0.035, 0.045, 3.05),
                    color=(0.02, 0.18, 0.65)
                )

                # Deretan jendela gerbong
                for w in range(7):
                    z_window = coach_z - 2.25 + (w * 0.75)
                    add_train_part(
                        local_offset=(side_x, 0.35, z_window),
                        scale=(0.035, 0.23, 0.22),
                        color=(0.06, 0.09, 0.13)
                    )

                # Pintu gerbong depan-belakang
                add_train_part(
                    local_offset=(side_x, 0.10, coach_z - 2.85),
                    scale=(0.035, 0.48, 0.18),
                    color=(0.82, 0.82, 0.78)
                )
                add_train_part(
                    local_offset=(side_x, 0.10, coach_z + 2.85),
                    scale=(0.035, 0.48, 0.18),
                    color=(0.82, 0.82, 0.78)
                )

            # Bogie/roda gerbong
            for z in [coach_z - 2.15, coach_z + 2.15]:
                add_train_wheel((-0.85, -1.20, z))
                add_train_wheel((0.85, -1.20, z))
    
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

        # 4. DEKORASI LINGKUNGAN (Trees)
        tree_positions = [
            (-20, 0.85, -20), (-22, 0.85, -18), (-18, 0.85, -22), # Pojok Kiri Belakang
            (20, 0.85, -20), (22, 0.85, -18), (18, 0.85, -22),   # Pojok Kanan Belakang
            (-20, 0.85, 20), (-22, 0.85, 18), (-18, 0.85, 22),   # Pojok Kiri Depan
            (20, 0.85, 20), (22, 0.85, 18), (18, 0.85, 22)       # Pojok Kanan Depan
        ]
        
        for pos in tree_positions:
            # Batang Pohon
            trunk = ColorCube(app, pos=pos, scale=(0.3, 1.0, 0.3), color=(0.3, 0.2, 0.1))
            # Daun (Top)
            leaf_pos = glm.vec3(pos) + glm.vec3(0, 1.2, 0)
            leaf = ColorCube(app, pos=leaf_pos, scale=(1.2, 1.2, 1.2), color=(0.1, 0.6, 0.1))
            add(trunk); add(leaf)

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
        # Batas fisik jalan adalah 100 unit (scale=100).
        # Spawn di luar batas visual (-105/105) agar masuk dengan smooth.
        spawn_x = -105.0 if direction == 1 else 105.0
        for v in self.vehicles_pool:
            if v.active and v.direction == direction:
                # Cek jarak aman agar tidak menumpuk saat spawn baru
                if abs(v.pos.x - spawn_x) < 12.0:
                    return 
                    
        for car in self.vehicles_pool:
            if not car.active:
                car.active = True
                car.direction = direction
                car.pos.y = 0.8  
                car.pos.z = 4.0 if direction == 1 else -4.0 
                car.pos.x = spawn_x
                car.current_speed = car.orig_speed * direction
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
                
                # PERBAIKAN BUG VANISHING:
                # Road boundary adalah 100. Gunakan 110 agar mobil benar-benar keluar dari pandangan 
                # (termasuk panjang bodi mobil) sebelum di-reset ke ujung lainnya.
                if lane_dir == 1 and car.pos.x > 110.0: car.pos.x = -110.0
                if lane_dir == -1 and car.pos.x < -110.0: car.pos.x = 110.0

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

        # --- UPDATE MATRIX KERETA ---
        # Semua bagian kereta bergerak mengikuti anchor utama,
        # tetapi tetap mempertahankan jarak relatif antar lokomotif dan gerbong.
        train_anchor = glm.vec3(0, 1.75, self.train_z)

        for part in self.train_parts:
            part.pos = train_anchor + part.relative_offset
            part.m_model = part.get_model_matrix()

        # Roda Kereta berputar sinkron saat kereta bergerak
        wheel_rot_angle = self.train_z * 2.0
        for wheel, _ in self.train_wheels:
            wheel.pos = train_anchor + wheel.relative_offset
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
