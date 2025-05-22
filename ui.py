import tkinter as tk
from tkinter import ttk, colorchooser
from objects.base_renderer import ShapeRenderer
from transformations.rotate import rotate_point_3d

class ShapeAppUI:
    def __init__(self, root):
        self.root = root
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
        self.is_rotating = False
        self.mouse_rotate_enabled = False

        self.renderer = ShapeRenderer(self)

        self._build_ui()
        self.draw_shape()

    def _build_ui(self):
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.grid(row=0, column=0)

        control_frame = tk.Frame(main_frame)
        control_frame.grid(row=0, column=1, padx=10, sticky="n")

        canvas_frame = tk.Frame(main_frame)
        canvas_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_frame, width=600, height=400, bg="white", cursor="hand2")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.start_interactive_drag)
        self.canvas.bind("<B1-Motion>", self.perform_interactive_drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_interactive_drag)

        self.object_frame = tk.LabelFrame(control_frame, text="OBJECT", padx=5, pady=5)
        self.object_frame.pack(pady=5, fill='x')

        object_2d_frame = tk.LabelFrame(self.object_frame, text="2D", padx=3, pady=3)
        object_2d_frame.pack(side="left", padx=2)
        object_3d_frame = tk.LabelFrame(self.object_frame, text="3D", padx=3, pady=3)
        object_3d_frame.pack(side="left", padx=2)

        ttk.Button(object_2d_frame, text="Persegi", command=lambda: self.set_shape("square")).pack(side="left", padx=2)
        ttk.Button(object_2d_frame, text="Jajargenjang", command=lambda: self.set_shape("parallelogram")).pack(side="left", padx=2)
        ttk.Button(object_2d_frame, text="Trapesium", command=lambda: self.set_shape("trapezoid")).pack(side="left", padx=2)

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

        bottom_frame = tk.Frame(self.root, pady=10)
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
        if self.is_rotating and self.shape in ["cone", "prism", "cylinder"]:
            self.angle_y = (self.angle_y + 2) % 360
            self.draw_shape()
            self.root.after(30, self.auto_rotate)

    def draw_shape(self):
        self.canvas.delete("all")
        self.renderer.render(self.shape, self.canvas, self.fill_color, self.line_color,
                             self.angle_x, self.angle_y, self.scale, self.offset_x, self.offset_y)

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