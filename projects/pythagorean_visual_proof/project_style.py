"""
项目专属视觉装置 —— 《勾股定理的可视化几何证明》

核心几何：一个大正方形 (边长 a+b) 内放四块全等直角三角形。
* 摆法一：四块三角形首尾相接，中央空出边长 c 的倾斜正方形（面积 c²）；
* 摆法二：四块三角形靠向左下 / 右上，空出边长 a 与 b 的两个正方形（面积 a²、b²）。

两幕共用下面的常量与构造器，保证「同一个大正方形」在两幕里像素级重合。
"""
import numpy as np
from manim import *  # noqa: F401,F403

# ==========================================
# 公共几何参数
# ==========================================
A_LEG = 1.25            # 直角边 a（水平）
B_LEG = 1.95            # 直角边 b（竖直）
SIDE = A_LEG + B_LEG    # 大正方形边长 a + b
C_LEG = float(np.hypot(A_LEG, B_LEG))   # 斜边 c ≈ 2.316


# ==========================================
# 第一幕：三条边上各作一个正方形
# ==========================================
S1_SCALE = 0.90                                   # 整体缩放，保证不出安全视口
S1_CENTER = np.array([-1.58, 0.18, 0.0])          # 图组包围盒中心
_S1_LOCAL_CENTER = np.array([(SIDE - B_LEG) / 2.0, (SIDE - A_LEG) / 2.0, 0.0])
_S1_SHIFT = S1_CENTER - S1_SCALE * _S1_LOCAL_CENTER


def s1(x, y):
    """第一幕局部坐标（直角顶点为原点，a 沿 +x、b 沿 +y）→ 屏幕坐标。"""
    return S1_SCALE * np.array([float(x), float(y), 0.0]) + _S1_SHIFT


def s1_poly(scene, points, fill_opacity=0.20, color=None, stroke_width=2.5):
    """第一幕多边形（自动套用 s1 坐标映射）。"""
    c = color if color is not None else scene.theme.text_main
    return Polygon(*[s1(x, y) for x, y in points],
                   color=c, fill_opacity=fill_opacity, stroke_width=stroke_width)


def s1_hyp_mid():
    """斜边中点（用于放置 c 的标注）。"""
    return s1(A_LEG / 2.0, B_LEG / 2.0)


def s1_hyp_normal():
    """斜边朝外（远离直角顶点）的单位法向。"""
    return np.array([B_LEG, A_LEG, 0.0]) / C_LEG


# ==========================================
# 第二 / 三幕：同一个大正方形
# ==========================================
SQUARE_ORIGIN = np.array([-2.95, -1.05, 0.0])     # 大正方形左下角


def sq(x, y):
    """大正方形局部坐标（左下角为原点）→ 屏幕坐标。"""
    return SQUARE_ORIGIN + np.array([float(x), float(y), 0.0])


def _polys(scene, quads, fill_opacity=0.80, color=None, stroke_width=2.2):
    c = color if color is not None else scene.theme.text_muted
    return VGroup(*[
        Polygon(*[sq(x, y) for x, y in quad],
                color=c, fill_opacity=fill_opacity, stroke_width=stroke_width)
        for quad in quads
    ])


def square_outline(scene):
    """大正方形外框（边长 a+b）。"""
    return Polygon(
        sq(0, 0), sq(SIDE, 0), sq(SIDE, SIDE), sq(0, SIDE),
        color=scene.theme.text_main, fill_opacity=0.0, stroke_width=3.0,
    )


# 摆法一：四块三角形首尾相接，中央空出 c²
# 每块三角形的顶点顺序统一为 [直角顶点, a 腿端点, b 腿端点]，保证形变平滑
_QUADS_ONE = [
    [(0, 0), (A_LEG, 0), (0, B_LEG)],
    [(SIDE, 0), (SIDE, A_LEG), (A_LEG, 0)],
    [(SIDE, SIDE), (SIDE, A_LEG), (B_LEG, SIDE)],
    [(0, SIDE), (B_LEG, SIDE), (0, B_LEG)],
]

