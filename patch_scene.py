import re

with open('scene.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update GradeCrossingSignal class with strict hierarchy and matrices
new_crossing_class = """class GradeCrossingSignal:
    def __init__(self, scene, pos, rotation_y, gate_pivot_side):
        self.scene, self.app, self.pos = scene, scene.app, glm.vec3(pos)
        self.rotation_y, self.gate_pivot_side = rotation_y, gate_pivot_side
        self.parts, self.mast_lights, self.arm_lights = [], [], []        

        # -----------------------------------------------------------
        # HIERARKI VERTIKAL (SUMBU Y - DARI BAWAH KE ATAS)
        # -----------------------------------------------------------
        
        # 1. Bottom Level: Concrete Base (Pondasi abu-abu)
        self.base = ColorCube(self.app, pos=self.pos + glm.vec3(0, 0.05, 0), scale=(0.5, 0.05, 0.5), color=(0.5, 0.5, 0.5))
        self.parts.append(self.base)

        # 2. Main Mast (Tiang Utama silinder/kotak)
        # Mast base at 0.1, height 3.0. Center at 1.6
        self.mast = TexturedCube(self.app, pos=self.pos + glm.vec3(0, 1.6, 0), scale=(0.15, 1.5, 0.15), 
                                 texture_id=0, uv_offset=(0, 0), uv_scale=(1, 0.5))
        self.parts.append(self.mast)

        # 3. Mid Level: Gate Mechanism (Kotak engsel/Hinge box)
        # Offset ke samping tiang (kiri tiang dari POV traffic)
        # Mast radius 0.15 + Hinge half-width 0.25 = 0.4 offset
        hinge_offset_z = gate_pivot_side * 0.4
        self.hinge_pos = self.pos + glm.vec3(0, 1.2, hinge_offset_z)
        self.hinge_box = ColorCube(self.app, pos=self.hinge_pos, scale=(0.25, 0.25, 0.25), color=(0.1, 0.1, 0.1))
        self.parts.append(self.hinge_box)

        # 4. Lower Level: Barrier Arm (Lengan palang)
        # Pangkal menempel pada engsel, membentang ke tengah jalan
        self.gate_arm = TexturedCube(self.app, pos=self.hinge_pos + glm.vec3(0, -0.1, 0), scale=(0.1, 0.1, 9.0), 
                                    texture_id=0, uv_offset=(0, 0), uv_scale=(1, 0.5))
        # Pivot offset menggeser geometri agar ujungnya di hinge_pos
        self.gate_arm.pivot_offset = glm.vec3(0, 0, gate_pivot_side * 9.0)
        self.parts.append(self.gate_arm)

        # 3 Lampu Palang (Serial)
        for i in range(3):
            al = ColorCube(self.app, scale=(0.12, 0.12, 0.12), color=(0.4, 0, 0))
            self.arm_lights.append(al); self.parts.append(al)

        # 5. Upper Level: Crossbuck & Main Lights (Dirotasi 90 derajat ke jalan)
        cb_yaw = rotation_y + 90
        # Offset sedikit ke depan tiang agar tidak tumpang tindih
        offset_dir = glm.vec3(math.sin(glm.radians(rotation_y)), 0, math.cos(glm.radians(rotation_y)))
        
        # Tanda 'X' (Sangat Besar)
        cb_pos = self.pos + glm.vec3(0, 2.9, 0) + offset_dir * 0.22
        cb1 = TexturedCube(self.app, pos=cb_pos, scale=(1.5, 0.25, 0.05), rot=(0, cb_yaw, 45), 
                           texture_id=0, uv_offset=(0, 0.5), uv_scale=(1, 0.5)) 
        cb2 = TexturedCube(self.app, pos=cb_pos, scale=(1.5, 0.25, 0.05), rot=(0, cb_yaw, -45), 
                           texture_id=0, uv_offset=(0, 0.5), uv_scale=(1, 0.5))
        self.parts.extend([cb1, cb2])

        # Wadah Lampu Peringatan
        housing_pos = self.pos + glm.vec3(0, 2.6, 0) + offset_dir * 0.22
        housing = ColorCube(self.app, pos=housing_pos, scale=(1.0, 0.2, 0.1), rot=(0, cb_yaw, 0), color=(0.1, 0.1, 0.1))
        self.parts.append(housing)

        # Dua lingkaran merah (Lampu Utama)
        side_dir = glm.vec3(math.sin(glm.radians(cb_yaw)), 0, math.cos(glm.radians(cb_yaw)))
        for side in [-1, 1]:
            lp = housing_pos + side_dir * (side * 0.7) + offset_dir * 0.12
            l = ColorCube(self.app, pos=lp, scale=(0.35, 0.35, 0.05), rot=(0, cb_yaw, 0), color=(0.4, 0, 0))
            self.mast_lights.append(l); self.parts.append(l)

        # 6. Top Level: Bell Cap (Ujung paling atas)
        self.bell = ColorCube(self.app, pos=self.pos + glm.vec3(0, 3.25, 0), scale=(0.2, 0.1, 0.2), color=(0.4, 0.4, 0.4))
        self.parts.append(self.bell)

        for p in self.parts: scene.add_object(p)

    def update(self, gate_angle, emissive_val):
        angle_rad = glm.radians(gate_angle)
        
        # Animasi Lengan Palang
        self.gate_arm.rot.x = -angle_rad if self.gate_pivot_side > 0 else angle_rad
        self.gate_arm.m_model = self.gate_arm.get_model_matrix()

        # Update Posisi 3 Lampu Palang mengikuti rotasi engsel
        arm_model = self.gate_arm.m_model
        light_local_zs = [7.0, 0, -8.0] if self.gate_pivot_side > 0 else [-7.0, 0, 8.0]
        for i, lz in enumerate(light_local_zs):
            pos_w = arm_model * glm.vec4(0, 0.2, lz, 1.0)
            self.arm_lights[i].pos = glm.vec3(pos_w)
            self.arm_lights[i].rot.x = self.gate_arm.rot.x
            self.arm_lights[i].emissive = glm.vec3(emissive_val, 0, 0)    
            self.arm_lights[i].m_model = self.arm_lights[i].get_model_matrix()

        # Update Intensitas Cahaya Lampu Utama
        light_emissive = glm.vec3(emissive_val, 0.0, 0.0)
        for l in self.mast_lights: l.emissive = light_emissive
"""

content = re.sub(r'class GradeCrossingSignal:.*?class Scene:', new_crossing_class + '\nclass Scene:', content, flags=re.DOTALL)

with open('scene.py', 'w', encoding='utf-8') as f:
    f.write(content)
