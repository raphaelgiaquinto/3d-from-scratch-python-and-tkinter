from engine3d import Engine3D, Cube3D, Triangle3D
from tkinter import Tk, Canvas
import random


screenW = 640
screenH = 640

root = Tk()
root.geometry(f"{screenW}x{screenH}")
root.resizable(False, False)
root.title("3D")

canvas = Canvas(root, width=screenW, height=screenH)
canvas.pack()

engine = Engine3D(canvas)

for i in range(50):
    engine.shapes.append(Cube3D())

for cube in engine.shapes:
    cube.translate([random.random()*10, random.random()*10, random.random()*10])


engine.bind()

engine.run()

root.mainloop()
