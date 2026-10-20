"""
Scene 01：立图设问 —— 直角三角形、斜边上的高，以及被高分开的三条关键线段。
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
    altitude_cd,
    fit,
    legend_row,
    right_angle_mark,
    side_ab,
    side_ac,
    side_bc,
    triangle_fill,
    vertex_labels,
)


class Scene01Setup(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        th = self.theme

        # ---------- 1. 直角三角形 ----------
        with speech(
            self,
            "先画一个直角三角形，直角在顶点 C，斜边是 AB。",
            spoken="先画一个直角三角形，直角在顶点 C，斜边是 A B。",
        ):
            self.play_show_title("射影定理", "直角三角形斜边上的高")
            tri = VGroup(side_ab(self), side_ac(self), side_bc(self))
            self.play(FadeIn(triangle_fill(self)), Create(tri), run_time=1.4)
            self.play(FadeIn(vertex_labels(self)[:3], shift=UP * 0.12), run_time=0.5)
            self.play(Create(right_angle_mark(self, C_PT, A_PT, B_PT, length=0.30)), run_time=0.5)

        # ---------- 2. 斜边上的高 ----------
        with speech(
            self,
            "从直角顶点 C 向斜边作一条垂线，垂足记作 D。",
            spoken="从直角顶点 C 向斜边作一条垂线，垂足记作 D。",
        ):
            cd = altitude_cd(self)
            self.play(Create(cd), run_time=1.0)
            self.play(
                FadeIn(vertex_labels(self)[3], shift=DOWN * 0.12),
                Create(right_angle_mark(self, D_PT, A_PT, C_PT, length=0.22)),
                run_time=0.6,
            )
            self.play(ShowPassingFlash(cd.copy().set_stroke(width=9), time_width=0.55), run_time=0.9)

        # ---------- 3. 两段 + 图例 + 设问 ----------
        with speech(
            self,
            "这条高 CD，把斜边分成了 AD 和 DB 两段，它们之间有什么关系？",
            spoken="这条高 C D，把斜边分成了 A D 和 D B 两段，它们之间有什么关系？",
        ):
            self.play(
                ShowPassingFlash(Line(A_PT, D_PT).set_stroke(color=th.accent, width=9), time_width=0.5),
                ShowPassingFlash(Line(D_PT, B_PT).set_stroke(color=th.accent, width=9), time_width=0.5),
                run_time=1.2,
            )
            legend = VGroup(
                legend_row(self, th.primary, "AC：一条直角边"),
                legend_row(self, th.secondary, "BC：另一条直角边"),
                legend_row(self, th.accent, "CD：斜边上的高"),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.40)
            fit(legend, 5.0)
            legend.move_to(np.array([RIGHT_PANEL_X, 0.30, 0.0]))
            self.play(
                LaggedStart(*[FadeIn(r, shift=RIGHT * 0.25) for r in legend], lag_ratio=0.28),
                run_time=1.6,
            )
            question = fit(
                self.make_text("AD、DB、CD 有什么关系？", font_size=24, color=th.accent), 5.0
            )
            question.next_to(legend, DOWN, buff=0.60)
            self.play(FadeIn(question, shift=UP * 0.15), run_time=0.8)

        self.finish()
