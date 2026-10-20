"""
Scene 01：命题的具象化 —— 直角三角形的三条边上各作一个正方形。

画面：标题 + 直角三角形（标注 a、b、c）→ 两直角边上的正方形 a²、b²
      → 斜边上的正方形 c² → 右侧写出结论 a² + b² = c²。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *  # noqa: F401,F403
from theme_config import VideoScene, speech

from project_style import (
    A_LEG,
    B_LEG,
    SIDE,
    s1,
    s1_hyp_mid,
    s1_hyp_normal,
    s1_poly,
)


class Scene01Statement(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()

        # ---------- 标题 ----------
        title = self.make_text("勾股定理", font_size=40)
        subtitle = self.make_text("一条直角边、两条直角边与斜边的故事", font_size=20,
                                  color=self.theme.text_muted)
        header = VGroup(title, subtitle).arrange(DOWN, buff=0.14).to_edge(UP, buff=0.30)

        # ---------- 1. 直角三角形与三边标注 ----------
        with speech(self, "先看一个直角三角形：两条直角边分别长 a 和 b，斜边长 c。",
                    spoken="先看一个直角三角形。两条直角边，分别长 a 和 b，斜边长 c。"):
            self.play(FadeIn(header, shift=DOWN * 0.2), run_time=0.9)

            tri = s1_poly(self, [(0, 0), (A_LEG, 0), (0, B_LEG)],
                          fill_opacity=0.12, color=self.theme.text_main, stroke_width=3.2)
            right_angle = s1_poly(self, [(0.26, 0), (0.26, 0.26), (0, 0.26)],
                                  fill_opacity=0.0, color=self.theme.text_muted, stroke_width=2.0)

            lab_a = self.make_math("a", font_size=34, color=self.theme.primary)
            lab_a.move_to(s1(A_LEG / 2.0, 0) + DOWN * 0.26)
            lab_b = self.make_math("b", font_size=34, color=self.theme.secondary)
            lab_b.move_to(s1(0, B_LEG / 2.0) + LEFT * 0.26)
            lab_c = self.make_math("c", font_size=34, color=self.theme.accent)
            lab_c.move_to(s1_hyp_mid() + s1_hyp_normal() * 0.32)

            self.play(Create(tri), run_time=1.2)
            self.play(Create(right_angle), run_time=0.5)
            self.play(LaggedStart(FadeIn(lab_a, shift=UP * 0.08),
                                  FadeIn(lab_b, shift=UP * 0.08), lag_ratio=0.45), run_time=1.0)
            self.play(FadeIn(lab_c, shift=s1_hyp_normal() * 0.15), run_time=0.6)

        # ---------- 2. 两条直角边上的正方形 ----------
        with speech(self, "在两条直角边上各作一个正方形，面积就是 a² 和 b²。",
                    spoken="在两条直角边上，各作一个正方形。它们的面积，就是 a 的平方和 b 的平方。"):
            sq_a = s1_poly(self, [(0, 0), (A_LEG, 0), (A_LEG, -A_LEG), (0, -A_LEG)],
                           fill_opacity=0.22, color=self.theme.primary, stroke_width=2.6)
            sq_b = s1_poly(self, [(0, 0), (0, B_LEG), (-B_LEG, B_LEG), (-B_LEG, 0)],
                           fill_opacity=0.22, color=self.theme.secondary, stroke_width=2.6)
            a2 = self.make_math("a^2", font_size=36, color=self.theme.primary)
            a2.move_to(s1(A_LEG / 2.0, -A_LEG / 2.0))
            b2 = self.make_math("b^2", font_size=36, color=self.theme.secondary)
            b2.move_to(s1(-B_LEG / 2.0, B_LEG / 2.0))

            self.play(Create(sq_a), run_time=1.0)
            self.play(Write(a2), run_time=0.7)
            self.play(Create(sq_b), run_time=1.0)
            self.play(Write(b2), run_time=0.7)

        # ---------- 3. 斜边上的正方形 + 结论 ----------
        with speech(self, "在斜边上再作一个正方形，面积是 c²；勾股定理说，a² 加 b² 恰好等于 c²。",
                    spoken="在斜边上，再作一个正方形，面积是 c 的平方。勾股定理说："
                           "a 的平方加上 b 的平方，恰好等于 c 的平方。"):
            sq_c = s1_poly(self, [(0, B_LEG), (A_LEG, 0), (SIDE, A_LEG), (B_LEG, SIDE)],
                           fill_opacity=0.22, color=self.theme.accent, stroke_width=2.6)
            c2 = self.make_math("c^2", font_size=36, color=self.theme.accent)
            c2.move_to(s1(SIDE / 2.0, SIDE / 2.0))
            self.play(Create(sq_c), run_time=1.2)
            self.play(Write(c2), run_time=0.7)

            claim = self.make_math(r"a^2+b^2=c^2", font_size=54)
            claim.set_color_by_tex("a^2", self.theme.primary)
            claim.set_color_by_tex("b^2", self.theme.secondary)
            claim.set_color_by_tex("c^2", self.theme.accent)
            claim.scale_to_fit_width(4.2)
            claim.move_to(np.array([3.05, 0.80, 0.0]))
            horizon = Line(claim.get_corner(DL) + DOWN * 0.22, claim.get_corner(DR) + DOWN * 0.22,
                           color=self.theme.accent, stroke_width=1.6)
            self.play(Write(claim), run_time=1.6)
            self.play(Create(horizon), run_time=0.8)
            self.play(Circumscribe(claim, color=self.theme.accent, run_time=0.9))
            self.wait(0.4)

        # ---------- 4. 过渡到拼图 ----------
        with speech(self, "为什么一定相等？答案藏在一个很简单的拼图里。",
                    spoken="为什么一定相等呢？答案，藏在一个很简单的拼图里。"):
            self.play(FadeOut(VGroup(header, tri, right_angle, lab_a, lab_b, lab_c,
                                     sq_a, sq_b, sq_c, a2, b2, c2, claim, horizon),
                              shift=UP * 0.3),
                      run_time=1.2)

        self.finish()
