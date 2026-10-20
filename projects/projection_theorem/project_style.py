"""
项目专属视觉装置（projection_theorem）：射影定理演示的公共几何。

五幕共用同一批顶点与配色，保证「同一个直角三角形」在每一幕里像素级一致。

配色语义（贯穿全片）：
    primary   墨蓝   → 直角边 AC，以及它在斜边上的射影 AD
    secondary 赤陶橙 → 直角边 BC，以及它在斜边上的射影 DB
    accent    暖金   → 斜边上的高 CD
    success   鼠尾草绿 → 相似判定 / 勾股定理
"""
import numpy as np
from manim import (
    ORIGIN,
    PI,
    RIGHT,
    TAU,
    Arc,
    DashedLine,
    Dot,
    Line,
    Polygon,
    VGroup,
    always_redraw,
    angle_of_vector,
)

# ---------------- 公共几何参数 ----------------
BASE_Y = -1.35            # 斜边 AB 所在水平线
A_X = -5.15               # 顶点 A 的横坐标
AD_LEN = 1.90             # AD（AC 在斜边上的射影）
DB_LEN = 2.85             # DB（BC 在斜边上的射影），AD : DB = 2 : 3
AB_LEN = AD_LEN + DB_LEN
CD_LEN = (AD_LEN * DB_LEN) ** 0.5      # 斜边上的高 CD = √(AD·DB)

A_PT = np.array([A_X, BASE_Y, 0.0])
B_PT = np.array([A_X + AB_LEN, BASE_Y, 0.0])
D_PT = np.array([A_X + AD_LEN, BASE_Y, 0.0])
C_PT = np.array([A_X + AD_LEN, BASE_Y + CD_LEN, 0.0])

RIGHT_PANEL_X = 3.05      # 右侧推导面板的水平中心


# ---------------- 排版小工具 ----------------
def fit(mobject, max_width=5.2):
    """超宽就等比压缩，杜绝出界。"""
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    return mobject


def legend_row(scene, color, label, font_size=22):
    """一行图例：彩色短线 + 说明文字。"""
    bullet = Line(ORIGIN, RIGHT * 0.34, color=color, stroke_width=5.5)
    row = VGroup(bullet, scene.make_text(label, font_size=font_size))
    row.arrange(RIGHT, buff=0.22)
    return row


# ---------------- 基本图形 ----------------
def side_ab(scene):
    return Line(A_PT, B_PT, color=scene.theme.text_main, stroke_width=3.0)


def side_ac(scene):
    return Line(A_PT, C_PT, color=scene.theme.primary, stroke_width=3.0)


def side_bc(scene):
    return Line(B_PT, C_PT, color=scene.theme.secondary, stroke_width=3.0)


def altitude_cd(scene):
    return Line(C_PT, D_PT, color=scene.theme.accent, stroke_width=3.0)


def triangle_fill(scene, opacity=0.055):
    return Polygon(
        A_PT, B_PT, C_PT,
        color=scene.theme.text_main, fill_opacity=opacity,
        stroke_width=0, stroke_opacity=0,
    )


def sub_triangle(scene, which, fill_opacity=0.26, stroke_width=2.0):
    """高亮子三角形：which ∈ {"acd", "cbd", "abc"}"""
    table = {
        "acd": (A_PT, C_PT, D_PT, scene.theme.primary),
        "cbd": (C_PT, B_PT, D_PT, scene.theme.secondary),
        "abc": (A_PT, B_PT, C_PT, scene.theme.text_main),
    }
    p1, p2, p3, color = table[which]
    return Polygon(p1, p2, p3, color=color, fill_opacity=fill_opacity, stroke_width=stroke_width)


def vertex_labels(scene):
    """A / B / C / D 四个顶点标注（返回 VGroup，可按索引取用）。"""
    A = scene.make_math("A", font_size=30).move_to(A_PT + np.array([-0.30, -0.20, 0.0]))
    B = scene.make_math("B", font_size=30).move_to(B_PT + np.array([0.30, -0.20, 0.0]))
    C = scene.make_math("C", font_size=30).move_to(C_PT + np.array([-0.32, 0.18, 0.0]))
    D = scene.make_math("D", font_size=30).move_to(D_PT + np.array([0.0, -0.36, 0.0]))
    return VGroup(A, B, C, D)


def right_angle_mark(scene, corner, p1, p2, length=0.28, color=None):
    """在 corner 处沿 corner→p1、corner→p2 两个方向画直角小方块。"""
    c = color if color is not None else scene.theme.text_muted
    u = (p1 - corner) / np.linalg.norm(p1 - corner) * length
    v = (p2 - corner) / np.linalg.norm(p2 - corner) * length
    return VGroup(
        Line(corner + u, corner + u + v, color=c, stroke_width=2.4),
        Line(corner + u + v, corner + v, color=c, stroke_width=2.4),
    )


