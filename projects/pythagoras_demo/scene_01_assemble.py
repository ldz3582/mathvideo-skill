"""
Scene 01: 四个全等直角三角形首尾相接摆成大正方形，中间空出边长 c 的倾斜正方形。
结论铺垫：(a+b)^2 = 4·(1/2)ab + c^2
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *
from theme_config import VideoScene, speech, export_timeline

from project_style import (
    ASSEMBLY_ORIGIN,
    UNIT_ORIGIN,
    assembly_triangles,
    inner_square,
    unit_labels,
    unit_triangle,
)

TIMELINE_FILE = Path(__file__).resolve().parent / "voiceover_timeline_Scene01Assemble.json"


class Scene01Assemble(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()

        # ---------- 1. 立题 + 单个直角三角形 ----------
        with speech(self, "勾股定理说：两条直角边的平方和，等于斜边的平方。它为什么成立？",
                    spoken="勾股定理说：两条直角边的平方和，等于斜边的平方。它为什么成立？"):
            self.play_show_title("勾股定理，为什么成立？", "A Visual Proof")
            template = unit_triangle(self, UNIT_ORIGIN)
            lab_a, lab_b, lab_c = unit_labels(self, UNIT_ORIGIN)
            self.play(Create(template), run_time=1.3)
            self.play(FadeIn(VGroup(lab_a, lab_b, lab_c), shift=UP * 0.1), run_time=0.7)

        # ---------- 2. 标注三边 ----------
        with speech(self, "这是一个直角三角形，两条直角边分别是 a 和 b，斜边是 c。",
                    spoken="这是一个直角三角形，两条直角边分别是 a 和 b，斜边是 c。"):
            self.play(Indicate(lab_a, color=self.theme.primary, scale_factor=1.6), run_time=0.6)
            self.play(Indicate(lab_b, color=self.theme.secondary, scale_factor=1.6), run_time=0.6)
            self.play(Indicate(lab_c, color=self.theme.accent, scale_factor=1.6), run_time=0.6)

        # ---------- 3. 复制四份，围成大正方形 ----------
        with speech(self, "现在，把四个一模一样的三角形，首尾相接地摆成一个大正方形。",
                    spoken="现在，把四个一模一样的三角形，首尾相接地摆成一个大正方形。"):
            quads = assembly_triangles(self)
            self.play(
                LaggedStart(*[TransformFromCopy(template, quad) for quad in quads], lag_ratio=0.35),
                run_time=3.0,
            )
            left_group = VGroup(template, lab_a, lab_b, lab_c)
            self.play(FadeOut(left_group, shift=LEFT * 0.4), run_time=0.7)

        # ---------- 4. 中间空出来的正是 c² ----------
        with speech(self, "中间空出来的这一块，四条边都是斜边 c，所以它是边长 c 的正方形，面积就是 c 的平方。",
                    spoken="中间空出来的这一块，四条边都是斜边 c，所以它是边长 c 的正方形，面积就是 c 的平方。"):
            hole = inner_square(self)
            self.play(FadeIn(hole), run_time=1.0)
            label_c2 = self.make_math("c^2", font_size=46, color=self.theme.accent)
            label_c2.move_to(hole.get_center())
            self.play(Write(label_c2), run_time=0.9)
            self.play(Circumscribe(label_c2, color=self.theme.accent, run_time=0.8))

        # ---------- 5. 面积恒等式 ----------
        with speech(self, "大正方形的边长是 a 加 b，面积就是 a 加 b 的平方；它也等于四个三角形，加上中间的 c 的平方。",
                    spoken="大正方形的边长是 a 加 b，面积就是 a 加 b 的平方；它也等于四个三角形，加上中间的 c 的平方。"):
            equation = self.make_math(r"(a+b)^2 = 4\cdot\frac{1}{2}ab + c^2", font_size=38)
            equation.move_to(np.array([-1.4, -2.35, 0.0]))
            equation.set_color_by_tex("c^2", self.theme.accent)
            self.play(Write(equation), run_time=1.8)
            self.wait(0.3)

        self.finish()
