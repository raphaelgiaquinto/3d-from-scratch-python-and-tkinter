import numpy as np
import math
class Transform3D:

    @staticmethod
    def translate(origin, pos):
        x, y, z = pos
        mat = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [x, y, z, 1.0]
        ])
        return np.dot(origin, mat)

    @staticmethod
    def rotate_x(origin, angle):
        mat = np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, math.cos(angle), math.sin(angle), 0.0],
            [0.0, -math.sin(angle), math.cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ])
        return np.dot(origin, mat)
    
    @staticmethod
    def rotate_y(origin, angle):
        mat = np.array([
            [math.cos(angle), 0.0, -math.sin(angle), 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [math.sin(angle), 0.0, math.cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        return np.dot(origin, mat)

    @staticmethod
    def rotate_z(origin, angle):
        mat =  np.array([
            [math.cos(angle), math.sin(angle), 0.0, 0.0],
            [-math.sin(angle), math.cos(angle), 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        return np.dot(origin, mat)

    @staticmethod
    def scale(origin, s):
        mat = np.array([
            [s, 0.0, 0.0, 0.0],
            [0.0, s, 0.0, 0.0],
            [0.0, 0.0, s, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
        return np.dot(origin, mat)

class Camera3D:

    def __init__(self, position, screenWidth, screenHeight):
        self.screenWidth = screenWidth
        self.screenHeight = screenWidth
        self.half_w = screenWidth / 2
        self.half_h = screenHeight / 2
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0.0, 0.0, 1.0])
        self.up = np.array([0.0, 1.0, 0.0])
        self.right = np.array([1.0, 0.0, 0.0])
        self.horizontal_fov = math.pi / 3
        self.vertical_fov = self.horizontal_fov * (screenWidth / screenHeight)
        self.z_near = 0.0
        self.z_far = 100.0
    
    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, 0.0],
            [-x ,-y, -z, 1.0]
        ])

    def rotate_matrix(self):
        rx, ry, rz = self.right
        fx, fy, fz = self.forward
        ux, uy, uz = self.up
        return np.array([
            [rx, ux, fx, 0.0],
            [ry, uy, fy, 0.0],
            [rz, uz, fz, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    
    def camera_matrix(self):
        return np.dot(self.translate_matrix(), self.rotate_matrix())

    def projection_matrix(self):
        near = self.z_near
        far = self.z_far
        right = math.tan(self.horizontal_fov / 2)
        left = -right 
        top = math.tan(self.vertical_fov / 2)
        bottom = -top
        return np.array([
            [2 / (right - left), 0.0, 0.0, 0.0],
            [0.0, 2 / (top - bottom), 0.0, 0.0],
            [0.0, 0.0, (far + near) / (far - near), 1.0],
            [0.0, 0.0, -2 * near * (far / (far - near)), 0.0]
        ])

    def screen_projection(self, vertices):
        projected = np.dot(vertices, self.camera_matrix())
        projected = np.dot(projected, self.projection_matrix())
        projected /= projected[:, -1].reshape(-1, 1)
        return projected

    def screen_render(self, vertices):
        screen_matrix = np.array([
            [self.half_w, 0.0, 0.0, 0.0],
            [0.0, -self.half_h, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [self.half_w, self.half_h, 0.0, 1.0]
        ])
        rendered = np.dot(vertices, screen_matrix)
        rendered = rendered[:, :2]
        return rendered

    def translate_forward(self):
        self.position = Transform3D.translate(self.position, [0.0, 0.0, 0.1])

    def translate_backward(self):
        self.position = Transform3D.translate(self.position, [0.0, 0.0, -0.1])

    def translate_left(self):
        self.position = Transform3D.translate(self.position, [-0.1, 0.0, 0.0])

    def translate_right(self):
        self.position = Transform3D.translate(self.position, [0.1, 0.0, 0.0])

    def translate_up(self):
        self.position = Transform3D.translate(self.position, [0.0, 0.1, 0.0])

    def translate_down(self):
        self.position = Transform3D.translate(self.position, [0.0, -0.1, 0.0])


class Shape3D:
    def __init__(self):
        self.vertices = None
        self.edges = None

    def translate(self, pos):
        self.vertices = Transform3D.translate(self.vertices, pos)
    
    def rotate_x(self, angle):
        self.vertices = Transform3D.rotate_x(self.vertices, math.radians(angle))

    def rotate_y(self, angle):
        self.vertices = Transform3D.rotate_y(self.vertices, math.radians(angle))

    def rotate_z(self, angle):
        self.vertices = Transform3D.rotate_z(self.vertices, math.radians(angle))

class Cube3D(Shape3D):
    def __init__(self, vertices=None, edges=None):
        self.vertices = np.array([
            [0, 0, 0, 1],
            [0, 1, 0, 1],
            [1, 1, 0, 1],
            [1, 0, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 0, 1, 1]
        ]) if vertices == None else vertices

        self.edges = [
            [0, 1],
            [1, 2],
            [2, 3],
            [3, 0],
            [4, 5],
            [5, 6],
            [6, 7],
            [7, 4],
            [1, 5],
            [0, 4],
            [2, 6],
            [3, 7]
        ] if edges == None else edges


class Triangle3D(Shape3D):

    def __init__(self, vertices=None, edges=None):
        self.vertices = np.array([
            [-1, 0, 0, 1],
            [0, 1, 0, 1],
            [1, 0, 0, 1],
            [0, 0.5, 1, 1]
        ]) if vertices == None else vertices
        self.edges = [
            [0, 1],
            [1, 2],
            [2, 0],
            [0, 3],
            [1, 3],
            [2, 3]
        ] if edges == None else edges

class Engine3D:
    
    def __init__(self, canvas):
        self.camera = Camera3D([0.0, 0.5, -30], int(canvas['width']), int(canvas['height']))
        self.shapes = []
        self.canvas = canvas

    def bind(self, 
            forward="z", 
            backward="s", 
            right="d", 
            left="q", 
            up="a", 
            down="e"):
        self.canvas.winfo_toplevel().bind(forward, lambda event: self.camera.translate_forward())
        self.canvas.winfo_toplevel().bind(backward, lambda event: self.camera.translate_backward())
        self.canvas.winfo_toplevel().bind(right, lambda event: self.camera.translate_right())
        self.canvas.winfo_toplevel().bind(left, lambda event: self.camera.translate_left())
        self.canvas.winfo_toplevel().bind(up, lambda event: self.camera.translate_up())
        self.canvas.winfo_toplevel().bind(down, lambda event: self.camera.translate_down())

    def run(self):
        self.render()

    def render(self):
        self.canvas.delete("all")
        for shape in self.shapes:
            shape.rotate_y(1)
            rendered_shape = self.camera.screen_render(self.camera.screen_projection(shape.vertices))
            for edge in shape.edges:
                a = rendered_shape[edge[0]]
                b = rendered_shape[edge[1]]
                self.canvas.create_line(a[0], a[1], b[0], b[1], fill="gray", width=2)
        self.canvas.after(16, self.render)