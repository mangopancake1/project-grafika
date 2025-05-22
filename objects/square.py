def draw_square(canvas, fill_color, line_color, scale, offset_x, offset_y):
    canvas.update_idletasks()  # Pastikan ukuran terbaru
    cx = canvas.winfo_width() // 2 + offset_x
    cy = canvas.winfo_height() // 2 + offset_y

    half = 40
    pts = [(-half, -half), (half, -half), (half, half), (-half, half)]
    scaled_pts = [(cx + x * scale, cy + y * scale) for x, y in pts]

    canvas.create_polygon(scaled_pts, fill=fill_color, outline=line_color)
