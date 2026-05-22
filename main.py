import sys
import math
import numpy as np
import pygame as pg
import moderngl as mgl
from pyglm import glm

from camera import Camera
from point_light import PointLight
from mesh import Mesh
from texture import Texture
from scene import Scene
from scene_renderer import SceneRenderer


class SxvxnEngine:
    def __init__(self, win_size=(1280, 720)):
        pg.init()
        pg.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pg.display.set_caption("Modern GL Basics - Railway Crossing")
        self.WIN_SIZE = win_size

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.ctx = mgl.create_context(require=330)
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.time = 0.0
        self.delta_time = 0.0
        
        # --- SISTEM WAKTU (DAY-NIGHT CYCLE) ---
        self.sim_time = 12.0 # Mulai di jam 12 siang
        self.time_speed = 0.5 # Kecepatan siklus (1 jam simulasi = 2 detik real time jika 0.5)
        self.background_color = (0.55, 0.78, 0.95)

        self.light = PointLight(position=(-8.0, 12.0, 10.0), color=(1.0, 0.96, 0.86), intensity=1.35)
        
        # Audio
        self.sounds = self.create_synth_sounds()
        
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.texture = Texture(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)

    def create_synth_sounds(self):
        sample_rate = 22050
        
        def make_sound(arr):
            # Convert to 16-bit signed integer
            arr = (arr * 32767).astype(np.int16)
            # Make stereo
            stereo = np.zeros((arr.size, 2), dtype=np.int16)
            stereo[:, 0] = arr
            stereo[:, 1] = arr
            return pg.sndarray.make_sound(stereo)

        # 1. Bell Sound (Ding)
        duration = 0.5
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        bell = np.sin(2 * np.pi * 880 * t) * np.exp(-5 * t)
        
        # 2. Train Whistle (Tuuuut)
        duration_whistle = 1.5
        t_w = np.linspace(0, duration_whistle, int(sample_rate * duration_whistle), False)
        whistle = (np.sin(2 * np.pi * 330 * t_w) + 0.5 * np.sin(2 * np.pi * 440 * t_w)) * 0.4
        # Fade in/out
        fade = np.ones_like(t_w)
        fade[:1000] = np.linspace(0, 1, 1000)
        fade[-1000:] = np.linspace(1, 0, 1000)
        whistle *= fade

        # 3. Engine Chug (Rhythmic noise)
        duration_chug = 0.4
        t_c = np.linspace(0, duration_chug, int(sample_rate * duration_chug), False)
        noise = np.random.uniform(-1, 1, t_c.size)
        chug = noise * np.exp(-15 * t_c) * 0.3

        return {
            'bell': make_sound(bell),
            'whistle': make_sound(whistle),
            'chug': make_sound(chug)
        }

    def update_day_night(self):
        # Sesuai permintaan: 24 jam = 48 detik (1 jam = 2 detik)
        # 24 jam / 48 detik = 0.5 jam per detik real-time
        hours_per_second = 0.5
        self.sim_time = (self.sim_time + hours_per_second * self.delta_time * self.time_speed) % 24

        # --- LOGIKA VISUAL DAY-NIGHT ---
        # 0.0 = Tengah Malam, 12.0 = Siang Terik, 18.0 = Senja, 6.0 = Subuh
        # Mapping sim_time ke intensitas cahaya dan warna langit

        day_bg = glm.vec3(0.55, 0.78, 0.95)
        night_bg = glm.vec3(0.05, 0.08, 0.20)
        day_light_col = glm.vec3(1.0, 0.96, 0.86)
        night_light_col = glm.vec3(0.3, 0.3, 0.5)

        # Gunakan kurva cosinus untuk transisi yang sangat halus
        # Kita geser 12 jam agar puncaknya di jam 12 siang (cos(0) = 1)
        # sim_time 0 -> factor 1 (malam), sim_time 12 -> factor 0 (siang)
        # 15 derajat per jam (360/24)
        factor = 0.5 * (1.0 - math.cos(math.radians((self.sim_time) * 15))) # factor=0 di jam 0, factor=1 di jam 12
        # Kita balik agar factor=1 di malam hari
        night_factor = 1.0 - factor

        # Update warna dan intensitas
        self.background_color = glm.lerp(day_bg, night_bg, night_factor)
        intensity = glm.lerp(1.35, 0.15, night_factor)
        light_color = glm.lerp(day_light_col, night_light_col, night_factor)

        self.light.update_properties(light_color, intensity)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.destroy()
                pg.quit()
                sys.exit()

            # EVENT LISTENER: Tombol Enter untuk trigger perlintasan
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                self.scene.handle_input_enter()

            # EVENT LISTENER: Tombol Spasi untuk spawn kendaraan
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.scene.handle_input_space()

            # Tombol +/- untuk mengatur kecepatan waktu
            if event.type == pg.KEYDOWN and event.key == pg.K_EQUALS: # Plus key
                self.time_speed = min(10.0, self.time_speed + 0.5)
            if event.type == pg.KEYDOWN and event.key == pg.K_MINUS:
                self.time_speed = max(0.0, self.time_speed - 0.5)

            if event.type == pg.KEYDOWN and event.key == pg.K_TAB:
                self.camera.use_orbit = not self.camera.use_orbit
                self.camera.set_default()

            if event.type == pg.KEYDOWN and event.key == pg.K_BACKQUOTE:
                visible = not pg.mouse.get_visible()
                pg.mouse.set_visible(visible)
                pg.event.set_grab(not visible)

            if event.type == pg.MOUSEBUTTONDOWN and self.camera.use_orbit:
                if event.button == 4:
                    self.camera.orbit_radius = max(2.0, self.camera.orbit_radius - 0.5)
                elif event.button == 5:
                    self.camera.orbit_radius = min(40.0, self.camera.orbit_radius + 0.5)


    def render(self):
        self.ctx.clear(color=self.background_color)
        self.scene_renderer.render()
        pg.display.flip()

    def get_time(self): 
        self.time = pg.time.get_ticks() * 0.001

    def destroy(self):
        self.mesh.destroy()
        self.texture.destroy()
        self.scene_renderer.destroy()

    def run(self):
        while True:
            # Hitung delta_time dalam detik di awal frame
            self.delta_time = self.clock.tick(60) * 0.001
            self.get_time()
            self.check_events()
            self.camera.update()
            self.update_day_night()
            self.scene.update() # Update logika perlintasan & aktor
            self.render()


if __name__ == '__main__':
    app = SxvxnEngine()
    app.run()
