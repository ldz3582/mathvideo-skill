"""
Scene 01：乘法就是伸缩 —— 数轴上的正数乘法只改变箭头长度，不改变方向。
主题: claude_light ｜ 配音: zh-CN-YunxiNeural
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *  # noqa: F401,F403
from theme_config import speech  # 工作台基础设施
from project_style import (  # 本项目专属装置 + 分幕基类
    CHAIN_Y,
    CARD_POS,
    COLOR_POS,
    ProjectScene,
    build_axis_arrow,
    build_number_line,
    build_result_card,
    build_value_label,
)

CHAIN_POS = np.array([0.0, CHAIN_Y, 0.0])


class Scene01Scale(ProjectScene):
    DEFAULT_THEME = "claude_light"
    ENABLE_VOICEOVER = True
    VOICE_NAME = "zh-CN-YunxiNeural"

    def construct(self):
        super().construct()

        axis = build_number_line()

        # ---------- 1. 开场：一根数轴，一支长度为 1 的箭头 ----------
        with speech(self, "先从最朴素的一件事说起：数轴上的乘法，其实就是把一支箭头拉长。"):
            self.play_show_title("为什么负负得正？", "Why  (-1) × (-1) = 1")
            self.play(Create(axis), run_time=1.3)

        arrow = build_axis_arrow(1, COLOR_POS)
        lbl = build_value_label(self, 1, COLOR_POS)
        chain = self.make_math("1", font_size=44, color=self.theme.text_main).move_to(CHAIN_POS)

        with speech(self, "从原点出发的这支箭头，长度是一，代表一个单位。"):
            self.play(GrowArrow(arrow), FadeIn(lbl, shift=UP * 0.12), run_time=0.9)
            self.play(FadeIn(chain, shift=DOWN * 0.15), run_time=0.5)

        # ---------- 2. 乘 2、乘 3：箭头越伸越长 ----------
        lbl_2 = build_value_label(self, 2, COLOR_POS)
        lbl_3 = build_value_label(self, 6, COLOR_POS)
        chain_2 = self.make_math("1\\times 2=2", font_size=44, color=self.theme.text_main).move_to(CHAIN_POS)
        chain_3 = self.make_math("1\\times 2\\times 3=6", font_size=44, color=self.theme.text_main).move_to(CHAIN_POS)

        with speech(self, "把它乘二，箭头伸到二；再乘三，一直伸到六。"):
            self.play(FadeOut(lbl), FadeOut(chain), run_time=0.25)
            self.play(
                Transform(arrow, build_axis_arrow(2, COLOR_POS)),
                FadeIn(lbl_2),
                FadeIn(chain_2),
                run_time=1.0,
            )
            lbl, chain = lbl_2, chain_2
            self.play(FadeOut(lbl), FadeOut(chain), run_time=0.25)
            self.play(
                Transform(arrow, build_axis_arrow(6, COLOR_POS)),
                FadeIn(lbl_3),
                FadeIn(chain_3),
                run_time=1.2,
            )
            lbl, chain = lbl_3, chain_3

        # ---------- 3. 结论：正数乘法只改变长度 ----------
        card = build_result_card(self, "正数乘法", ["只改变长度", "方向不变"], COLOR_POS).move_to(CARD_POS)
        with speech(self, "你看，从头到尾方向一点没变。正数乘法，只改变长度。"):
            self.play(
                FadeIn(card, shift=LEFT * 0.25),
                Indicate(arrow, color=COLOR_POS, scale_factor=1.05),
                run_time=1.2,
            )

        self.finish()
