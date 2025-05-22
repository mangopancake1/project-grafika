from transformations.rotate import rotate_point_3d

def draw_prism(canvas, fill_color, line_color, scale, angle_x, angle_y, offset_x, offset_y):
    a = 40  # panjang sisi alas
    t = 40  # tinggi segitiga

    # Update ukuran canvas
    canvas.update_idletasks()
    center_x = canvas.winfo_width() // 2 + offset_x
    center_y = canvas.winfo_height() // 2 + offset_y

    # Titik-titik segitiga depan dan belakang dalam koordinat 3D
    front = [(-a, t, a), (a, t, a), (0, -t, a)]
    back =  [(-a, t, -a), (a, t, -a), (0, -t, -a)]

    # Gambar sisi-sisi antara front dan back
    for i in range(3):
        quad = [front[i], front[(i + 1) % 3], back[(i + 1) % 3], back[i]]
        _draw_projected_polygon(canvas, quad, "#b4a7d6", line_color, scale, angle_x, angle_y, center_x, center_y)

    # Gambar muka depan dan belakang
    _draw_projected_polygon(canvas, front, fill_color, line_color, scale, angle_x, angle_y, center_x, center_y)
    _draw_projected_polygon(canvas, back, "#bbbbbb", line_color, scale, angle_x, angle_y, center_x, center_y)


def _draw_projected_polygon(canvas, pts, fill_color, line_color, scale, ax, ay, cx, cy):
    projected = []
    for x, y, z in pts:
        rx, ry = rotate_point_3d(x * scale, y * scale, z * scale, ax, ay)
        projected.append((cx + rx, cy + ry))
    canvas.create_polygon(projected, fill=fill_color, outline=line_color)
