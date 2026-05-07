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
        self.orig_speed = 7.0
        self.current_speed = 0.0
        self.wheel_rot = 0.0
        self.active = False
        self.safe_distance = 3.5
        self.length = 2.0 # Panjang total mobil (X-axis)
        
        # Atribut Fisika Pengereman
        self.deceleration = 10.0 # Kekuatan rem
        self.accel_rate = 8.0    # Kekuatan gas
        
        # Geometri Komposit (Orientasi X)
        # Body: Panjang di sumbu X
        self.body = ColorCube(app, color=color, scale=(1.0, 0.25, 0.5))
        self.cabin = ColorCube(app, color=color, scale=(0.5, 0.2, 0.4))
        self.wheels = [
            ColorCube(app, color=(0.1, 0.1, 0.1), scale=(0.15, 0.15, 0.15)) for _ in range(4)
        ]
        self.parts = [self.body, self.cabin] + self.wheels

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

        # 0. ALAS UTAMA
        add(ColorCube(app, pos=(0, -0.25, 0), scale=(50, 0.1, 50), color=(0.4, 0.5, 0.4)))

        # 1. LINGKUNGAN (X-axis Road, Z-axis Rails)
        # Aspal Jalan Raya (Sumbu X)
        add(ColorCube(app, pos=(0, -0.1, 0), scale=(50, 0.05, 5), color=(0.15, 0.15, 0.15)))
        
        # Marka Jalan Putus-Putus (Sumbu X)
        for x_pos in range(-48, 52, 4):
            add(ColorCube(app, pos=(x_pos, -0.04, 0), scale=(0.5, 0.01, 0.1), color=(1.0, 1.0, 1.0)))

        # Rel Kereta (Sumbu Z)
        add(ColorCube(app, pos=(-1.5, 0.15, 0), scale=(0.1, 0.1, 50), color=(0.5, 0.5, 0.5)))
        add(ColorCube(app, pos=(1.5, 0.15, 0), scale=(0.1, 0.1, 50), color=(0.5, 0.5, 0.5)))
        
        # Bantalan Rel (Sumbu Z)
        for i in range(34):
            z_pos = (i - 17) * 1.5
            add(ColorCube(app, pos=(0, 0.05, z_pos), scale=(2, 0.05, 0.3), color=(0.3, 0.2, 0.1)))
        
        # Pos Penjaga
        add(ColorCube(app, pos=(6, 0.85, 6), scale=(1, 1, 1), color=(0.8, 0.8, 0.7)))
        add(ColorCube(app, pos=(6, 1.45, 6), scale=(1.2, 0.1, 1.2), color=(0.6, 0.1, 0.1)))

        # 2. KERETA API (Expanded Locomotive + 2 Carriages with Wheels)
        self.train_parts = []
        self.train_wheels = []
        train_colors = [(0.2, 0.2, 0.6), (0.7, 0.7, 0.7), (0.7, 0.7, 0.7)]
        
        for i in range(3):
            z_offset = i * 8.0
            color = train_colors[i]
            
            # Body Gerbong
            t_body = ColorCube(app, pos=(0, 1.75, self.train_z - z_offset), scale=(1.8, 1.5, 3.5), color=color)
            t_accent = ColorCube(app, pos=(0, 0.6, self.train_z - z_offset), scale=(1.85, 0.2, 3.55), color=(0.1, 0.1, 0.1))
            self.train_parts.extend([t_body, t_accent])
            add(t_body); add(t_accent)
            
            # Wheels for Gerbong (4 per carriage)
            w_offsets = [glm.vec3(0.8, -0.4, 1.5), glm.vec3(-0.8, -0.4, 1.5), glm.vec3(0.8, -0.4, -1.5), glm.vec3(-0.8, -0.4, -1.5)]
            for off in w_offsets:
                w_pos = glm.vec3(0, 1.75, self.train_z - z_offset) + off # Placeholder pos
                wheel = ColorCube(app, pos=w_pos, scale=(0.3, 0.3, 0.3), color=(0.05, 0.05, 0.05))
                wheel.relative_offset = off + glm.vec3(0, -1.75 + 0.5, 0) # Offset from body center
                self.train_wheels.append((wheel, z_offset))
                add(wheel)

            if i == 0:
                t_cabin = ColorCube(app, pos=(0, 2.7, self.train_z - z_offset + 1.0), scale=(1.4, 0.5, 1.2), color=(0.15, 0.15, 0.3))
                self.train_parts.append(t_cabin)
                add(t_cabin)
    
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
        for part in self.train_parts:
            part.pos.z = self.train_z
            part.m_model = part.get_model_matrix()

        # Roda Kereta (Berputar Sinkron)
        wheel_rot_angle = self.train_z * 2.0
        for wheel, z_offset in self.train_wheels:
            wheel.pos = glm.vec3(0, 1.75, self.train_z - z_offset) + wheel.relative_offset
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
