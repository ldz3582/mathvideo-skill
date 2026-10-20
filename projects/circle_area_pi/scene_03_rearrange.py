"""Scene 03：把扇形交错拼成平行四边形 —— 底 = 半个圆周 = πr，高 = r。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *

from theme_config import VideoScene, speech
from project_style import ACCENT, INK, MUTED, RADIUS, circle_fan, fan_arrangement


class Scene03Rearrange(VideoScene):
    DEFAULT_THEME = "3b1b_dark"

    def construct(self):
        super().construct()
        n = 8
        r = RADIUS
        src_center = UP * 0.95
        dst_center = UP * 0.12

        pieces = circle_fan(n, radius=r, center=src_center)
        arranged = fan_arrangement(n, radius=r, center=dst_center)

        self.play(FadeIn(pieces), run_time=0.8)

        with speech(
            self,
            "取一个尖朝下，再取一个翻过来、尖朝上，插进它的缝里。",
            spoken="取一个尖朝下，再取一个翻过来、尖朝上，插进它的缝里。",
        ):
            self.play(
                Transform(pieces[0], arranged[0]),
                Transform(pieces[1], arranged[1]),
                run_time=1.8,
            )

        with speech(
            self,
            "剩下的依次交错，全部拼进去。",
            spoken="剩下的依次交错，全部拼进去。",
        ):
            self.play(
                *[Transform(pieces[k], arranged[k]) for k in range(2, n)],
                lag_ratio=0.14,
                run_time=2.4,
            )

        with speech(
            self,
            "拼出来的是一条波浪边的平行四边形，底边是 8 段小弧。",
            spoken="拼出来的是一条波浪边的平行四边形，底边是八段小弧。",
        ):
            self.wait(0.4)
            self.play(Indicate(pieces, color=ACCENT, scale_factor=1.02), run_time=1.6)

        # 底边 = 半个圆周
        bottom_y = -1.00
        x_left = -2.30
        x_right = 2.30
        bottom_arrow = DoubleArrow(
            [x_left, bottom_y, 0],
            [x_right, bottom_y, 0],
            buff=0,
            color=ACCENT,
            stroke_width=2.4,
            tip_length=0.18,
        )
        bottom_math = self.make_math(r"\pi r", font_size=38, color=ACCENT)
        bottom_text = self.make_text("半个圆周", font_size=22, color=MUTED)
        bottom_text.next_to(bottom_math, RIGHT, buff=0.18)
        bottom_group = VGroup(bottom_math, bottom_text).next_to(bottom_arrow, DOWN, buff=0.16)

        tick_left = Line([x_left, bottom_y - 0.12, 0], [x_left, bottom_y + 0.12, 0], color=ACCENT, stroke_width=2)
        tick_right = Line([x_right, bottom_y - 0.12, 0], [x_right, bottom_y + 0.12, 0], color=ACCENT, stroke_width=2)

        with speech(
            self,
            "八段弧加起来，正好是半个圆周：πr。",
            spoken="八段弧加起来，正好是半个圆周，派 r。",
        ):
            self.play(GrowFromCenter(bottom_arrow), Create(tick_left), Create(tick_right), run_time=0.9)
            self.play(FadeIn(bottom_group, shift=DOWN * 0.1), run_time=0.7)

        # 高 = r
        top_y = 0.93
        right_bar_x = 2.72
        height_arrow = DoubleArrow(
            [right_bar_x, bottom_y + 0.12, 0],
            [right_bar_x, top_y, 0],
            buff=0,
            color=INK,
            stroke_width=2.2,
            tip_length=0.16,
        )
        height_label = self.make_math("r", font_size=36, color=INK).next_to(height_arrow, RIGHT, buff=0.16)

        with speech(
            self,
            "而它的高度，就是半径 r。",
            spoken="而它的高度，就是半径 r。",
        ):
            self.play(GrowFromCenter(height_arrow), FadeIn(height_label), run_time=0.9)

        self.finish()
