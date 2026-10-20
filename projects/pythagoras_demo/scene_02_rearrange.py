"""
Scene 02: 同样四个三角形换一种摆法，空出 a² 与 b² 两个正方形，
与第一幕的同一个大正方形对照，得到 c² = a² + b²。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *
from theme_config import VideoScene, speech, export_timeline

from project_style import (
    big_square,
    rearranged_triangles,
    side_labels,
    square_a,
    square_b,
)

TIMELINE_FILE = Path(__file__).resolve().parent / "voiceover_timeline_Scene02Rearrange.json"


class Scene02Rearrange(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()

        # ---------- 1. 换个摆法 ----------
        with speech(self, "换一种摆法。同样四个三角形，这次让它们分别靠在左下和右上的两个角上。",
                    spoken="换一种摆法。同样四个三角形，这次让它们分别靠在左下和右上的两个角上。"):
            self.play_show_title("换一种摆法，答案就出来了", "Rearrange the Same Four Triangles")
            outline = big_square(self)
            self.play(Create(outline), run_time=1.0)
            triangles = rearranged_triangles(self)
            self.play(
                LaggedStart(*[FadeIn(tri, shift=UP * 0.12) for tri in triangles], lag_ratio=0.25),
                run_time=2.4,
            )

        # ---------- 2. 空出来的是 a² 与 b² ----------
        with speech(self, "这一回空出来的是两个正方形：一个边长 a，面积 a 的平方；一个边长 b，面积 b 的平方。",
                    spoken="这一回空出来的是两个正方形：一个边长 a，面积 a 的平方；一个边长 b，面积 b 的平方。"):
            sq_a, sq_b = square_a(self), square_b(self)
            self.play(FadeIn(sq_a), run_time=0.7)
            label_a = self.make_math("a^2", font_size=42, color=self.theme.primary)
            label_a.move_to(sq_a.get_center())
            self.play(Write(label_a), run_time=0.7)
            self.play(FadeIn(sq_b), run_time=0.7)
            label_b = self.make_math("b^2", font_size=42, color=self.theme.secondary)
            label_b.move_to(sq_b.get_center())
            self.play(Write(label_b), run_time=0.7)
            self.play(FadeIn(side_labels(self), shift=DOWN * 0.1), run_time=0.6)

        # ---------- 3. 同一个大正方形，两种算法 ----------
        with speech(self, "大正方形还是那个大正方形。去掉同样四个三角形，剩下的面积必然相等。",
                    spoken="大正方形还是那个大正方形。去掉同样四个三角形，剩下的面积必然相等。"):
            equation = self.make_math(r"(a+b)^2 = 4\cdot\frac{1}{2}ab + a^2 + b^2", font_size=36)
            equation.move_to(np.array([0.0, -2.35, 0.0]))
            equation.set_color_by_tex("a^2", self.theme.primary)
            equation.set_color_by_tex("b^2", self.theme.secondary)
            self.play(Write(equation), run_time=1.8)

        # ---------- 4. 两边约掉四个三角形 ----------
        with speech(self, "两边约掉同样的四个三角形，就只剩下：c 的平方，等于 a 的平方加上 b 的平方。",
                    spoken="两边约掉同样的四个三角形，就只剩下：c 的平方，等于 a 的平方加上 b 的平方。"):
            self.play(FadeOut(equation), run_time=0.6)
            conclusion = self.make_math(r"c^2 = a^2 + b^2", font_size=64)
            conclusion.move_to(np.array([0.0, -2.1, 0.0]))
            conclusion.set_color_by_tex("c^2", self.theme.accent)
            conclusion.set_color_by_tex("a^2", self.theme.primary)
            conclusion.set_color_by_tex("b^2", self.theme.secondary)
            self.play(Write(conclusion), run_time=1.6)
            self.play(Circumscribe(conclusion, color=self.theme.accent, run_time=1.0))
            self.add_sleek_horizon(conclusion)

        self.finish()
