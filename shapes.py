import math
from transformations import rotate_point_3d

class ShapeRenderer:
    def __init__(self, ui):
        self.ui = ui  # referensi ke UI jika perlu, misal untuk akses state

    def render(self, shape, canvas, fill_color, line_color, angle_x, angle_y, scale, offset_x, offset_y):
        cx, cy = 300 + offset_x, 200 + offset_y

        if shape == "cone":
            self._render_cone(canvas, cx, cy, fill_color, line_color, angle_x, angle_y, scale)
        elif shape == "prism":
            self._render_prism(canvas, cx, cy, fill_color, line_color, angle_x, angle_y, scale)
        elif shape == "cylinder":
            self._render_cylinder(canvas, cx, cy, fill_color, line_color, angle_x, angle_y, scale)
        elif shape == "square":
            pts = [(-40, -40), (40, -40), (40, 40), (-40, 40)]
            self._draw_polygon(canvas, pts, cx, cy, fill_color, line_color, scale)
        elif shape == "parallelogram":
            pts = [(50, -30), (-30, -30), (-50, 30), (30, 30)]
            self._draw_polygon(canvas, pts, cx, cy, fill_color, line_color, scale)
        elif shape == "trapezoid":
            pts = [(-20, -40), (20, -40), (40, 40), (-40, 40)]
            self._draw_polygon(canvas, pts, cx, cy, fill_color, line_color, scale)

    def _draw_polygon(self, canvas, pts, cx, cy, fill_color, line_color, scale):
        final_points = [(cx + x * scale, cy + y * scale) for x, y in pts]
        canvas.create_polygon(final_points, fill=fill_color, outline=line_color)

    def _draw_projected(self, canvas, pts, cx, cy, fill_color, line_color, angle_x, angle_y, scale):
        projected = []
        for x, y, z in pts:
            x2, y2 = rotate_point_3d(x * scale, y * scale, z * scale, angle_x, angle_y)
            projected.append((cx + x2, cy + y2))
        canvas.create_polygon(projected, fill=fill_color, outline=line_color)

    def _render_cone(self, canvas, cx, cy, fill_color, line_color, angle_x, angle_y, scale):
        top = (0, -60, 0)
        ellipse = [(30 * math.cos(math.radians(a)), 60, 30 * math.sin(math.radians(a))) for a in range(0, 360, 10)]
        for i in range(len(ellipse)):
            next_i = (i + 1) % len(ellipse)
            self._draw_projected(canvas, [top, ellipse[i], ellipse[next_i]], cx, cy, fill_color, line_color, angle_x, angle_y, scale)
        self._draw_projected(canvas, ellipse, cx, cy, "#bbbbbb", line_color, angle_x, angle_y, scale)

    def _render_prism(self, canvas, cx, cy, fill_color, line_color, angle_x, angle_y, scale):
        a = 40
        t = 40
        front = [(-a, t, a), (a, t, a), (0, -t, a)]
        back = [(-a, t, -a), (a, t, -a), (0, -t, -a)]
        for i in range(3):
            quad = [front[i], front[(i+1)%3], back[(i+1)%3], back[i]]
            self._draw_projected(canvas, quad, cx, cy, fill_color, line_color, angle_x, angle_y, scale)
        self._draw_projected(canvas, front, cx, cy, fill_color, line_color, angle_x, angle_y, scale)
        self._draw_projected(canvas, back, cx, cy, fill_color, line_color, angle_x, angle_y, scale)

    def _render_cylinder(self, canvas, cx, cy, fill_color, line_color, angle_x, angle_y, scale):
        top_circle = [(30 * math.cos(math.radians(a)), -40, 30 * math.sin(math.radians(a))) for a in range(0, 360, 10)]
        bottom_circle = [(30 * math.cos(math.radians(a)), 40, 30 * math.sin(math.radians(a))) for a in range(0, 360, 10)]
        for i in range(len(top_circle)):
            next_i = (i + 1) % len(top_circle)
            self._draw_projected(canvas, [top_circle[i], top_circle[next_i], bottom_circle[next_i], bottom_circle[i]], cx, cy, fill_color, line_color, angle_x, angle_y, scale)
        self._draw_projected(canvas, top_circle, cx, cy, "#bbbbbb", line_color, angle_x, angle_y, scale)
        self._draw_projected(canvas, bottom_circle, cx, cy, "#bbbbbb", line_color, angle_x, angle_y, scale)
