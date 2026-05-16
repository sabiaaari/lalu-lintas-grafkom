import numpy as np


class VBO:
    def __init__(self, ctx):
        self.vbos = {
            'color_cube': ColorCubeVBO(ctx),
            'color_plane': ColorPlaneVBO(ctx),
            'color_pyramid': ColorPyramidVBO(ctx),
            'tex_cube': TexCubeVBO(ctx),
        }

    def destroy(self):
        for vbo in self.vbos.values():
            vbo.destroy()


class BaseVBO:
    format = None
    attribs = None

    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.ctx.buffer(self.get_vertex_data().astype('f4').tobytes())

    def get_vertex_data(self):
        raise NotImplementedError

    def destroy(self):
        self.vbo.release()


class ColorPlaneVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f 3f'
        self.attribs = ['in_normal', 'in_position']

    def get_vertex_data(self):
        positions = [
            (-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1)
        ]
        
        indices = [(0, 2, 1), (0, 3, 2)]
        normals = [(0, 1, 0)] * 6

        def get_data(verts, inds):
            return np.array([verts[i] for tri in inds for i in tri], dtype='f4')

        pos_data = get_data(positions, indices)
        norm_data = np.array(normals, dtype='f4')

        return np.hstack([norm_data, pos_data])


class ColorCubeVBO(BaseVBO):
    format = '3f 3f'
    attribs = ['in_normal', 'in_position']

    def get_vertex_data(self):
        vertices = np.array([
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
            (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1),
        ], dtype='f4')

        faces = [
            ((0, 2, 3), (0, 1, 2), (0, 0, 1)),
            ((1, 7, 2), (1, 6, 7), (1, 0, 0)),
            ((6, 5, 4), (4, 7, 6), (0, 0, -1)),
            ((3, 4, 5), (3, 5, 0), (-1, 0, 0)),
            ((3, 7, 4), (3, 2, 7), (0, 1, 0)),
            ((0, 6, 1), (0, 5, 6), (0, -1, 0)),
        ]

        data = []
        for tri_a, tri_b, normal in faces:
            for tri in (tri_a, tri_b):
                for idx in tri:
                    data.extend(normal)
                    data.extend(vertices[idx])
        return np.array(data, dtype='f4').reshape(-1, 6)

class ColorPyramidVBO(BaseVBO):
    format = '3f 3f'
    attribs = ['in_normal', 'in_position']

    def get_vertex_data(self):
        # Bentuk limas/piramida low-poly
        v0 = np.array([-1, -1,  1], dtype='f4')  # depan kiri bawah
        v1 = np.array([ 1, -1,  1], dtype='f4')  # depan kanan bawah
        v2 = np.array([ 1, -1, -1], dtype='f4')  # belakang kanan bawah
        v3 = np.array([-1, -1, -1], dtype='f4')  # belakang kiri bawah
        top = np.array([0, 1, 0], dtype='f4')    # pucuk

        faces = [
            (v0, v1, top),  # sisi depan
            (v1, v2, top),  # sisi kanan
            (v2, v3, top),  # sisi belakang
            (v3, v0, top),  # sisi kiri

            # alas bawah
            (v0, v2, v1),
            (v0, v3, v2),
        ]

        data = []

        for tri in faces:
            p0, p1, p2 = tri
            normal = np.cross(p1 - p0, p2 - p0)
            normal = normal / np.linalg.norm(normal)

            for p in tri:
                data.extend(normal)
                data.extend(p)

        return np.array(data, dtype='f4').reshape(-1, 6)

class TexCubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f 2f 3f'
        self.attribs = ['in_normal', 'in_texcoord_0', 'in_position']

    def get_vertex_data(self):
        vertices = np.array([
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
            (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1),
        ], dtype='f4')

        faces = [
            ((0, 2, 3), (0, 1, 2), (0, 0, 1)),
            ((1, 7, 2), (1, 6, 7), (1, 0, 0)),
            ((6, 5, 4), (4, 7, 6), (0, 0, -1)),
            ((3, 4, 5), (3, 5, 0), (-1, 0, 0)),
            ((3, 7, 4), (3, 2, 7), (0, 1, 0)),
            ((0, 6, 1), (0, 5, 6), (0, -1, 0)),
        ]

        tex_coords = [
            (0, 0), (1, 0), (1, 1), (0, 1)
        ]
        tex_indices = [
            (0, 2, 3), (0, 1, 2)
        ]

        data = []
        for tri_a, tri_b, normal in faces:
            for i, tri in enumerate((tri_a, tri_b)):
                for j, idx in enumerate(tri):
                    data.extend(normal)
                    data.extend(tex_coords[tex_indices[i][j]])
                    data.extend(vertices[idx])
        return np.array(data, dtype='f4').reshape(-1, 8)
