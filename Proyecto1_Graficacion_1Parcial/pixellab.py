import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import Image, ImageDraw

WIDTH, HEIGHT = 800, 600
SCALE = 4
GRID_W, GRID_H = WIDTH // SCALE, HEIGHT // SCALE

color_actual = "#000000"
last_x, last_y = None, None

# Imagen en memoria para guardar
img = Image.new("RGB", (WIDTH, HEIGHT), "white")
draw = ImageDraw.Draw(img)

def bresenham_line(x0, y0, x1, y1):
    puntos = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        puntos.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2*err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return puntos

def pintar(e):
    global last_x, last_y
    cx = e.x // SCALE
    cy = e.y // SCALE
    if last_x is not None:
        for px, py in bresenham_line(last_x, last_y, cx, cy):
            canvas.create_rectangle(px*SCALE, py*SCALE, (px+1)*SCALE, (py+1)*SCALE, fill=color_actual, outline="")
            draw.rectangle([px*SCALE, py*SCALE, (px+1)*SCALE, (py+1)*SCALE], fill=color_actual)
    else:
        canvas.create_rectangle(cx*SCALE, cy*SCALE, (cx+1)*SCALE, (cy+1)*SCALE, fill=color_actual, outline="")
        draw.rectangle([cx*SCALE, cy*SCALE, (cx+1)*SCALE, (cy+1)*SCALE], fill=color_actual)
    last_x, last_y = cx, cy

def soltar(e):
    global last_x, last_y
    last_x, last_y = None, None

def cambiar_color():
    global color_actual
    c = colorchooser.askcolor()[1]
    if c:
        color_actual = c
        btn_color.config(bg=c)

def guardar():
    ruta = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG","*.png"),("BMP","*.bmp")])
    if ruta:
        img.save(ruta)
        print(f"Guardado en {ruta}")

def guardar_bn():
    ruta = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP","*.bmp")])
    if ruta:
        img.convert("L").save(ruta)
        print(f"Guardado BN en {ruta}")

root = tk.Tk()
root.title("PixelLab Graficacion - 2415ICM001 - 24ISICM002")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()
canvas.bind("<B1-Motion>", pintar)
canvas.bind("<ButtonPress-1>", pintar)
canvas.bind("<ButtonRelease-1>", soltar)

frame = tk.Frame(root)
frame.pack(fill="x")
btn_color = tk.Button(frame, text="Cambiar Color RGB", command=cambiar_color, bg="black", fg="white", height=2)
btn_color.pack(side="left", expand=True, fill="x")
btn_guardar = tk.Button(frame, text="Guardar PNG/BMP", command=guardar, bg="green", fg="white", height=2)
btn_guardar.pack(side="left", expand=True, fill="x")
btn_bn = tk.Button(frame, text="Guardar en B/N", command=guardar_bn, bg="gray", fg="white", height=2)
btn_bn.pack(side="left", expand=True, fill="x")

root.mainloop()