def angle_arc(center, p1, p2, radius=0.5, color=None, stroke_width=3.2):
    """在 center 处画 p1、p2 之间的那个小夹角（自动取劣弧）。"""
    a1, a2 = angle_of_vector(p1 - center), angle_of_vector(p2 - center)
    delta = (a2 - a1) % TAU
    if delta > PI:
        a1, a2, delta = a2, a1, TAU - delta
    return Arc(
        radius=radius, start_angle=a1, angle=delta, arc_center=center,
        color=color, stroke_width=stroke_width,
    )


def static_figure(scene, with_labels=True, with_fill=True):
    """
    五幕共用的静态底图：三角形 + 高 + 两处直角标记 + 顶点标注。
    返回 (group, parts)，parts 里带各处引用，便于单独高亮。
    """
    sides = VGroup(side_ab(scene), side_ac(scene), side_bc(scene), altitude_cd(scene))
    ra_c = right_angle_mark(scene, C_PT, A_PT, B_PT, length=0.30)
    ra_d = right_angle_mark(scene, D_PT, A_PT, C_PT, length=0.22)
    marks = VGroup(ra_c, ra_d)
    labels = vertex_labels(scene) if with_labels else VGroup()

    group = VGroup()
    if with_fill:
        group.add(triangle_fill(scene))
    group.add(sides, marks, labels)
    return group, {"sides": sides, "ra_c": ra_c, "ra_d": ra_d, "labels": labels}


# ---------------- 第四幕：垂直投影扫掠装置 ----------------
def projection_sweep(scene, tracker, start_pt, end_pt, color, dash_color=None):
    """
    「光垂直照下来」的动效：动点沿 start→end 移动，同时向斜边投垂直虚线，
    落点在斜边上扫出一段 —— 那段就是射影。
    返回 (虚线, 动点, 影子点) 三个 always_redraw 对象。
    """
    dc = dash_color if dash_color is not None else scene.theme.text_muted

    def point():
        return start_pt + tracker.get_value() * (end_pt - start_pt)

    def foot():
        p = point()
        return np.array([p[0], BASE_Y, 0.0])

    dashed = always_redraw(
        lambda: DashedLine(point(), foot(), color=dc, dash_length=0.09, stroke_width=2.2)
    )
    mover = always_redraw(lambda: Dot(point(), radius=0.075, color=color))
    shadow = always_redraw(lambda: Dot(foot(), radius=0.075, color=color))
    return dashed, mover, shadow


# ---------------- 第五幕：例题用的自定义几何 ----------------
def custom_geometry(ad_len, db_len, left_x, base_y):
    """按给定 AD、DB 长度生成一组几何点（比例真实，便于画例题）。"""
    h = (ad_len * db_len) ** 0.5
    a = np.array([left_x, base_y, 0.0])
    d = np.array([left_x + ad_len, base_y, 0.0])
    b = np.array([left_x + ad_len + db_len, base_y, 0.0])
    c = np.array([left_x + ad_len, base_y + h, 0.0])
    return {"A": a, "B": b, "C": c, "D": d}


def draw_geometry(scene, geo, with_labels=True):
    """把 custom_geometry 的点画成与主图同款的三角形。"""
    a, b, c, d = geo["A"], geo["B"], geo["C"], geo["D"]
    fill = Polygon(a, b, c, color=scene.theme.text_main, fill_opacity=0.055,
                   stroke_width=0, stroke_opacity=0)
    sides = VGroup(
        Line(a, b, color=scene.theme.text_main, stroke_width=3.0),
        Line(a, c, color=scene.theme.primary, stroke_width=3.0),
        Line(b, c, color=scene.theme.secondary, stroke_width=3.0),
        Line(c, d, color=scene.theme.accent, stroke_width=3.0),
    )
    marks = VGroup(
        right_angle_mark(scene, c, a, b, length=0.26),
        right_angle_mark(scene, d, a, c, length=0.19),
    )
    labels = VGroup()
    if with_labels:
        labels = VGroup(
            scene.make_math("A", font_size=28).move_to(a + np.array([-0.26, -0.18, 0.0])),
            scene.make_math("B", font_size=28).move_to(b + np.array([0.26, -0.18, 0.0])),
            scene.make_math("C", font_size=28).move_to(c + np.array([-0.28, 0.16, 0.0])),
            scene.make_math("D", font_size=28).move_to(d + np.array([0.0, -0.34, 0.0])),
        )
    group = VGroup(fill, sides, marks, labels)
    return group, {"sides": sides, "marks": marks, "labels": labels, "points": geo}
