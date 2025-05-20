import tkinter as tk
from tkinter import ttk, colorchooser
import math

class ShapeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Transformasi Objek 2D & 3D")

        self.shape = "trapezoid"
        self.fill_color = "blue"
        self.line_color = "black"
        self.angle_x = 0
        self.angle_y = 0
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.shapes_list = []
        self.is_rotating = False
        self.play_button = None
        self.mouse_rotate_enabled = False

        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.grid(row=0, column=0)

        # Tambahkan control_frame sebelum digunakan
        control_frame = tk.Frame(main_frame)
        control_frame.grid(row=0, column=1, padx=10, sticky="n")

        # CANVAS TANPA SCROLLBAR
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(
            canvas_frame, width=600, height=400, bg="white", cursor="hand2"
        )
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.start_interactive_drag)
        self.canvas.bind("<B1-Motion>", self.perform_interactive_drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_interactive_drag)

        # OBJECT FRAME TANPA SCROLLBAR
        self.object_frame = tk.LabelFrame(control_frame, text="OBJECT", padx=5, pady=5)
        self.object_frame.pack(pady=5, fill='x')

        # Frame untuk 2D dan 3D, horizontal
        object_2d_frame = tk.LabelFrame(self.object_frame, text="2D", padx=3, pady=3)
        object_2d_frame.pack(side="left", padx=2)
        object_3d_frame = tk.LabelFrame(self.object_frame, text="3D", padx=3, pady=3)
        object_3d_frame.pack(side="left", padx=2)

        # Tombol 2D (horizontal)
        ttk.Button(object_2d_frame, text="Persegi", command=lambda: self.set_shape("square")).pack(side="left", padx=2)
        ttk.Button(object_2d_frame, text="Jajargenjang", command=lambda: self.set_shape("parallelogram")).pack(side="left", padx=2)
        ttk.Button(object_2d_frame, text="Trapesium", command=lambda: self.set_shape("trapezoid")).pack(side="left", padx=2)

        # Tombol 3D (horizontal)
        ttk.Button(object_3d_frame, text="Prisma Segitiga", command=lambda: self.set_shape("prism")).pack(side="left", padx=2)
        ttk.Button(object_3d_frame, text="Tabung", command=lambda: self.set_shape("cylinder")).pack(side="left", padx=2)
        ttk.Button(object_3d_frame, text="Kerucut", command=lambda: self.set_shape("cone")).pack(side="left", padx=2)

        self.play_button = ttk.Button(self.object_frame, text="PLAY", command=self.toggle_rotation)
        self.play_button.pack(fill='x', pady=(5,0))
        self.update_play_button()

        self.transform_frame = tk.LabelFrame(control_frame, text="TRANSLASI", padx=5, pady=5)
        self.transform_frame.pack(pady=5, fill='x')
        for label, dx, dy in [("↑", 0, -10), ("↓", 0, 10), ("←", -10, 0), ("→", 10, 0)]:
            ttk.Button(self.transform_frame, text=label, command=lambda dx=dx, dy=dy: self.translate(dx, dy)).pack(fill='x')

        self.scale_frame = tk.LabelFrame(control_frame, text="SKALA", padx=5, pady=5)
        self.scale_frame.pack(pady=5, fill='x')
        for percent in [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]:
            ttk.Button(self.scale_frame, text=f"{int(percent*100)}%", command=lambda s=percent: self.set_scale(s)).pack(fill='x')

        bottom_frame = tk.Frame(root, pady=10)
        bottom_frame.grid(row=1, column=0, columnspan=2)

        warna_frame = tk.LabelFrame(bottom_frame, text="WARNA", padx=5, pady=5)
        warna_frame.grid(row=0, column=0, padx=10)
        ttk.Button(warna_frame, text="Isi", command=self.choose_fill_color).pack(fill='x')
        ttk.Button(warna_frame, text="Garis", command=self.choose_line_color).pack(fill='x')

        rotasi_frame = tk.LabelFrame(bottom_frame, text="ROTASI", padx=5, pady=5)
        rotasi_frame.grid(row=0, column=1, padx=10)
        self.angle_entry = tk.Entry(rotasi_frame, width=5)
        self.angle_entry.insert(0, "0")
        self.angle_entry.pack(side="left")
        ttk.Button(rotasi_frame, text="Apply", command=self.rotate).pack(side="left")

        manage_frame = tk.LabelFrame(bottom_frame, text="MANAGE", padx=5, pady=5)
        manage_frame.grid(row=0, column=2, padx=10)
        ttk.Button(manage_frame, text="Duplicate", command=self.duplicate_shape).pack(fill='x')
        ttk.Button(manage_frame, text="Remove All", command=self.remove_all_shapes).pack(fill='x')
        ttk.Button(manage_frame, text="Keluar", command=self.root.quit).pack(fill='x')

        self.draw_shape()

    def set_shape(self, shape):
        self.shape = shape
        self.angle_x = 0
        self.angle_y = 0
        self.offset_x = 0
        self.offset_y = 0
        self.scale = 1.0
        self.update_play_button()
        self.draw_shape()

    def update_play_button(self):
        if self.shape in ["cone", "prism", "cylinder"]:
            self.play_button.state(["!disabled"])
        else:
            self.play_button.state(["disabled"])
            self.is_rotating = False

    def toggle_rotation(self):
        self.is_rotating = not self.is_rotating
        if self.is_rotating:
            self.auto_rotate()

    def auto_rotate(self):
        if self.is_rotating and self.shape in ["cone", "cube", "pyramid"]:
            self.angle_y = (self.angle_y + 2) % 360
            self.draw_shape()
            self.root.after(30, self.auto_rotate)

    def draw_shape(self):
        self.canvas.delete("all")
        self.shapes_list.clear()
        self.render_shape()

    def rotate_point_3d(self, x, y, z):
        rad_x = math.radians(self.angle_x)
        rad_y = math.radians(self.angle_y)
        cosx, sinx = math.cos(rad_x), math.sin(rad_x)
        cosy, siny = math.cos(rad_y), math.sin(rad_y)

        y2 = y * cosx - z * sinx
        z2 = y * sinx + z * cosx

        x2 = x * cosy - z2 * siny
        z3 = x * siny + z2 * cosy

        return x2, y2

    def render_shape(self):
        cx, cy = 300 + self.offset_x, 200 + self.offset_y

        if self.shape == "cone":
            # Kerucut
            top = (0, -60, 0)
            ellipse = [(30 * math.cos(math.radians(a)), 60, 30 * math.sin(math.radians(a))) for a in range(0, 360, 10)]
            for i in range(len(ellipse)):
                next_i = (i + 1) % len(ellipse)
                self.draw_projected([top, ellipse[i], ellipse[next_i]], cx, cy, fill=self.fill_color)
            self.draw_projected(ellipse, cx, cy, fill="#bbbbbb")
        elif self.shape == "prism":
            # Prisma segitiga
            a = 40
            t = 40
            front = [(-a, t, a), (a, t, a), (0, -t, a)]
            back = [(-a, t, -a), (a, t, -a), (0, -t, -a)]
            for i in range(3):
                self.draw_projected([front[i], front[(i+1)%3], back[(i+1)%3], back[i]], cx, cy, fill="#b4a7d6")
            self.draw_projected(front, cx, cy, fill=self.fill_color)
            self.draw_projected(back, cx, cy, fill="#bbbbbb")
        elif self.shape == "cylinder":
            # Tabung
            r = 30
            h = 80
            top_ellipse = [(r * math.cos(math.radians(a)), -h/2, r * math.sin(math.radians(a))) for a in range(0, 360, 10)]
            bottom_ellipse = [(r * math.cos(math.radians(a)), h/2, r * math.sin(math.radians(a))) for a in range(0, 360, 10)]
            for i in range(len(top_ellipse)):
                next_i = (i + 1) % len(top_ellipse)
                quad = [top_ellipse[i], top_ellipse[next_i], bottom_ellipse[next_i], bottom_ellipse[i]]
                self.draw_projected(quad, cx, cy, fill="#b4a7d6")
            self.draw_projected(top_ellipse, cx, cy, fill=self.fill_color)
            self.draw_projected(bottom_ellipse, cx, cy, fill="#bbbbbb")
        elif self.shape == "square":
            pts = [(-40, -40), (40, -40), (40, 40), (-40, 40)]
            self.draw_polygon(pts, cx, cy)
        elif self.shape == "parallelogram":
            pts = [(50, -30), (-30, -30), (-50, 30), (30, 30)]
            self.draw_polygon(pts, cx, cy)
        elif self.shape == "trapezoid":
            flat_points = [(-20, -40), (20, -40), (40, 40), (-40, 40)]
            self.draw_polygon(flat_points, cx, cy)

    def draw_projected(self, pts, cx, cy, fill=None):
        projected = []
        for x, y, z in pts:
            x2, y2 = self.rotate_point_3d(x * self.scale, y * self.scale, z * self.scale)
            projected.append((cx + x2, cy + y2))
        self.canvas.create_polygon(projected, fill=fill if fill is not None else self.fill_color, outline=self.line_color)

    def draw_polygon(self, pts, cx, cy):
        final_points = [(cx + x * self.scale, cy + y * self.scale) for x, y in pts]
        self.canvas.create_polygon(final_points, fill=self.fill_color, outline=self.line_color)

    def translate(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy
        self.draw_shape()

    def set_scale(self, s):
        self.scale = s
        self.draw_shape()

    def rotate(self):
        try:
            self.angle_y = float(self.angle_entry.get())
        except ValueError:
            self.angle_y = 0
        self.draw_shape()

    def choose_fill_color(self):
        color = colorchooser.askcolor(title="Pilih Warna Isi")
        if color[1]:
            self.fill_color = color[1]
            self.draw_shape()

    def choose_line_color(self):
        color = colorchooser.askcolor(title="Pilih Warna Garis")
        if color[1]:
            self.line_color = color[1]
            self.draw_shape()

    def duplicate_shape(self):
        self.offset_x += 50
        self.draw_shape()

    def remove_all_shapes(self):
        self.canvas.delete("all")
        self.shapes_list.clear()

    def start_interactive_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.mouse_rotate_enabled = self.shape in ["cone", "prism", "cylinder"]

    def perform_interactive_drag(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        if self.mouse_rotate_enabled:
            self.angle_y += dx * 0.5
            self.angle_x += dy * 0.5
        else:
            self.offset_x += dx
            self.offset_y += dy
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.draw_shape()

    def end_interactive_drag(self, event):
        self.mouse_rotate_enabled = False

if __name__ == '__main__':
    root = tk.Tk()
    app = ShapeApp(root)
    root.mainloop()