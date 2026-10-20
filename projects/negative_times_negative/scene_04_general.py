"""
Scene 04：两个负号 = 翻转两次 —— 一般化到 (-a)×(-b)=ab，收束全片。
主题: claude_light ｜ 配音: zh-CN-YunxiNeural
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *  # noqa: F401,F403
from theme_config import speech  # 工作台基础设施
from project_style import (  # 本项目专属装置 + 分幕基类
    CARD_BOTTOM,
    COLOR_FLIP,
    COLOR_POS,
    FORMULA_Y,
    UNIT,
    ProjectScene,
    axis_point,
    build_axis_arrow,
    build_full_turn,
    build_number_line,
    build_result_card,
    build_section_label,
    build_sweep,
    build_value_label,
)

RADIUS = 2 * UNIT
FORMULA_POS = np.array([0.0, FORMULA_Y, 0.0])


class Scene04General(ProjectScene):
    DEFAULT_THEME = "claude_light"
    ENABLE_VOICEOVER = True
    VOICE_NAME = "zh-CN-YunxiNeural"

    def construct(self):
        super().construct()

        tag = build_section_label(self, "两个负号 = 翻转两次")
        axis = build_number_line()
        arrow = build_axis_arrow(2, COLOR_POS)
        lbl = build_value_label(self, 2, COLOR_POS)

        # ---------- 1. 一般式：(-a)×(-b) ----------
        chain = self.make_math("(-a)\\times(-b)", font_size=50, color=self.theme.text_main).move_to(FORMULA_POS)
        with speech(self, "把刚才的两步写成一般式：负 a 乘负 b。"):
            self.play(FadeIn(tag, shift=DOWN * 0.2), Create(axis), run_time=1.2)
            self.play(GrowArrow(arrow), FadeIn(lbl), FadeIn(chain, shift=DOWN * 0.15), run_time=0.9)

        # ---------- 2. 拆成两个负一 ----------
        c_two = self.make_math("(-1)a\\times(-1)b", font_size=50, color=self.theme.text_main).move_to(FORMULA_POS)
        with speech(self, "负 a 就是负一乘 a，负 b 就是负一乘 b。", spoken="负 a 就是负一乘 a，负 b 就是负一乘 b。"):
            self.play(FadeOut(chain), run_time=0.22)
            self.play(FadeIn(c_two), run_time=0.28)
        chain = c_two

        c_three = self.make_math("(-1)(-1)\\cdot ab", font_size=50, color=COLOR_FLIP).move_to(FORMULA_POS)
        with speech(self, "把两个负一挑出来，先算它们。"):
            self.play(FadeOut(chain), run_time=0.22)
            self.play(FadeIn(c_three), run_time=0.28)
        chain = c_three

        # ---------- 3. 两个负一 = 两次翻转 ----------
        arc_one = build_sweep(RADIUS)
        arc_two = build_sweep(RADIUS * 1.10, dashed=True)
        with speech(self, "两个负一，就是两次翻转。翻一次改变方向，翻两次回到原样。"):
            self.play(
                Rotate(arrow, angle=PI, about_point=axis_point(0)),
                Create(arc_one),
                run_time=1.6,
            )
            self.play(
                Rotate(arrow, angle=PI, about_point=axis_point(0)),
                Create(arc_two),
                run_time=1.6,
            )

        # ---------- 4. 结论定格 ----------
        full_turn = build_full_turn(RADIUS)
        final = self.make_math("(-a)\\times(-b)=ab", font_size=54, color=COLOR_FLIP).move_to(FORMULA_POS)
        card = build_result_card(self, "负负得正", ["一次负号改变方向", "两次负号把方向改回来"], COLOR_FLIP)
        card.move_to(CARD_BOTTOM)

        with speech(self, "所以负负得正，从来不是一条硬性规定，而是翻转两次的必然结果。"):
            self.play(FadeOut(arc_one), FadeOut(arc_two), Create(full_turn), run_time=1.0)
            self.play(FadeOut(full_turn), FadeOut(arrow), FadeOut(lbl), run_time=0.5)
            self.play(FadeOut(chain), run_time=0.2)
            self.play(FadeIn(final), run_time=0.35)
            self.play(FadeIn(card, shift=UP * 0.2), run_time=0.9)

        self.finish()
