import math
from transformations.rotate import rotate_point_3d

def draw_cone(canvas, line_color, fill_color, scale, angle_x, angle_y, offset_x, offset_y):
    # Pastikan ukuran canvas mutakhir
    canvas.update_idletasks()
    center_x = canvas.winfo_width() // 2 + offset_x
    center_y = canvas.winfo_height() // 2 + offset_y

    # Titik puncak kerucut
    top = (0, -60, 0)

    # Titik-titik elips alas
    ellipse = [(30 * math.cos(math.radians(a)), 60, 30 * math.sin(math.radians(a))) for a in range(0, 360, 10)]

    # Gambar sisi-sisi kerucut
    for i in range(len(ellipse)):
        next_i = (i + 1) % len(ellipse)
        _draw_projected_polygon(canvas, [top, ellipse[i], ellipse[next_i]],
                                fill_color, line_color, scale, angle_x, angle_y, center_x, center_y)

    # Gambar alas kerucut
    _draw_projected_polygon(canvas, ellipse, "#bbbbbb", line_color, scale, angle_x, angle_y, center_x, center_y)

def _draw_projected_polygon(canvas, pts, fill_color, line_color, scale, ax, ay, cx, cy):
    projected = []
    for x, y, z in pts:
        x2, y2 = rotate_point_3d(x * scale, y * scale, z * scale, ax, ay)
        projected.append((cx + x2, cy + y2))
    canvas.create_polygon(projected, fill=fill_color, outline=line_color)
