import math
from transformations.rotate import rotate_point_3d

def draw_cylinder(canvas, line_color, fill_color, scale, angle_x, angle_y, offset_x, offset_y):
    r = 30
    h = 120  # tinggi tabung (dari -60 ke +60)

    # Update ukuran canvas untuk dapatkan tengahnya
    canvas.update_idletasks()
    center_x = canvas.winfo_width() // 2 + offset_x
    center_y = canvas.winfo_height() // 2 + offset_y

    # Titik-titik untuk lingkaran atas (y = -h/2)
    top_circle = [(r * math.cos(math.radians(a)), -h/2, r * math.sin(math.radians(a))) for a in range(0, 360, 10)]
    # Titik-titik untuk lingkaran bawah (y = +h/2)
    bottom_circle = [(x, y + h, z) for x, y, z in top_circle]

    # Gambar sisi-sisi silinder
    for i in range(len(top_circle)):
        next_i = (i + 1) % len(top_circle)
        quad = [top_circle[i], top_circle[next_i], bottom_circle[next_i], bottom_circle[i]]
        _draw_projected_polygon(canvas, quad, "#b4a7d6", line_color, scale, angle_x, angle_y, center_x, center_y)

    # Gambar lingkaran atas (tutup atas) dan bawah (alas)
    _draw_projected_polygon(canvas, top_circle, fill_color, line_color, scale, angle_x, angle_y, center_x, center_y)
    _draw_projected_polygon(canvas, bottom_circle, "#bbbbbb", line_color, scale, angle_x, angle_y, center_x, center_y)

def _draw_projected_polygon(canvas, pts, fill_color, line_color, scale, ax, ay, cx, cy):
    projected = []
    for x, y, z in pts:
        rx, ry = rotate_point_3d(x * scale, y * scale, z * scale, ax, ay)
        projected.append((cx + rx, cy + ry))
    canvas.create_polygon(projected, fill=fill_color, outline=line_color)
