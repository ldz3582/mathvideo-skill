"""Scene 04：份数 8 → 32 → 128 → ∞，锯齿消失，平行四边形拉直成矩形。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *

from theme_config import VideoScene, speech
from project_style import ACCENT, INK, MUTED, RADIUS, SUCCESS, fan_arrangement


class Scene04Limit(VideoScene):
    DEFAULT_THEME = "3b1b_dark"

    def construct(self):
        super().construct()
        r = RADIUS
        center = UP * 0.12

        arranged_8 = fan_arrangement(8, radius=r, center=center)
        arranged_32 = fan_arrangement(32, radius=r, center=center)
        arranged_128 = fan_arrangement(128, radius=r, center=center)

        counter = self.make_math("n = 8", font_size=40, color=ACCENT).move_to([4.85, 2.05, 0])

        self.add(arranged_8, counter)
        self.wait(0.3)

        with speech(
            self,
            "但它还只是近似，因为边是波浪的。",
            spoken="但它还只是近似，因为边是波浪的。",
        ):
            self.play(Circumscribe(arranged_8, color=ACCENT, buff=0.12), run_time=1.2)

        with speech(
            self,
            "把份数从 8 提高到 32。",
            spoken="把份数从八提高到三十二。",
        ):
            new_counter = self.make_math("n = 32", font_size=40, color=ACCENT).move_to(counter)
            self.play(
                FadeOut(arranged_8, scale=0.97),
                FadeIn(arranged_32, scale=1.03),
                ReplacementTransform(counter, new_counter),
                run_time=1.3,
            )
            counter = new_counter

        with speech(
            self,
            "再加到 128，锯齿肉眼几乎看不见了。",
            spoken="再加到一百二十八，锯齿肉眼几乎看不见了。",
        ):
            new_counter = self.make_math("n = 128", font_size=40, color=ACCENT).move_to(counter)
            self.play(
                FadeOut(arranged_32, scale=0.97),
                FadeIn(arranged_128, scale=1.03),
                ReplacementTransform(counter, new_counter),
                run_time=1.3,
            )
            counter = new_counter

        outline = Rectangle(
            width=PI * r,
            height=r,
            color=SUCCESS,
            stroke_width=2.5,
            stroke_opacity=0.9,
        ).move_to(center)
        inf_counter = self.make_math(r"n \to \infty", font_size=40, color=SUCCESS).move_to(counter)

        with speech(
            self,
            "份数趋于无穷时，每一段弧都趋近于直线，平行四边形变成了矩形。",
            spoken="份数趋于无穷时，每一段弧都趋近于直线，平行四边形变成了完美的矩形。",
        ):
            self.play(ReplacementTransform(counter, inf_counter), run_time=0.9)
            self.play(Create(outline), run_time=1.4)
            self.play(Circumscribe(outline, color=SUCCESS, buff=0.15), run_time=1.2)

        keep = self.make_text("面积从头到尾没有变过", font_size=24, color=MUTED)
        keep.move_to([0.0, -1.55, 0])

        with speech(
            self,
            "而我们只是搬动拼图，面积从头到尾没有变过。",
            spoken="而我们只是搬动拼图，面积从头到尾没有变过。",
        ):
            self.play(FadeIn(keep, shift=UP * 0.1), run_time=0.9)

        self.finish()
