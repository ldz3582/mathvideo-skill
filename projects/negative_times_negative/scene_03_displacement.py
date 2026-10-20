"""
Scene 03：退两步的反方向 —— 用位移理解 (-3)×(-2)=6：先伸缩三倍，再原地反转方向。
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
    ProjectScene,
    axis_point,
    build_axis_arrow,
    build_number_line,
    build_section_label,
    build_sweep,
    build_value_label,
)

FORMULA_POS = np.array([0.0, FORMULA_Y, 0.0])
DESC_POS = np.array([-3.55, 0.72, 0.0])


class Scene03Displacement(ProjectScene):
    DEFAULT_THEME = "claude_light"
    ENABLE_VOICEOVER = True
    VOICE_NAME = "zh-CN-YunxiNeural"

    def construct(self):
        super().construct()

        tag = build_section_label(self, "退两步的反方向")
        axis = build_number_line()
        arrow = build_axis_arrow(-2, COLOR_NEG)
        lbl = build_value_label(self, -2, COLOR_NEG)
        desc = self.make_text("向左退 2 步", font_size=27, color=COLOR_NEG).move_to(DESC_POS)
        chain = self.make_math("(-2)\\times(-3)", font_size=44, color=self.theme.text_main).move_to(FORMULA_POS)

        # ---------- 1. 负二 = 向左退两步 ----------
        with speech(self, "换个更具体的角度。数轴上的负二，可以看成向左退两步。"):
            self.play(FadeIn(tag, shift=DOWN * 0.2), Create(axis), run_time=1.2)
            self.play(GrowArrow(arrow), FadeIn(lbl, shift=UP * 0.12), run_time=0.9)
            self.play(FadeIn(desc, shift=DOWN * 0.15), FadeIn(chain, shift=DOWN * 0.15), run_time=0.8)

        # ---------- 2. 把负三拆成三和负一 ----------
        step_two = self.make_math("(-2)\\times 3\\times(-1)", font_size=44, color=self.theme.text_main).move_to(FORMULA_POS)
        with speech(self, "现在把它乘以负三。负三，就是三乘以负一。"):
            self.play(FadeOut(chain), run_time=0.22)
            self.play(FadeIn(step_two), run_time=0.28)
        chain = step_two

        # ---------- 3. 先乘三：位移拉长三倍 ----------
        with speech(self, "先乘三：长度变成三倍，向左退六步。"):
            lbl_six = build_value_label(self, -6, COLOR_NEG)
            desc_six = self.make_text("向左退 6 步", font_size=27, color=COLOR_NEG).move_to(DESC_POS)
            self.play(FadeOut(lbl), FadeOut(desc), run_time=0.22)
            self.play(
                Transform(arrow, build_axis_arrow(-6, COLOR_NEG)),
                FadeIn(lbl_six),
                FadeIn(desc_six),
                run_time=1.3,
            )
            lbl, desc = lbl_six, desc_six
            step_three = self.make_math("(-6)\\times(-1)", font_size=44, color=self.theme.text_main).move_to(FORMULA_POS)
            self.play(FadeOut(chain), run_time=0.22)
            self.play(FadeIn(step_three), run_time=0.28)
            chain = step_three

        # ---------- 4. 再乘负一：整个位移原地反转方向 ----------
        pivot = build_sweep(0.75)
        with speech(self, "再乘负一：整个位移原地反转方向，向左六步，变成向右六步。"):
            lbl_right = build_value_label(self, 6, COLOR_POS)
            desc_right = self.make_text("向右走 6 步", font_size=27, color=COLOR_POS).move_to(DESC_POS)
            self.play(FadeOut(lbl), FadeOut(desc), run_time=0.22)
            self.play(
                Transform(arrow, build_axis_arrow(6, COLOR_POS)),
                FadeIn(lbl_right),
                FadeIn(desc_right),
                Create(pivot),
                run_time=1.6,
            )
            lbl, desc = lbl_right, desc_right
            self.play(FadeOut(pivot), run_time=0.4)

        # ---------- 5. 结论 ----------
        final = self.make_math("(-3)\\times(-2)=6", font_size=50, color=COLOR_FLIP).move_to(FORMULA_POS)
        with speech(self, "于是负三乘负二，等于正六。两个负号，又一次互相抵消。"):
            self.play(FadeOut(chain), run_time=0.22)
            self.play(FadeIn(final), run_time=0.3)
            self.play(Indicate(arrow, color=COLOR_POS), run_time=0.8)

        self.finish()
