"""
Scene 04：为什么叫「射影」—— 垂直投影扫掠，直角边的影子就是它那段射影；
          两式相加还原出勾股定理。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *

from theme_config import VideoScene, speech

from project_style import (
    A_PT,
    B_PT,
    C_PT,
    D_PT,
    RIGHT_PANEL_X,
    fit,
    projection_sweep,
    static_figure,
)


class Scene04Projection(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        th = self.theme

        fig, _ = static_figure(self)

        # ---------- 1. AC 垂直投影到斜边 ----------
        with speech(
            self,
            "为什么叫射影？想象光垂直照下来，直角边 AC 会在斜边上留下影子。",
            spoken="为什么叫射影？想象光垂直照下来，直角边 A C 会在斜边上留下影子。",
        ):
            self.add(fig)
            self.play_show_title("为什么叫「射影」", "直角边在斜边上的影子")
            t1 = ValueTracker(0.0)
            dashed1, mover1, shadow1 = projection_sweep(self, t1, A_PT, C_PT, th.primary)
            self.add(t1, dashed1, mover1, shadow1)
            self.play(t1.animate.set_value(1.0), run_time=2.8)

        ad = Line(A_PT, D_PT, color=th.primary, stroke_width=8)
        self.remove(t1, dashed1, mover1, shadow1)

        # ---------- 2. AD 就是 AC 的射影 ----------
        with speech(
            self,
            "这一段影子 AD，就叫做 AC 在斜边上的射影。",
            spoken="这一段影子 A D，就叫做 A C 在斜边上的射影。",
        ):
            self.play(Create(ad), run_time=0.7)
            self.focus_on(ad, color=th.primary)

        # ---------- 3. BC 的影子是 BD ----------
        with speech(
            self,
            "同样，直角边 BC 的影子是 BD。",
            spoken="同样，直角边 B C 的影子是 B D。",
        ):
            t2 = ValueTracker(0.0)
            dashed2, mover2, shadow2 = projection_sweep(self, t2, B_PT, C_PT, th.secondary)
            self.add(t2, dashed2, mover2, shadow2)
            self.play(t2.animate.set_value(1.0), run_time=2.2)

        db = Line(D_PT, B_PT, color=th.secondary, stroke_width=8)
        self.remove(t2, dashed2, mover2, shadow2)
        self.play(Create(db), run_time=0.7)

        # ---------- 4. 直角边² = 射影 × 斜边 ----------
        eq1 = self.make_math(r"AC^2 = AD \cdot AB", font_size=42, color=th.primary)
        eq2 = self.make_math(r"BC^2 = BD \cdot AB", font_size=42, color=th.secondary)
        stack = VGroup(eq1, eq2).arrange(DOWN, buff=0.75)
        stack.move_to(np.array([RIGHT_PANEL_X, 0.75, 0.0]))
        with speech(
            self,
            "所以，直角边的平方，等于它的射影乘以整条斜边。",
            spoken="所以，直角边的平方，等于它的射影乘以整条斜边。",
        ):
            self.play(Write(eq1), run_time=1.0)
            self.play(Write(eq2), run_time=1.0)

        # ---------- 5. 两式相加 → 勾股定理 ----------
        chain = self.make_math(r"AC^2 + BC^2 = AB(AD + DB) = AB^2", font_size=32, color=th.success)
        fit(chain, 5.2)
        chain.move_to(np.array([RIGHT_PANEL_X, -1.05, 0.0]))
        with speech(
            self,
            "两式相加，再用上 AD 加 DB 等于 AB，就还原出了勾股定理。",
            spoken="两式相加，再用上 A D 加 D B 等于 A B，就还原出了勾股定理。",
        ):
            self.play(Write(chain), run_time=1.8)

        # ---------- 6. 收尾 ----------
        with speech(
            self,
            "射影定理，其实就是勾股定理的上游。",
            spoken="射影定理，其实就是勾股定理的上游。",
        ):
            self.add_sleek_horizon(chain, accent_color=th.success)
            self.play(Circumscribe(chain, color=th.success, run_time=0.9))

        self.finish()
