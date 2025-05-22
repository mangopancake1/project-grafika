from objects.trapezoid import draw_trapezoid
from objects.square import draw_square
from objects.parallelogram import draw_parallelogram
from objects.prism import draw_prism
from objects.cone import draw_cone
from objects.cylinder import draw_cylinder

class ShapeRenderer:
    def __init__(self, app):
        self.app = app

    def render(self, shape, canvas, fill, outline, angle_x, angle_y, scale, offset_x=None, offset_y=None):
        # Pastikan canvas sudah terupdate ukurannya
        canvas.update_idletasks()
        cx = offset_x if offset_x is not None else canvas.winfo_width() // 2
        cy = offset_y if offset_y is not None else canvas.winfo_height() // 2

        if shape == "trapezoid":
            draw_trapezoid(canvas, fill, outline, scale, cx, cy)
        elif shape == "square":
            draw_square(canvas, fill, outline, scale, cx, cy)
        elif shape == "parallelogram":
            draw_parallelogram(canvas, fill, outline, scale, cx, cy)
        elif shape == "prism":
            draw_prism(canvas, fill, outline, scale, angle_x, angle_y, cx, cy)
        elif shape == "cone":
            draw_cone(canvas, fill, outline, scale, angle_x, angle_y, cx, cy)
        elif shape == "cylinder":
            draw_cylinder(canvas, fill, outline, scale, angle_x, angle_y, cx, cy)
