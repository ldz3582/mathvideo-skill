"""Scene 05：矩形 πr × r → S = πr²，收束到「切分 · 重排 · 取极限」。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *

from theme_config import VideoScene, speech
from project_style import ACCENT, INK, MUTED, RADIUS, SUCCESS


class Scene05Conclusion(VideoScene):
    DEFAULT_THEME = "3b1b_dark"

    def construct(self):
        super().construct()
        r = RADIUS
        width = PI * r
        center = UP * 0.85

        rect = Rectangle(
            width=width,
            height=r,
            color=SUCCESS,
            stroke_width=3.5,
            fill_color=SUCCESS,
            fill_opacity=0.10,
        ).move_to(center)

        left_x = center[0] - width / 2
        right_x = center[0] + width / 2
        bottom_y = center[1] - r / 2
        top_y = center[1] + r / 2

        bottom_arrow = DoubleArrow(
            [left_x, bottom_y - 0.30, 0],
            [right_x, bottom_y - 0.30, 0],
            buff=0,
            color=ACCENT,
            stroke_width=2.4,
            tip_length=0.18,
        )
        bottom_label = self.make_math(r"\pi r", font_size=40, color=ACCENT).next_to(bottom_arrow, DOWN, buff=0.14)

        height_arrow = DoubleArrow(
            [right_x + 0.45, bottom_y, 0],
            [right_x + 0.45, top_y, 0],
            buff=0,
            color=ACCENT,
            stroke_width=2.4,
            tip_length=0.18,
        )
        height_label = self.make_math("r", font_size=38, color=ACCENT).next_to(height_arrow, RIGHT, buff=0.14)

        with speech(
            self,
            "矩形宽 πr，高 r。",
            spoken="矩形的宽是派 r，高是 r。",
        ):
            self.play_show_title("重排之后，答案自己浮出来", "Rearrange, then take the limit")
            self.play(Create(rect), run_time=1.2)
            self.play(GrowFromCenter(bottom_arrow), FadeIn(bottom_label), run_time=0.9)
            self.play(GrowFromCenter(height_arrow), FadeIn(height_label), run_time=0.9)

        formula = self.make_math(
            r"S = \pi r \times r = \pi r^{2}",
            font_size=64,
        ).move_to([0.0, -1.30, 0])
        formula[0][0:5].set_color(INK)
        formula[0][-2:].set_color(SUCCESS)

        with speech(
            self,
            "所以圆的面积 S 等于 πr 乘 r，等于 πr²。",
            spoken="所以，圆的面积 S 等于派 r 乘 r，等于派 r 的平方。",
        ):
            self.play(Write(formula), run_time=1.8)
            self.play(Circumscribe(formula, color=ACCENT, buff=0.18, run_time=1.3))

        closing = self.make_text("切分 · 重排 · 取极限", font_size=26, color=MUTED)
        closing.move_to([0.0, -2.45, 0])

        with speech(
            self,
            "我们没有测量任何长度，只是切分、重排，然后让份数趋于无穷。",
            spoken="我们没有测量任何长度，只是切分、重排，然后让份数趋于无穷。",
        ):
            self.play(FadeIn(closing, shift=UP * 0.1), run_time=1.0)
            self.play(Indicate(formula, color=ACCENT, scale_factor=1.04), run_time=1.2)

        self.finish()
