"""
Scene 02：负号就是转身 —— 乘以 (-1) 等于箭头绕原点旋转 180°，两次翻转回到原方向。
主题: claude_light ｜ 配音: zh-CN-YunxiNeural
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *  # noqa: F401,F403
from theme_config import speech  # 工作台基础设施
from project_style import (  # 本项目专属装置 + 分幕基类
    COLOR_FLIP,
    COLOR_NEG,
    COLOR_POS,
    FORMULA_Y,
    UNIT,
    ProjectScene,
    axis_point,
    build_axis_arrow,
    build_full_turn,
    build_number_line,
    build_section_label,
    build_sweep,
    build_value_label,
)

RADIUS = 2 * UNIT          # 箭头长度 2 对应的屏幕半径
FORMULA_POS = np.array([0.0, FORMULA_Y, 0.0])
CHIP_POS = np.array([-3.5, 0.35, 0.0])


class Scene02Flip(ProjectScene):
    DEFAULT_THEME = "claude_light"
    ENABLE_VOICEOVER = True
    VOICE_NAME = "zh-CN-YunxiNeural"

    def construct(self):
        super().construct()

        tag = build_section_label(self, "负号 = 转身 180°")
        axis = build_number_line()
        arrow = build_axis_arrow(2, COLOR_POS)
        lbl = build_value_label(self, 2, COLOR_POS)
        chip = self.make_math("\\times(-1)", font_size=40, color=COLOR_NEG).move_to(CHIP_POS)

        # ---------- 1. 数轴上的一支箭头，乘上 (-1) ----------
        with speech(self, "那负号呢？给这支箭头乘负一试试。"):
            self.play(FadeIn(tag, shift=DOWN * 0.2), Create(axis), FadeIn(chip), run_time=1.3)
            self.play(GrowArrow(arrow), FadeIn(lbl, shift=UP * 0.12), run_time=0.9)

        # ---------- 2. 第一次翻转：绕原点转身 180° ----------
        arc_one = build_sweep(RADIUS)
        lbl_neg = build_value_label(self, -2, COLOR_NEG)
        with speech(self, "乘负一，就是让它绕原点原地转身一百八十度，从正方向翻到负方向。"):
            self.play(FadeOut(lbl), run_time=0.22)
            self.play(
                Rotate(arrow, angle=PI, about_point=axis_point(0)),
                Create(arc_one),
                Indicate(chip, color=COLOR_NEG, scale_factor=1.12),
                run_time=2.0,
            )
            self.play(FadeIn(lbl_neg), run_time=0.25)

        # ---------- 3. 第二次翻转：方向原封不动地回来 ----------
        arc_two = build_sweep(RADIUS * 1.10, dashed=True)
        lbl_home = build_value_label(self, 2, COLOR_POS)
        with speech(self, "再乘一次负一，又要转身一百八十度。"):
            self.play(FadeOut(lbl_neg), run_time=0.22)
            self.play(
                Rotate(arrow, angle=PI, about_point=axis_point(0)),
                Create(arc_two),
                run_time=2.0,
            )
            self.play(FadeIn(lbl_home), run_time=0.25)

        # ---------- 4. 两次翻转合成一整圈，得出 (-1)×(-1)=1 ----------
        full_turn = build_full_turn(RADIUS)
        result = self.make_math("(-1)\\times(-1)=1", font_size=50, color=COLOR_FLIP).move_to(FORMULA_POS)

        with speech(self, "两次翻转，方向原封不动地回来了。所以负一乘负一，等于正一。"):
            self.play(FadeOut(arc_one), FadeOut(arc_two), Create(full_turn), run_time=1.1)
            self.play(FadeIn(result, scale=1.12), Indicate(arrow, color=COLOR_POS), run_time=1.1)

        self.finish()
