import sys
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
        self.camera = Camera(self)
        self.mesh = Mesh(self)
        self.texture = Texture(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)

    def update_day_night(self):
        # SIKLUS JAM PASIR: Berubah setiap 20 detik (Total siklus 40 detik)
        # 0-20 detik: Siang (dengan transisi di akhir)
        # 20-40 detik: Malam (dengan transisi di akhir)
        cycle_duration = 20.0
        total_cycle = cycle_duration * 2
        current_cycle_time = self.time % total_cycle
        
        transition_dur = 4.0 # Durasi transisi halus selama 4 detik
        
        day_bg = glm.vec3(0.55, 0.78, 0.95)
        night_bg = glm.vec3(0.02, 0.02, 0.05)
        day_light_col = glm.vec3(1.0, 0.96, 0.86)
        night_light_col = glm.vec3(0.3, 0.3, 0.5)
        
        if 0.0 <= current_cycle_time < cycle_duration - transition_dur:
            # SIANG PENUH
            factor = 0.0
        elif cycle_duration - transition_dur <= current_cycle_time < cycle_duration:
            # TRANSISI SIANG -> MALAM
            factor = (current_cycle_time - (cycle_duration - transition_dur)) / transition_dur
        elif cycle_duration <= current_cycle_time < total_cycle - transition_dur:
            # MALAM PENUH
            factor = 1.0
        else:
            # TRANSISI MALAM -> SIANG
            factor = 1.0 - (current_cycle_time - (total_cycle - transition_dur)) / transition_dur
            
        # Update warna dan intensitas
        self.background_color = glm.lerp(day_bg, night_bg, factor)
        intensity = glm.lerp(1.35, 0.15, factor)
        light_color = glm.lerp(day_light_col, night_light_col, factor)
        
        # Update sim_time untuk sinkronisasi lampu di scene.py
        # Kita set sim_time agar sesuai dengan logika: >17 atau <7 adalah malam
        # Jika factor > 0.5 (mendekati malam), kita set ke jam 0 (tengah malam)
        # Jika factor <= 0.5 (mendekati siang), kita set ke jam 12 (siang hari)
        self.sim_time = 0.0 if factor > 0.5 else 12.0
        
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
