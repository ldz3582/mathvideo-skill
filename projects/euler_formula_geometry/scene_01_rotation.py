import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import VideoScene, ClaudeLightTheme, speech


class Scene01Rotation(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        axes = Axes(
            x_range=[-1.5, 1.5, 1], y_range=[-1.35, 1.35, 1],
            x_length=4.4, y_length=4.0,
            axis_config={"color": ClaudeLightTheme.text_muted, "stroke_width": 2, "include_ticks": False},
            tips=True,
        ).shift(LEFT * 2.55 + DOWN * 0.1)
        origin = axes.c2p(0, 0)
        radius = axes.x_axis.unit_size
        circle = Circle(radius=radius, color=ClaudeLightTheme.primary, stroke_width=3).move_to(origin)
        theta = 2 * PI / 5
        end = axes.c2p(np.cos(theta), np.sin(theta))
        vector = Arrow(origin, end, buff=0, color=ClaudeLightTheme.accent, stroke_width=6)
        start_dot = Dot(axes.c2p(1, 0), color=ClaudeLightTheme.secondary)
        one = self.make_math("1", font_size=30, color=ClaudeLightTheme.secondary).next_to(start_dot, DOWN, buff=0.12)
        re_lbl = self.make_text("实轴", font_size=24, color=ClaudeLightTheme.text_muted).next_to(axes.x_axis.get_end(), DOWN, buff=0.1)
        im_lbl = self.make_text("虚轴", font_size=24, color=ClaudeLightTheme.text_muted).next_to(axes.y_axis.get_end(), LEFT, buff=0.1)

        with speech(self, "先别把欧拉公式看成一串符号，把它放进复平面。", spoken="先别把欧拉公式看成一串符号，把它放进复平面。"):
            self.play_show_title("虚数指数，就是旋转", "Complex Exponentials as Rotation")
            self.play(Create(axes), Create(circle), FadeIn(start_dot, one, re_lbl, im_lbl), run_time=1.6)

        arc = Arc(radius=0.62, start_angle=0, angle=theta, arc_center=origin, color=ClaudeLightTheme.secondary)
        theta_lbl = self.make_math(r"\theta", font_size=34, color=ClaudeLightTheme.secondary).next_to(arc, RIGHT, buff=0.1)
        with speech(self, "单位向量逆时针转过 θ，终点的横坐标是 cosθ，纵坐标是 sinθ。", spoken="单位向量逆时针转过西塔，终点的横坐标是余弦西塔，纵坐标是正弦西塔。"):
            self.play(GrowArrow(vector), Create(arc), FadeIn(theta_lbl), run_time=1.8)

        vline = DashedLine(end, axes.c2p(np.cos(theta), 0), color=ClaudeLightTheme.secondary)
        hline = DashedLine(end, axes.c2p(0, np.sin(theta)), color=ClaudeLightTheme.primary)
        x_lbl = self.make_math(r"\cos\theta", font_size=29, color=ClaudeLightTheme.secondary).next_to(axes.c2p(np.cos(theta), 0), DOWN, buff=0.12)
        y_lbl = self.make_math(r"\sin\theta", font_size=29, color=ClaudeLightTheme.primary).next_to(axes.c2p(0, np.sin(theta)), LEFT, buff=0.12)
        point_formula = self.make_math(r"\cos\theta+i\sin\theta", font_size=47)
        point_formula.move_to([2.7, 0.45, 0])
        with speech(self, "复数把横坐标写在实部，把纵坐标乘 i 写在虚部。", spoken="复数把横坐标写在实部，把纵坐标乘虚数单位 i 写在虚部。"):
            self.play(Create(vline), Create(hline), FadeIn(x_lbl, y_lbl), Write(point_formula), run_time=1.8)

        formula = self.make_math(r"e^{i\theta}=\cos\theta+i\sin\theta", font_size=56)
        formula.move_to([2.45, 0.25, 0])
        with speech(self, "所以 e^{iθ} 的几何本质，就是一次角度为 θ 的旋转。", spoken="所以，e 的 i 西塔次方，几何本质就是一次角度为西塔的旋转。"):
            self.play(TransformMatchingTex(point_formula, formula), run_time=1.5)
            self.play(Circumscribe(formula, color=ClaudeLightTheme.accent), run_time=1.0)

        self.finish()
