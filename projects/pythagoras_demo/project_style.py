"""
项目专属视觉装置（pythagoras_demo）：勾股定理拼图证明的公共几何。

两幕共用同一批数字与顶点，保证「同一个大正方形」在两幕里像素级一致。
"""
import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, Line, Polygon, VGroup

A_LEG = 1.10          # 直角边 a
B_LEG = 1.50          # 直角边 b
SIDE = A_LEG + B_LEG  # 大正方形边长 a + b

UNIT_ORIGIN = np.array([-4.45, -0.55, 0.0])    # 第一幕左侧的样板三角形
ASSEMBLY_ORIGIN = np.array([1.15, -0.95, 0.0])  # 第一幕右侧：斜放 c² 的拼法
CENTER_ORIGIN = np.array([-1.30, -1.00, 0.0])   # 第二幕居中：露出 a² 与 b² 的拼法


def at(origin, x, y):
    """把局部坐标（以大正方形左下角为原点）换算成场景坐标。"""
    return origin + np.array([float(x), float(y), 0.0])


def unit_triangle(scene, origin):
    """样板直角三角形：直角在左下角，两条直角边 a（横）、b（竖），斜边 c。"""
    triangle = Polygon(
        at(origin, 0, 0), at(origin, A_LEG, 0), at(origin, 0, B_LEG),
        color=scene.theme.text_muted, fill_opacity=0.85, stroke_width=2,
    )
    return triangle


def unit_labels(scene, origin):
    """a / b / c 三边标注。"""
    lab_a = scene.make_math("a", font_size=32, color=scene.theme.primary)
    lab_a.next_to(Line(at(origin, 0, 0), at(origin, A_LEG, 0)), DOWN, buff=0.14)
    lab_b = scene.make_math("b", font_size=32, color=scene.theme.secondary)
    lab_b.next_to(Line(at(origin, 0, 0), at(origin, 0, B_LEG)), LEFT, buff=0.16)
    hyp_mid = at(origin, A_LEG / 2, B_LEG / 2)
    unit = np.array([B_LEG, A_LEG, 0.0]) / np.hypot(A_LEG, B_LEG)
    lab_c = scene.make_math("c", font_size=32, color=scene.theme.accent)
    lab_c.move_to(hyp_mid + unit * 0.3)
    return lab_a, lab_b, lab_c


def assembly_triangles(scene):
    """
    第一幕拼法：四个三角形首尾相接，中间空出一个边长 c 的倾斜正方形。
      大正方形四角为 (0,0) (S,0) (S,S) (0,S)，
      各边上的分点为 (a,0) (S,a) (b,S) (0,b)。
    """
    origin = ASSEMBLY_ORIGIN
    quads = [
        [(0, 0), (A_LEG, 0), (0, B_LEG)],
        [(A_LEG, 0), (SIDE, 0), (SIDE, A_LEG)],
        [(SIDE, A_LEG), (SIDE, SIDE), (B_LEG, SIDE)],
        [(B_LEG, SIDE), (0, SIDE), (0, B_LEG)],
    ]
    return VGroup(*[
        Polygon(*[at(origin, x, y) for x, y in points],
                color=scene.theme.text_muted, fill_opacity=0.85, stroke_width=2)
        for points in quads
    ])


def inner_square(scene):
    """第一幕中间空出来的 c² 区域。"""
    origin = ASSEMBLY_ORIGIN
    return Polygon(
        at(origin, A_LEG, 0), at(origin, SIDE, A_LEG),
        at(origin, B_LEG, SIDE), at(origin, 0, B_LEG),
        color=scene.theme.accent, fill_opacity=0.30, stroke_width=3,
    )


def rearranged_triangles(scene):
    """
    第二幕拼法：同样四个三角形挪到左下、右上之外的矩形里，
    空出左下角 a² 与右上角 b² 两个正方形。
    """
    origin = CENTER_ORIGIN
    quads = [
        [(A_LEG, 0), (SIDE, 0), (SIDE, A_LEG)],
        [(A_LEG, 0), (SIDE, A_LEG), (A_LEG, A_LEG)],
        [(0, A_LEG), (A_LEG, A_LEG), (A_LEG, SIDE)],
        [(0, A_LEG), (A_LEG, SIDE), (0, SIDE)],
    ]
    return VGroup(*[
        Polygon(*[at(origin, x, y) for x, y in points],
                color=scene.theme.text_muted, fill_opacity=0.85, stroke_width=2)
        for points in quads
    ])


def big_square(scene):
    origin = CENTER_ORIGIN
    return Polygon(
        at(origin, 0, 0), at(origin, SIDE, 0), at(origin, SIDE, SIDE), at(origin, 0, SIDE),
        color=scene.theme.text_main, fill_opacity=0, stroke_width=2.5,
    )


def square_a(scene):
    origin = CENTER_ORIGIN
    return Polygon(
        at(origin, 0, 0), at(origin, A_LEG, 0), at(origin, A_LEG, A_LEG), at(origin, 0, A_LEG),
        color=scene.theme.primary, fill_opacity=0.30, stroke_width=2.5,
    )


def square_b(scene):
    origin = CENTER_ORIGIN
    return Polygon(
        at(origin, A_LEG, A_LEG), at(origin, SIDE, A_LEG),
        at(origin, SIDE, SIDE), at(origin, A_LEG, SIDE),
        color=scene.theme.secondary, fill_opacity=0.30, stroke_width=2.5,
    )


def center_at(mobject, x=0.0, y=0.45):
    """把整组图形挪到指定屏幕位置（第二幕用）。"""
    return mobject.move_to(np.array([x, y, 0.0]))


def side_labels(scene):
    """第二幕底边的 a 与 b 分段标注。"""
    origin = CENTER_ORIGIN
    lab_a = scene.make_math("a", font_size=30, color=scene.theme.primary)
    lab_a.next_to(Line(at(origin, 0, 0), at(origin, A_LEG, 0)), DOWN, buff=0.16)
    lab_b = scene.make_math("b", font_size=30, color=scene.theme.secondary)
    lab_b.next_to(Line(at(origin, A_LEG, 0), at(origin, SIDE, 0)), DOWN, buff=0.16)
    return VGroup(lab_a, lab_b)
