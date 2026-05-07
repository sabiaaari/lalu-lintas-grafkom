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
            self.body.relative_offset = glm.vec3(0, 0, 0)
            self.cabin = ColorCube(app, color=glass_color, scale=(0.5, 0.25, 0.45))
            self.cabin.relative_offset = glm.vec3(0.0, 0.5, 0)
            self.parts.extend([self.body, self.cabin])
            w_offs = [glm.vec3(0.6, -0.2, 0.45), glm.vec3(0.6, -0.2, -0.45), glm.vec3(-0.6, -0.2, 0.45), glm.vec3(-0.6, -0.2, -0.45)]

        elif self.v_type == 1: # TRUK BESAR
            self.length, self.orig_speed, self.safe_distance = 3.5, random.uniform(4, 6), 5.5
            self.cabin = ColorCube(app, color=color, scale=(0.6, 0.6, 0.5))
            self.cabin.relative_offset = glm.vec3(1.0, 0.4, 0)
            self.window = ColorCube(app, color=glass_color, scale=(0.1, 0.3, 0.45))
            self.window.relative_offset = glm.vec3(1.55, 0.6, 0)
            self.body = ColorCube(app, color=(0.3, 0.3, 0.3), scale=(1.2, 0.6, 0.55))
            self.body.relative_offset = glm.vec3(-0.6, 0.4, 0)
            self.parts.extend([self.cabin, self.window, self.body])
            w_offs = [glm.vec3(1.1, -0.2, 0.45), glm.vec3(1.1, -0.2, -0.45), glm.vec3(-0.4, -0.2, 0.45), glm.vec3(-0.4, -0.2, -0.45), glm.vec3(-1.2, -0.2, 0.45), glm.vec3(-1.2, -0.2, -0.45)]

        elif self.v_type == 2: # HATCHBACK
            self.length, self.orig_speed, self.safe_distance = 1.7, random.uniform(8, 10), 3.5
            self.body = ColorCube(app, color=color, scale=(0.85, 0.25, 0.5))
            self.body.relative_offset = glm.vec3(0, 0, 0)
            self.cabin = ColorCube(app, color=glass_color, scale=(0.4, 0.25, 0.45))
            self.cabin.relative_offset = glm.vec3(-0.1, 0.5, 0)
            self.parts.extend([self.body, self.cabin])
            w_offs = [glm.vec3(0.5, -0.2, 0.45), glm.vec3(0.5, -0.2, -0.45), glm.vec3(-0.5, -0.2, 0.45), glm.vec3(-0.5, -0.2, -0.45)]

        elif self.v_type == 3: # PICK-UP
            self.length, self.orig_speed, self.safe_distance = 2.2, random.uniform(6, 8), 4.5
            self.head = ColorCube(app, color=color, scale=(0.4, 0.45, 0.45))
            self.head.relative_offset = glm.vec3(0.6, 0.3, 0)
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
            self.win_l = ColorCube(app, color=glass_color, scale=(0.6, 0.2, 0.01))
            self.win_l.relative_offset = glm.vec3(-0.1, 1.0, 0.55)
            self.win_r = ColorCube(app, color=glass_color, scale=(0.6, 0.2, 0.01))
            self.win_r.relative_offset = glm.vec3(-0.1, 1.0, -0.55)
            self.roof = ColorCube(app, color=color, scale=(0.8, 0.1, 0.5))
            self.roof.relative_offset = glm.vec3(-0.1, 1.3, 0)
            self.parts.extend([self.body, self.win_l, self.win_r, self.roof])
            w_offs = [glm.vec3(0.6, -0.2, 0.45), glm.vec3(0.6, -0.2, -0.45), glm.vec3(-0.6, -0.2, 0.45), glm.vec3(-0.6, -0.2, -0.45)]

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
        
        self.state = 'IDLE' 
        self.gate_angle = 90.0 
        self.gate_speed = 60.0 
        
        # Pengaturan Kereta (Dibalik, mulai dari 50 ke -50)
        self.TRAIN_START_Z = 50.0
        self.TRAIN_END_Z = -50.0
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

        # ==========================================
        # 1. LINGKUNGAN JALAN & REL KERETA
        # ==========================================
        add(ColorCube(app, pos=(0, -0.25, 0), scale=(50, 0.1, 50), color=(0.25, 0.45, 0.25)))
        add(ColorCube(app, pos=(0, -0.1, 0), scale=(50, 0.05, 5), color=(0.15, 0.15, 0.15)))
        add(ColorCube(app, pos=(0, 0.0, 5.5), scale=(50, 0.1, 0.5), color=(0.6, 0.6, 0.6)))
        add(ColorCube(app, pos=(0, 0.0, -5.5), scale=(50, 0.1, 0.5), color=(0.6, 0.6, 0.6)))

        for x_pos in range(-48, 52, 4):
            add(ColorCube(app, pos=(x_pos, -0.04, 0), scale=(1.0, 0.01, 0.15), color=(0.9, 0.9, 0.9)))

        add(ColorCube(app, pos=(0, -0.05, 0), scale=(3.5, 0.1, 50), color=(0.35, 0.35, 0.35)))
        add(ColorCube(app, pos=(-1.5, 0.15, 0), scale=(0.1, 0.1, 50), color=(0.7, 0.7, 0.7)))
        add(ColorCube(app, pos=(1.5, 0.15, 0), scale=(0.1, 0.1, 50), color=(0.7, 0.7, 0.7)))
        
        for i in range(50):
            z_pos = (i - 25) * 1.5
            if abs(z_pos) > 5.5: 
                add(ColorCube(app, pos=(0, 0.05, z_pos), scale=(2.2, 0.05, 0.3), color=(0.4, 0.25, 0.1)))

        add(ColorCube(app, pos=(7, 0.1, 7), scale=(1.5, 0.1, 1.5), color=(0.5, 0.5, 0.5)))    
        add(ColorCube(app, pos=(7, 0.6, 7), scale=(1.2, 0.4, 1.2), color=(0.8, 0.8, 0.7)))    
        add(ColorCube(app, pos=(7, 1.3, 7), scale=(1.1, 0.3, 1.1), color=(0.7, 0.9, 1.0)))    
        add(ColorCube(app, pos=(7, 1.7, 7), scale=(1.4, 0.15, 1.4), color=(0.6, 0.2, 0.2)))   
        add(ColorCube(app, pos=(7, 2.2, 7), scale=(0.02, 0.5, 0.02), color=(0.1, 0.1, 0.1)))

        # ==========================================
        # 2. DEKORASI LINGKUNGAN
        # ==========================================
        for x_pos in range(-40, 41, 15):
            if abs(x_pos) > 5: 
                add(ColorCube(app, pos=(x_pos, 2.0, -6.5), scale=(0.1, 2.0, 0.1), color=(0.3, 0.3, 0.3)))
                add(ColorCube(app, pos=(x_pos, 3.9, -5.8), scale=(0.08, 0.08, 0.8), color=(0.3, 0.3, 0.3)))
                add(ColorCube(app, pos=(x_pos, 3.8, -5.2), scale=(0.2, 0.1, 0.2), color=(1.0, 1.0, 0.6)))

        tree_positions = [
            (-15, -15), (-25, -10), (-35, -20), (-12, -30), (-45, -15), (-30, -35),
            (15, -15),  (25, -10),  (35, -20),  (12, -30),  (45, -15),  (30, -35),
            (-15, 15),  (-25, 10),  (-35, 20),  (-12, 30),  (-45, 15),  (-30, 35),
            (15, 15),   (25, 10),   (35, 20),   (12, 30),   (45, 15),   (30, 35)
        ]
        
        for tx, tz in tree_positions:
            tree_type = random.choice(['normal', 'pine'])
            scale_y = random.uniform(0.8, 1.5)
            add(ColorCube(app, pos=(tx, 0.5 * scale_y, tz), scale=(0.3, 0.8 * scale_y, 0.3), color=(0.4, 0.2, 0.1)))
            if tree_type == 'normal':
                add(ColorCube(app, pos=(tx, 1.5 * scale_y, tz), scale=(1.2, 1.0 * scale_y, 1.2), color=(0.15, 0.55, 0.2)))
                add(ColorCube(app, pos=(tx, 2.2 * scale_y, tz), scale=(0.8, 0.6 * scale_y, 0.8), color=(0.2, 0.6, 0.25)))
            else:
                add(ColorCube(app, pos=(tx, 1.2 * scale_y, tz), scale=(1.4, 0.5 * scale_y, 1.4), color=(0.1, 0.45, 0.15)))
                add(ColorCube(app, pos=(tx, 1.8 * scale_y, tz), scale=(1.0, 0.5 * scale_y, 1.0), color=(0.1, 0.45, 0.15)))
                add(ColorCube(app, pos=(tx, 2.4 * scale_y, tz), scale=(0.6, 0.5 * scale_y, 0.6), color=(0.1, 0.45, 0.15)))

        cloud_positions = [
            (-20, 15, -30), (20, 16, -25), (0, 14, -40),
            (-30, 17, 20), (30, 15, 25), (10, 16, 35)
        ]
        for cx, cy, cz in cloud_positions:
            add(ColorCube(app, pos=(cx, cy, cz), scale=(3.0, 0.5, 2.0), color=(1.0, 1.0, 1.0)))
            add(ColorCube(app, pos=(cx+1.5, cy+0.3, cz+0.5), scale=(2.0, 0.6, 1.5), color=(0.95, 0.95, 0.95)))
            add(ColorCube(app, pos=(cx-1.0, cy+0.2, cz-0.5), scale=(2.5, 0.4, 1.8), color=(1.0, 1.0, 1.0)))

        # ==========================================
        # 3. KERETA API (THOMAS THE TANK ENGINE & CARRIAGES)
        # ==========================================
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
        for g in range(1, 5): # Thomas identik dengan 2 gerbong
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

        # --- RODA KERETA ---
        all_units_z = [0] + [i * 6.5 for i in range(1, 5)]
        for i, base_z in enumerate(all_units_z):
            w_color = color_black 
            for side in [-1, 1]:
                for f_b in [-1.2, 0, 1.2]: # 6 Roda per unit
                    total_z = base_z + f_b
                    wheel = ColorCube(app, pos=(side * 1.5, y_wheel, self.train_z + total_z), scale=(0.12, 0.25, 0.25), color=w_color)
                    wheel.relative_offset = glm.vec3(side * 1.5, 0, total_z)
                    self.train_wheels.append((wheel, total_z))
                    add(wheel)

        # ==========================================
        # 4. PALANG PINTU
        # ==========================================
        self.gates = []
        self.signal_lights = []

        # Utara
        add(ColorCube(app, pos=(-7, 0.65, -5.5), scale=(0.15, 0.8, 0.15), color=(0.2, 0.2, 0.2)))
        add(ColorCube(app, pos=(-7, 2.2, -5.5), scale=(0.8, 0.1, 0.15), rot=(0, 0, 45), color=(0.9, 0.9, 0.9)))
        add(ColorCube(app, pos=(-7, 2.2, -5.5), scale=(0.8, 0.1, 0.15), rot=(0, 0, -45), color=(0.9, 0.9, 0.9)))
        gate_n = ColorCube(app, pos=(-7, 1.35, -5.5), scale=(0.05, 0.05, 4.5), color=(0.8, 0.1, 0.1))
        gate_n.pivot_offset = glm.vec3(0, 0, 4.5)
        self.gates.append(gate_n)
        add(gate_n)
        light_n = ColorCube(app, pos=(-7, 1.7, -5.5), scale=(0.15, 0.15, 0.15), color=(0.4, 0, 0))
        self.signal_lights.append(light_n)
        add(light_n)

        # Selatan
        add(ColorCube(app, pos=(7, 0.65, 5.5), scale=(0.15, 0.8, 0.15), color=(0.2, 0.2, 0.2)))
        add(ColorCube(app, pos=(7, 2.2, 5.5), scale=(0.8, 0.1, 0.15), rot=(0, 0, 45), color=(0.9, 0.9, 0.9)))
        add(ColorCube(app, pos=(7, 2.2, 5.5), scale=(0.8, 0.1, 0.15), rot=(0, 0, -45), color=(0.9, 0.9, 0.9)))
        gate_s = ColorCube(app, pos=(7, 1.35, 5.5), scale=(0.05, 0.05, 4.5), color=(0.8, 0.1, 0.1))
        gate_s.pivot_offset = glm.vec3(0, 0, -4.5)
        self.gates.append(gate_s)
        add(gate_s)
        light_s = ColorCube(app, pos=(7, 1.7, 5.5), scale=(0.15, 0.15, 0.15), color=(0.4, 0, 0))
        self.signal_lights.append(light_s)
        add(light_s)

        # ==========================================
        # 5. OBJECT POOL KENDARAAN
        # ==========================================
        for _ in range(self.max_pool):
            color = (random.random(), random.random(), random.random())
            car = Vehicle(app, color=color)
            self.vehicles_pool.append(car)
            add(car)

        self._spawn_vehicle(1) 
        self._spawn_vehicle(-1)

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
                car.pos.y = 0.5
                car.pos.z = 2.0 if direction == 1 else -2.0
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
        GATE_X_R = -7.0 
        GATE_X_L = 7.0  
        
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

        # --- FSM PALANG & KERETA ---
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
            # Arah Terbalik: Nilai minus menuju Z-
            self.train_z -= self.train_speed * dt
            if self.train_z < self.TRAIN_END_Z:
                self.state = 'OPENING'

        elif self.state == 'OPENING':
            self.gate_angle += self.gate_speed * dt
            if self.gate_angle >= 90.0:
                self.gate_angle = 90.0
                self.state = 'IDLE'

        # --- UPDATE MATRIX KERETA ---
        for part in self.train_parts:
            part.pos.z = self.train_z + part.relative_offset.z
            part.m_model = part.get_model_matrix()

        # Update Rotasi Roda Mundur
        wheel_rot_angle = -self.train_z * 2.0
        for wheel, total_z in self.train_wheels:
            wheel.pos = glm.vec3(wheel.relative_offset.x, 0.4, self.train_z + total_z)
            wheel.rot.x = wheel_rot_angle
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