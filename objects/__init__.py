from .trapezoid import draw_trapezoid
from .square import draw_square
from .parallelogram import draw_parallelogram
from .cone import draw_cone
from .prism import draw_prism
from .cylinder import draw_cylinder

shape_registry = {
    "trapezoid": draw_trapezoid,
    "square": draw_square,
    "parallelogram": draw_parallelogram,
    "cone": draw_cone,
    "prism": draw_prism,
    "cylinder": draw_cylinder
}
