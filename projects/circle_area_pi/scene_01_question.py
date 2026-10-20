"""Scene 01：提出疑问 —— π 从哪里来？用外切/内接正方形夹住面积。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *

from theme_config import VideoScene, speech
from project_style import ACCENT, INK, MUTED, PRIMARY, RADIUS, SECONDARY


class Scene01Question(VideoScene):
    DEFAULT_THEME = "3b1b_dark"

    def construct(self):
        super().construct()
        r = RADIUS
        center = LEFT * 2.60 + DOWN * 0.15
        right_x = 3.05

        circle = Circle(radius=r, color=PRIMARY, stroke_width=4).move_to(center)
        center_dot = Dot(center, color=ACCENT, radius=0.055)
        radius_line = Line(center, center + RIGHT * r, color=ACCENT, stroke_width=3)
        radius_label = self.make_math("r", font_size=36, color=ACCENT).next_to(radius_line, UP, buff=0.08)

        with speech(
            self,
            "圆的面积是 πr²，这个公式我们背了很多年。",
            spoken="圆的面积是派 r 的平方，这个公式我们背了很多年。",
        ):
            self.play_show_title("圆的面积里，藏着 π", "Where does π come from?")
            self.play(Create(circle), FadeIn(center_dot), run_time=1.3)
            self.play(Create(radius_line), FadeIn(radius_label), run_time=0.8)

        outer = Square(side_length=2 * r, color=SECONDARY, stroke_width=3, stroke_opacity=0.9).move_to(center)
        outer_area = self.make_math("4r^2", font_size=42, color=SECONDARY).move_to([right_x, 1.20, 0])
        outer_name = self.make_text("外切正方形", font_size=21, color=MUTED).next_to(outer_area, DOWN, buff=0.10)

        with speech(
            self,
            "先给圆套一个外切正方形：边长 2r，面积 4r²。",
            spoken="先给圆套一个外切正方形，边长二 r，面积四 r 的平方。",
        ):
            self.play(Create(outer), run_time=1.1)
            self.play(FadeIn(outer_area, shift=LEFT * 0.15), FadeIn(outer_name), run_time=0.7)

        inner = RegularPolygon(4, radius=r, color=ACCENT, stroke_width=3).move_to(center)
        inner_area = self.make_math("2r^2", font_size=42, color=ACCENT).move_to([right_x, 0.10, 0])
        inner_name = self.make_text("内接正方形", font_size=21, color=MUTED).next_to(inner_area, DOWN, buff=0.10)

        with speech(
            self,
            "再塞一个内接正方形：对角线是 2r，面积 2r²。",
            spoken="再塞一个内接正方形，对角线是二 r，面积二 r 的平方。",
        ):
            self.play(Create(inner), run_time=1.1)
            self.play(FadeIn(inner_area, shift=LEFT * 0.15), FadeIn(inner_name), run_time=0.7)

        ineq = self.make_math(r"2r^2 < S < 4r^2", font_size=46).move_to([right_x, -1.15, 0])
        ineq[0][0:5].set_color(ACCENT)
        ineq[0][7:9].set_color(SECONDARY)

        with speech(
            self,
            "于是 2r² 小于 S 小于 4r²，π 确实落在 2 和 4 之间。",
            spoken="于是，二 r 平方小于圆的面积，小于四 r 平方，派确实落在二和四之间。",
        ):
            self.play(Write(ineq), run_time=1.4)
            self.play(Circumscribe(ineq, color=ACCENT, run_time=1.0))

        hint = self.make_text("π ≈ 3.14，就夹在这两条线之间", font_size=22, color=MUTED)
        hint.move_to([right_x, -2.05, 0])

        with speech(
            self,
            "但夹逼只给范围，不给精确值。",
            spoken="但夹逼只给范围，不给精确值。要拿到派 r 平方，得换一把刀。",
        ):
            self.play(FadeIn(hint, shift=UP * 0.12), run_time=0.9)

        self.finish()
