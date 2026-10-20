"""
项目专属视觉装置 —— 圆的面积为什么是 πr²

* theme_config.py  = 工作台基础设施（**不要手改**）
* project_style.py = 本项目的常量、配色、几何装置（随便改）
"""
import numpy as np
from manim import *

from theme_config import THEMES

THEME = THEMES["3b1b_dark"]

PRIMARY = THEME.primary      # 天蓝：圆 / 主图形
SECONDARY = THEME.secondary  # 活力橙：隔块扇形 / 辅助
ACCENT = THEME.accent        # 启迪金黄：高亮与尺寸
SUCCESS = THEME.success      # 翡翠绿：最终结论
MUTED = THEME.text_muted
INK = THEME.text_main

RADIUS = 1.75


def piece_color(k):
    """奇偶交替配色，让拼接关系一眼可读。"""
    return PRIMARY if k % 2 == 0 else SECONDARY


def sector_piece(radius, start_angle, angle, color, fill_opacity=0.45):
    return Sector(
        radius=radius,
        start_angle=start_angle,
        angle=angle,
        fill_color=color,
        fill_opacity=fill_opacity,
        stroke_color=color,
        stroke_width=1.6,
        stroke_opacity=0.95,
    )


def circle_fan(n, radius=RADIUS, center=ORIGIN):
    """圆内 n 个等分扇形，尖端全部落在圆心。"""
    theta = TAU / n
    group = VGroup()
    for k in range(n):
        piece = sector_piece(radius, k * theta, theta, piece_color(k))
        piece.shift(center)
        group.add(piece)
    return group


def fan_metrics(n, radius=RADIUS):
    """返回 (单片弧的弦长 d, 弦到弧顶的垂距 h, 整排宽度 n·d/2)。"""
    theta = TAU / n
    d = 2 * radius * np.sin(theta / 2)
    h = radius * np.cos(theta / 2)
    return d, h, n * d / 2


def fan_arrangement(n, radius=RADIUS, center=ORIGIN):
    """
    把 n 个扇形交错拼成近平行四边形：
    偶数片尖朝下、弧朝上；奇数片翻转 180°，尖朝上、弧朝下。
    相邻扇形共享一条半径边，尖端横向间距 d/2。
    """
    theta = TAU / n
    d, h, _ = fan_metrics(n, radius)
    group = VGroup()
    for k in range(n):
        apex_x = k * d / 2
        if k % 2 == 0:
            start_angle = PI / 2 - theta / 2
            apex_y = 0.0
        else:
            start_angle = -PI / 2 - theta / 2
            apex_y = h
        piece = sector_piece(radius, start_angle, theta, piece_color(k))
        piece.shift([apex_x, apex_y, 0])
        group.add(piece)
    group.move_to(center)
    return group


def h_dimension(start, end, label, color=ACCENT, text_size=30, label_buff=0.22):
    """水平尺寸线：双箭头 + 居中标签。"""
    arrow = DoubleArrow(start, end, buff=0, color=color, stroke_width=2.2, tip_length=0.18)
    text = MathTex(label, font_size=text_size, color=color).next_to(arrow, DOWN, buff=label_buff)
    return VGroup(arrow, text)


def v_dimension(start, end, label, color=ACCENT, text_size=30, label_buff=0.22):
    """垂直尺寸线：双箭头 + 右侧标签。"""
    arrow = DoubleArrow(start, end, buff=0, color=color, stroke_width=2.2, tip_length=0.18)
    text = MathTex(label, font_size=text_size, color=color).next_to(arrow, RIGHT, buff=label_buff)
    return VGroup(arrow, text)
