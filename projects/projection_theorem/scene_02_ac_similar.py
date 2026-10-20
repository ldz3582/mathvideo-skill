"""
Scene 02：AC² = AD·AB —— △ACD ∽ △ABC（公共角 + 直角 → 相似比 → 交叉相乘）。
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
    RIGHT_PANEL_X,
    angle_arc,
    static_figure,
    sub_triangle,
)


class Scene02AcSimilar(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        th = self.theme

        fig, parts = static_figure(self)

        # ---------- 1. 拎出 △ACD ----------
        with speech(
            self,
            "先看三角形 ACD，它和三角形 ABC 有什么关系？",
            spoken="先看三角形 A C D，它和三角形 A B C 有什么关系？",
        ):
            self.add(fig)
            self.play_show_title("第一步 · 直角边 AC", "△ACD ∽ △ABC")
            acd = sub_triangle(self, "acd")
            self.play(FadeIn(acd), run_time=1.0)
            self.play(Indicate(acd, color=th.primary, scale_factor=1.02), run_time=0.8)

        # ---------- 2. 公共角 + 两个直角 ----------
        with speech(
            self,
            "角 A 是公共角，角 ADC 与角 ACB 都是直角。",
            spoken="角 A 是公共角，角 A D C 与角 A C B 都是直角。",
        ):
            arc = angle_arc(A_PT, B_PT, C_PT, radius=0.62, color=th.success)
            self.play(Create(arc), run_time=0.7)
            self.play(
                ShowPassingFlash(parts["ra_c"].copy().set_stroke(color=th.success, width=5), time_width=0.8),
                ShowPassingFlash(parts["ra_d"].copy().set_stroke(color=th.success, width=5), time_width=0.8),
                run_time=1.0,
            )

        # ---------- 3. 相似判定 ----------
        sim = self.make_math(r"\triangle ACD \sim \triangle ABC", font_size=38)
        sim.move_to(np.array([RIGHT_PANEL_X, 1.35, 0.0]))
        with speech(
            self,
            "两角对应相等，所以 △ACD ∽ △ABC。",
            spoken="两角对应相等，所以三角形 A C D 与三角形 A B C 相似。",
        ):
            self.play(Write(sim), run_time=1.3)
            self.play(Circumscribe(sim, color=th.success, run_time=0.9))

        # ---------- 4. 对应边成比例 ----------
        ratio = self.make_math(r"\frac{AC}{AB} = \frac{AD}{AC}", font_size=44)
        ratio.move_to(np.array([RIGHT_PANEL_X, 0.35, 0.0]))
        with speech(
            self,
            "对应边成比例：AC 比 AB 等于 AD 比 AC。",
            spoken="对应边成比例：A C 比 A B 等于 A D 比 A C。",
        ):
            self.play(Write(ratio), run_time=1.5)

        # ---------- 5. 交叉相乘得结论 ----------
        concl = self.make_math(r"AC^2 = AD \cdot AB", font_size=48, color=th.primary)
        concl.move_to(np.array([RIGHT_PANEL_X, -0.95, 0.0]))
        with speech(
            self,
            "交叉相乘，得到 AC² 等于 AD 乘以 AB。",
            spoken="交叉相乘，得到 A C 的平方等于 A D 乘以 A B。",
        ):
            self.play(Write(concl), run_time=1.4)
            self.focus_on(concl, color=th.primary)

        self.finish()
