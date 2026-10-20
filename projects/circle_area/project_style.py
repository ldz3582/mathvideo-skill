"""
项目专属视觉装置（circle_area）：圆环/长条/三角形三件套的公共几何参数与构造。

约定：
* theme_config.py 是工作台自动同步的基础设施（基类、字体、TTS、语画同步），**不要手改**；
* 本项目特有的常量与构图函数一律放这里，工作台升级不会覆盖；
* 分幕中的公共几何务必从这里取，保证多幕之间视觉严格一致。
"""
import numpy as np
from manim import (
    DOWN,
    LEFT,
    Annulus,
    Line,
    ManimColor,
    Polygon,
    Rectangle,
    VGroup,
    interpolate_color,
)

from theme_config import ClaudeLightTheme

# ==========================================
# 公共几何参数（两幕共享，保证视觉严格一致）
# ==========================================
N_RINGS = 16
R_CIRCLE = 1.5
CIRCLE_CENTER = np.array([0.0, 1.15, 0.0])
BASE_HALF = 5.3                                       # 底边半宽，视觉代表 pi * r
TRI_BOTTOM = -2.35
TRI_HEIGHT = (2 * BASE_HALF) / (2 * np.pi)            # 底 : 高 = 2*pi*r : r，形状真实
BAR_HEIGHT = TRI_HEIGHT / N_RINGS


def ring_color(i):
    """由内到外从墨韵石板蓝渐变到赤陶橙，与拉直后的长条颜色一一对应。"""
    return interpolate_color(
        ManimColor(ClaudeLightTheme.primary),
        ManimColor(ClaudeLightTheme.secondary),
        i / (N_RINGS - 1),
    )


def build_rings():
    """同心圆环组（内圈最小，颜色最蓝；外圈最大，颜色最橙）。"""
    dr = R_CIRCLE / N_RINGS
    rings = VGroup()
    for i in range(N_RINGS):
        rings.add(
            Annulus(
                inner_radius=max(i * dr, 0.015),
                outer_radius=(i + 1) * dr,
                fill_opacity=0.92,
                stroke_width=0,
                color=ring_color(i),
            ).move_to(CIRCLE_CENTER)
        )
    return rings


def build_bars():
    """把每圈圆环拉直成一条长度正比于 2*pi*rho 的长条，左对齐由短到长堆叠。"""
    bars = VGroup()
    for i in range(N_RINGS):
        rho = (i + 0.5) * R_CIRCLE / N_RINGS
        width = (rho / R_CIRCLE) * 2 * BASE_HALF
        bar = Rectangle(
            width=width,
            height=BAR_HEIGHT,
            fill_opacity=0.92,
            stroke_width=0,
            color=ring_color(i),
        )
        bar.move_to(np.array([-BASE_HALF + width / 2, TRI_BOTTOM + (i + 0.5) * BAR_HEIGHT, 0]))
        bars.add(bar)
    return bars


def triangle_points():
    """直角三角形三顶点：左下直角顶点、左上顶点(高)、右下端点(底)。"""
    vertex = np.array([-BASE_HALF, TRI_BOTTOM, 0.0])
    apex = np.array([-BASE_HALF, TRI_BOTTOM + TRI_HEIGHT, 0.0])
    right_end = np.array([BASE_HALF, TRI_BOTTOM, 0.0])
    return vertex, apex, right_end


def build_triangle_outline():
    vertex, apex, right_end = triangle_points()
    return Polygon(
        vertex, apex, right_end,
        color=ClaudeLightTheme.accent,
        stroke_width=3,
        fill_opacity=0,
    )


def build_triangle_labels(scene):
    """底 = 2*pi*r (赤陶橙) 与 高 = r (石板蓝) 标签。"""
    vertex, apex, right_end = triangle_points()
    lbl_base = scene.make_math(r"2\pi r", font_size=38, color=ClaudeLightTheme.secondary)
    lbl_base.next_to(Line(vertex, right_end), DOWN, buff=0.22)
    lbl_h = scene.make_math("r", font_size=36, color=ClaudeLightTheme.primary)
    lbl_h.next_to(Line(vertex, apex), LEFT, buff=0.2)
    return lbl_base, lbl_h
