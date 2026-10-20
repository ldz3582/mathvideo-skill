"""
项目专属视觉装置 —— negative_times_negative
《为什么负负得正？》全片共用的数轴、箭头、翻转扫掠弧与结论卡片。

设计意图：
* 一支「箭头」贯穿全片 —— 乘法 = 改变箭头的长度，负号 = 改变箭头的方向；
* 所有翻转都用同一个动作语言表达：箭头绕原点转身 180°，配一条暖金色扫掠弧；
* 颜色语义固定：正方向/正数 = 墨韵石板蓝，负方向/负号 = 赤陶橙，翻转 = 暖金琥珀。
"""
import numpy as np
from manim import *  # noqa: F401,F403

from theme_config import FONT_CHINESE, ClaudeLightTheme, VideoScene


class ProjectScene(VideoScene):
    """本项目分幕基类：字幕替换改为干净的交叉淡换，避免字形硬变形产生重影。"""

    def set_caption(self, text, font_size=20, color=None, max_width=11.2):
        c = color if color is not None else self.theme.text_muted
        single_line = text.replace("\n", " ").strip()
        count = len(single_line)
        size = 15.5 if count > 30 else (17.5 if count > 22 else font_size)
        txt = self.make_text(single_line, font_size=size, color=c)
        if txt.get_width() > max_width:
            txt.scale_to_fit_width(max_width)
        txt.to_edge(DOWN, buff=0.38)
        if self.caption_mobject is None:
            self.play(FadeIn(txt, shift=UP * 0.10), run_time=0.30)
        else:
            self.play(FadeOut(self.caption_mobject, run_time=0.14))
            self.play(FadeIn(txt, run_time=0.16))
        self.caption_mobject = txt
        return txt


# ==========================================
# 公共几何参数（4 幕严格共用，保证视觉一致）
# ==========================================
AXIS_Y = -1.35                    # 数轴所在高度
AXIS_LEN = 11.0                   # 数轴总长（安全视口 |x| <= 6.0）
AXIS_XMIN, AXIS_XMAX = -6, 6
UNIT = AXIS_LEN / (AXIS_XMAX - AXIS_XMIN)   # 每 1 个整数格占的屏幕宽度 ≈ 0.917
TICK_LABELS = (-6, -4, -2, 0, 2, 4, 6)      # 只标偶数位，避免刻度文字拥挤

FORMULA_Y = 1.62                  # 上方公式链的落版高度
CHAIN_Y = 0.95                    # 中途算式的高度（Scene 1）
CARD_POS = np.array([3.55, 1.60, 0.0])   # 右侧结论卡片位置
CARD_BOTTOM = np.array([0.0, -2.55, 0.0])  # 底部结论卡片位置（Scene 4）

COLOR_POS = ClaudeLightTheme.primary      # 正方向 / 正数
COLOR_NEG = ClaudeLightTheme.secondary    # 负方向 / 负号
COLOR_FLIP = ClaudeLightTheme.accent      # 翻转扫掠弧 / 结论
COLOR_MUTED = ClaudeLightTheme.text_muted


# ==========================================
# 公共装置构造
# ==========================================
def axis_point(x):
    """数轴上数值 x 对应的屏幕坐标。"""
    return np.array([x * UNIT, AXIS_Y, 0.0])


def build_number_line():
    """全片共用数轴：单位刻度 + 偶数位数字标签。"""
    axis = NumberLine(
        x_range=[AXIS_XMIN, AXIS_XMAX, 1],
        length=AXIS_LEN,
        color=COLOR_MUTED,
        stroke_width=2.6,
        include_ticks=True,
        tick_size=0.075,
        include_numbers=False,
    )
    axis.move_to(axis_point(0))
    labels = VGroup()
    for value in TICK_LABELS:
        txt = Text(str(value), font=FONT_CHINESE, font_size=19, color=COLOR_MUTED)
        txt.next_to(axis.number_to_point(value), DOWN, buff=0.20)
        labels.add(txt)
    return VGroup(axis, labels)


def build_axis_arrow(x, color, stroke_width=6.0):
    """从原点指向 x 的箭头（长度 = |x|，方向 = 符号）。"""
    return Arrow(
        start=axis_point(0),
        end=axis_point(x),
        buff=0,
        stroke_width=stroke_width,
        color=color,
        tip_length=0.26,
        max_tip_length_to_length_ratio=0.32,
    )


def build_value_label(scene, x, color=None, font_size=34, inward_shift=0.48):
    """跟在箭头尖端上方的数值标签；向原点多收一点，避开刻度数字与扫掠弧。"""
    color = color or (COLOR_POS if x > 0 else COLOR_NEG)
    lbl = scene.make_math(str(x), font_size=font_size, color=color)
    lbl.next_to(axis_point(x), UP, buff=0.16)
    lbl.shift((LEFT if x > 0 else RIGHT) * inward_shift)
    return lbl


def build_sweep(radius, color=COLOR_FLIP, stroke_width=3.6, dashed=False):
    """绕原点扫过 180° 的转向弧（从 +x 正方向经上半平面转到 -x 方向）。"""
    arc = Arc(
        radius=radius,
        start_angle=0,
        angle=PI,
        arc_center=axis_point(0),
        color=color,
        stroke_width=stroke_width,
    )
    return DashedVMobject(arc, num_dashes=26) if dashed else arc


def build_full_turn(radius, color=COLOR_FLIP, stroke_width=3.6):
    """一整圈 360°：两次 180° 翻转的合成结果。"""
    return Circle(radius=radius, color=color, stroke_width=stroke_width).move_to(axis_point(0))


def build_section_label(scene, text, accent=None):
    """左上角幕标题：一条琥珀色竖条 + 一幕主题词。"""
    accent = accent or COLOR_FLIP
    txt = scene.make_text(text, font_size=27, color=scene.theme.text_main)
    bar = Rectangle(width=0.085, height=txt.height * 1.15, color=accent, fill_opacity=1, stroke_width=0)
    bar.next_to(txt, LEFT, buff=0.20)
    group = VGroup(bar, txt)
    group.to_edge(UP, buff=0.85).to_edge(LEFT, buff=0.70)
    return group


def build_result_card(scene, title, lines, accent=None):
    """结论卡片：左侧强调竖条 + 一行标题 + 若干行说明（自动左对齐排布）。"""
    accent = accent or COLOR_FLIP
    title_mob = scene.make_text(title, font_size=30, color=scene.theme.text_main)
    body = VGroup(
        *[scene.make_text(line, font_size=24, color=scene.theme.text_muted) for line in lines]
    )
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    content = VGroup(title_mob, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
    bar = Rectangle(
        width=0.08,
        height=content.height + 0.20,
        color=accent,
        fill_opacity=1,
        stroke_width=0,
    )
    bar.next_to(content, LEFT, buff=0.22)
    return VGroup(bar, content)
