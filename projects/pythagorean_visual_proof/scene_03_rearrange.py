"""
Scene 03：换一种摆法 —— 同样四块三角形靠向左下角与右上角，
空出来的变成边长 a、b 的两个正方形。

面积恒等式（第二种算法）：(a+b)² = 4·(½ab) + a² + b²
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
    a2_label,
    b2_label,
    bottom_leg_labels,
    eq_indent,
    fit_uniform,
    hole_a,
    hole_b,
    square_outline,
    triangles_one,
    triangles_two,
)


class Scene03Rearrange(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()

        outline = square_outline(self)
        tris_one = triangles_one(self)
        tris_two = triangles_two(self)
        indent = eq_indent(self, font_size=44)

        # ---------- 1. 把四块三角形整体换位 ----------
        with speech(self, "换一种摆法：还是这四个三角形，这次让它们分别靠向左下角和右上角。",
                    spoken="换一种摆法。还是这四个三角形，这一次，让它们分别靠向左下角，和右上角。"):
            self.play(Create(outline), run_time=0.9)
            self.play(FadeIn(tris_one), run_time=0.8)
            self.wait(0.4)
            self.play(
                *[Transform(a, b, path_arc=0.40) for a, b in zip(tris_one, tris_two)],
                run_time=2.6,
            )

        # ---------- 2. 空出来的两个正方形 ----------
        with speech(self, "这一次空出来的是两个正方形：左下边长 a，面积 a²；右上边长 b，面积 b²。",
                    spoken="这一次空出来的，是两个正方形。左下角边长 a，面积是 a 的平方；"
                           "右上角边长 b，面积是 b 的平方。"):
            sq_a = hole_a(self)
            sq_b = hole_b(self)
            lab_a2 = a2_label(self)
            lab_b2 = b2_label(self)
            self.play(FadeIn(sq_a), run_time=0.9)
            self.play(Write(lab_a2), run_time=0.7)
            self.play(FadeIn(sq_b), run_time=0.9)
            self.play(Write(lab_b2), run_time=0.7)
            self.play(
                LaggedStart(Circumscribe(sq_a, color=self.theme.primary, run_time=0.8),
                            Circumscribe(sq_b, color=self.theme.secondary, run_time=0.8),
                            lag_ratio=0.5),
            )

        # ---------- 3. 第二种算法的面积恒等式 ----------
        with speech(self, "同一个大正方形，面积还是 a 加 b 的平方；它等于四块三角形，加上 a²，再加上 b²。",
                    spoken="同一个大正方形，面积还是 a 加 b 的平方。它等于四块三角形，"
                           "加上 a 的平方，再加上 b 的平方。"):
            side_labels = bottom_leg_labels(self)
            self.play(FadeIn(side_labels, shift=UP * 0.1), run_time=0.8)

            eq1 = self.make_math(r"S=(a+b)^2", font_size=44)
            eq2 = self.make_math(
                r"=4\times\frac{1}{2}ab+a^2+b^2", font_size=44,
                tex_to_color_map={
                    r"4\times\frac{1}{2}ab": self.theme.text_muted,
                    "a^2": self.theme.primary,
                    "b^2": self.theme.secondary,
                },
            )
            fit_uniform([eq1, eq2])
            eq1.move_to(np.array([PANEL_LEFT_X, PANEL_TOP_Y, 0.0]), aligned_edge=LEFT)
            eq2.move_to(np.array([PANEL_LEFT_X + indent, PANEL_BOT_Y, 0.0]), aligned_edge=LEFT)
            self.play(Write(eq1), run_time=1.2)
            self.play(Write(eq2), run_time=1.6)
            self.play(Indicate(VGroup(sq_a, sq_b), color=self.theme.text_main, scale_factor=1.04),
                      run_time=1.0)
            self.wait(0.3)

        self.finish()
