import math

def rotate_point_3d(x, y, z, angle_x_deg, angle_y_deg):
    ax = math.radians(angle_x_deg)
    ay = math.radians(angle_y_deg)

    # Rotate around X axis
    y2 = y * math.cos(ax) - z * math.sin(ax)
    z2 = y * math.sin(ax) + z * math.cos(ax)

    # Rotate around Y axis
    x3 = x * math.cos(ay) + z2 * math.sin(ay)
    z3 = -x * math.sin(ay) + z2 * math.cos(ay)

    return x3, y2
