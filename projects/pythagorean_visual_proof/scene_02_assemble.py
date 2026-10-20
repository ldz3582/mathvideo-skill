"""
Scene 02：拼图第一步 —— 四个全等直角三角形首尾相接，拼成边长 a+b 的大正方形，
中央空出边长 c 的倾斜正方形。

面积恒等式（第一种算法）：(a+b)² = 4·(½ab) + c²
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *  # noqa: F401,F403
from theme_config import VideoScene, speech

from project_style import (
    PANEL_BOT_Y,
    PANEL_LEFT_X,
    PANEL_TOP_Y,
    bottom_leg_labels,
    c2_label,
    eq_indent,
    fit_uniform,
    hole_c,
    square_outline,
    triangles_one,
)


class Scene02Assemble(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()

        outline = square_outline(self)
        tris = triangles_one(self)
        hole = hole_c(self)
        indent = eq_indent(self, font_size=44)

        # ---------- 1. 四块三角形拼成大正方形 ----------
        with speech(self, "把四个一模一样的直角三角形，首尾相接，摆成一个大正方形。",
                    spoken="把四个一模一样的直角三角形，首尾相接，摆成一个大正方形。"):
            self.play(Create(outline), run_time=1.0)
            self.play(Create(tris[0]), run_time=0.9)
            self.play(
                LaggedStart(*[TransformFromCopy(tris[0], t) for t in tris[1:]], lag_ratio=0.45),
                run_time=2.6,
            )

        # ---------- 2. 中央空洞就是 c² ----------
        with speech(self, "中间空出来的，是一个倾斜的正方形：四条边都是斜边 c，所以面积就是 c²。",
                    spoken="中间空出来的，是一个倾斜的正方形。它的四条边，都是三角形的斜边 c，"
                           "所以它的面积，就是 c 的平方。"):
            label_c2 = c2_label(self)
            self.play(FadeIn(hole), run_time=1.0)
            self.play(Write(label_c2), run_time=0.8)
            self.play(Circumscribe(hole, color=self.theme.accent, run_time=0.9))

        # ---------- 3. 大正方形面积的第一种算法 ----------
        with speech(self, "现在来算面积。大正方形的边长是 a 加 b，面积就是 a 加 b 的平方。",
                    spoken="现在来算面积。大正方形的边长，是 a 加 b，所以面积就是 a 加 b 的平方。"):
            side_labels = bottom_leg_labels(self)
            self.play(FadeIn(side_labels, shift=UP * 0.1), run_time=0.8)

            eq1 = self.make_math(r"S=(a+b)^2", font_size=44)
            fit_uniform([eq1])
            eq1.move_to(np.array([PANEL_LEFT_X, PANEL_TOP_Y, 0.0]), aligned_edge=LEFT)
            self.play(Write(eq1), run_time=1.4)

        # ---------- 4. 第二种算法：四块三角形 + c² ----------
        with speech(self, "它同时也等于四块三角形，加上中间那个 c²。",
                    spoken="它同时也等于，四块三角形，再加上中间那个 c 的平方。"):
            eq2 = self.make_math(
                r"=4\times\frac{1}{2}ab+c^2", font_size=44,
                tex_to_color_map={
                    r"4\times\frac{1}{2}ab": self.theme.text_muted,
                    "c^2": self.theme.accent,
                },
            )
            fit_uniform([eq2])
            eq2.move_to(np.array([PANEL_LEFT_X + indent, PANEL_BOT_Y, 0.0]), aligned_edge=LEFT)
            self.play(Write(eq2), run_time=1.5)
            self.play(Indicate(tris, color=self.theme.text_main, scale_factor=1.04), run_time=1.0)
            self.play(Indicate(hole, color=self.theme.accent, scale_factor=1.06), run_time=1.0)
            self.wait(0.3)

        self.finish()
