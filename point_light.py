from pyglm import glm

class PointLight:
    def __init__(self, position=(6, 15, 6), color=(1, 1, 1), intensity=1.2):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.intensity = intensity
        self.update_components()

    def update_light(self, intensity, color=(1, 1, 1)):
        # Fungsi ini dipanggil saat ganti suasana Siang/Malam
        self.color = glm.vec3(color)
        self.intensity = intensity
        self.update_components()
        
    def update_components(self):
        # Hitung ulang Ambient (Ia), Diffuse (Id), dan Specular (Is)
        self.Ia = 0.20 * self.color * self.intensity
        self.Id = 0.85 * self.color * self.intensity
        self.Is = 0.40 * self.color * self.intensity