def draw_parallelogram(canvas, fill_color, line_color, scale, offset_x, offset_y):
    canvas.update_idletasks()
    center_x = canvas.winfo_width() // 2 + offset_x
    center_y = canvas.winfo_height() // 2 + offset_y

    pts = [(-40, -40), (0, -40), (40, 40), (0, 40)]
    scaled_pts = [(center_x + x * scale, center_y + y * scale) for x, y in pts]
    canvas.create_polygon(scaled_pts, fill=fill_color, outline=line_color)