# 摆法二：三角形靠向左下角与右上角，空出 a² 与 b²
# 与摆法一逐块一一对应（T1→U3, T2→U1, T3→U2, T4→U4），重排时每块都做刚体式滑动
_QUADS_TWO = [
    [(A_LEG, A_LEG), (0, A_LEG), (A_LEG, SIDE)],
    [(SIDE, 0), (SIDE, A_LEG), (A_LEG, 0)],
    [(A_LEG, A_LEG), (A_LEG, 0), (SIDE, A_LEG)],
    [(0, SIDE), (A_LEG, SIDE), (0, A_LEG)],
]


def triangles_one(scene):
    """摆法一：四块全等直角三角形。"""
    return _polys(scene, _QUADS_ONE)


def triangles_two(scene):
    """摆法二：同样的四块，只是挪了位置。"""
    return _polys(scene, _QUADS_TWO)


def hole_c(scene):
    """摆法一中央空出来的倾斜正方形，边长 c。"""
    return Polygon(
        sq(A_LEG, 0), sq(SIDE, A_LEG), sq(B_LEG, SIDE), sq(0, B_LEG),
        color=scene.theme.accent, fill_opacity=0.30, stroke_width=3.0,
    )


def hole_a(scene):
    """摆法二左下空出来的正方形，边长 a。"""
    return Polygon(
        sq(0, 0), sq(A_LEG, 0), sq(A_LEG, A_LEG), sq(0, A_LEG),
        color=scene.theme.primary, fill_opacity=0.30, stroke_width=3.0,
    )


def hole_b(scene):
    """摆法二右上空出来的正方形，边长 b。"""
    return Polygon(
        sq(A_LEG, A_LEG), sq(SIDE, A_LEG), sq(SIDE, SIDE), sq(A_LEG, SIDE),
        color=scene.theme.secondary, fill_opacity=0.30, stroke_width=3.0,
    )


def bottom_leg_labels(scene):
    """底边上的 a、b 分段标注（说明边长 = a + b）。"""
    lab_a = scene.make_math("a", font_size=30, color=scene.theme.primary)
    lab_a.move_to(sq(A_LEG / 2.0, 0) + DOWN * 0.26)
    lab_b = scene.make_math("b", font_size=30, color=scene.theme.secondary)
    lab_b.move_to(sq((A_LEG + SIDE) / 2.0, 0) + DOWN * 0.26)
    return VGroup(lab_a, lab_b)


def c2_label(scene):
    """中央 c² 标注。"""
    lab = scene.make_math("c^2", font_size=46, color=scene.theme.accent)
    lab.move_to(sq(SIDE / 2.0, SIDE / 2.0))
    return lab


def a2_label(scene):
    lab = scene.make_math("a^2", font_size=38, color=scene.theme.primary)
    lab.move_to(sq(A_LEG / 2.0, A_LEG / 2.0))
    return lab


def b2_label(scene):
    lab = scene.make_math("b^2", font_size=38, color=scene.theme.secondary)
    lab.move_to(sq((A_LEG + SIDE) / 2.0, (A_LEG + SIDE) / 2.0))
    return lab


# ==========================================
# 右侧公式面板的公共位置（左对齐，第二行缩进到第一个等号下方）
# ==========================================
PANEL_LEFT_X = 1.05
PANEL_MAX_WIDTH = 4.45
PANEL_TOP_Y = 1.15
PANEL_BOT_Y = 0.32


def fit_uniform(mobjects, max_width=PANEL_MAX_WIDTH):
    """把一组公式按**同一个比例**缩放，保证各行字号绝对一致。"""
    widest = max(m.get_width() for m in mobjects)
    if widest > max_width:
        for m in mobjects:
            m.scale(max_width / widest)
    return mobjects


def eq_indent(scene, font_size=44):
    """第二行公式相对第一行左边缘的缩进量（对齐到第一个等号下方）。"""
    ref = scene.make_math("S", font_size=font_size)
    return ref.get_width() + 0.14
