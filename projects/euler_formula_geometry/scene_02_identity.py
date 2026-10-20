import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import VideoScene, ClaudeLightTheme, speech


class Scene02Identity(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        axes = Axes(
            x_range=[-1.5, 1.5, 1], y_range=[-1.3, 1.3, 1],
            x_length=4.2, y_length=3.7,
            axis_config={"color": ClaudeLightTheme.text_muted, "stroke_width": 2, "include_ticks": False},
            tips=True,
        ).shift(LEFT * 2.65 + DOWN * 0.1)
        origin = axes.c2p(0, 0)
        radius = axes.x_axis.unit_size
        circle = Circle(radius=radius, color=ClaudeLightTheme.primary, stroke_width=3).move_to(origin)
        tracker = ValueTracker(0)
        arrow = always_redraw(lambda: Arrow(
            origin,
            axes.c2p(np.cos(tracker.get_value()), np.sin(tracker.get_value())),
            buff=0, color=ClaudeLightTheme.accent, stroke_width=6,
        ))
        moving_dot = always_redraw(lambda: Dot(
            axes.c2p(np.cos(tracker.get_value()), np.sin(tracker.get_value())),
            color=ClaudeLightTheme.accent,
        ))
        one = self.make_math("1", font_size=30, color=ClaudeLightTheme.secondary).next_to(axes.c2p(1, 0), DOWN, buff=0.12)
        minus_one = self.make_math("-1", font_size=30, color=ClaudeLightTheme.accent).next_to(axes.c2p(-1, 0), DOWN, buff=0.12)

        with speech(self, "现在令 θ 等于 π，也就是让单位向量恰好旋转半圈。", spoken="现在令西塔等于派，也就是让单位向量恰好旋转半圈。"):
            self.play_show_title("转半圈，答案就出来了", "A Half-turn Reveals the Identity")
            self.play(Create(axes), Create(circle), FadeIn(one, minus_one, arrow, moving_dot), run_time=1.3)
            self.play(tracker.animate.set_value(PI), run_time=2.8, rate_func=smooth)

        coord = self.make_math(r"(-1,\,0)", font_size=46, color=ClaudeLightTheme.accent).move_to([2.5, 1.25, 0])
        with speech(self, "向量从 1 来到 −1：横坐标是 −1，纵坐标是 0。", spoken="向量从一来到负一，横坐标是负一，纵坐标是零。"):
            self.play(Indicate(minus_one, color=ClaudeLightTheme.accent), Write(coord), run_time=1.4)

        formula = self.make_math(r"e^{i\pi}=\cos\pi+i\sin\pi=-1", font_size=48)
        formula.move_to([2.45, 0.15, 0])
        with speech(self, "代入欧拉公式，就得到 e^{iπ}=−1。", spoken="代入欧拉公式，就得到 e 的 i 派次方等于负一。"):
            self.play(Write(formula), run_time=1.8)

        identity = self.make_math(r"e^{i\pi}+1=0", font_size=88)
        identity.move_to([1.7, 0.2, 0])
        with speech(self, "移项便是欧拉恒等式；它不是巧合，而是一场半圈旋转。", spoken="移项便是欧拉恒等式。它不是巧合，而是一场半圈旋转。"):
            self.play(FadeOut(coord), TransformMatchingTex(formula, identity), run_time=1.8)
            self.play(FadeOut(VGroup(axes, circle, arrow, moving_dot, one, minus_one)), identity.animate.move_to(ORIGIN), run_time=1.2)
            self.play(Circumscribe(identity, color=ClaudeLightTheme.accent), run_time=1.0)

        self.finish()
