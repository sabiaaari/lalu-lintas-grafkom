class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.scene = app.scene

    def render(self):
        # Update light uniforms for all programs
        light = self.app.light
        for pg_name in ['default_color', 'textured']:
            program = self.app.mesh.vao.program.programs[pg_name]
            program['light.Ia'].write(light.Ia)
            program['light.Id'].write(light.Id)
            program['light.Is'].write(light.Is)
            program['light.position'].write(light.position)

        for obj in self.scene.objects:
            obj.render()

    def destroy(self):
        return None
