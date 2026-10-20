"""Scene 02：像披萨一样把圆切成 n 个扇形 —— 只是分割，面积不变。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *

from theme_config import VideoScene, speech
from project_style import ACCENT, INK, MUTED, RADIUS, circle_fan


class Scene02Slice(VideoScene):
    DEFAULT_THEME = "3b1b_dark"

    def construct(self):
        super().construct()
        n = 8
        r = RADIUS
        center = UP * 0.02
        theta = TAU / n

        outline = Circle(radius=r, color=INK, stroke_width=2.6).move_to(center)
        spokes = VGroup(
            *[
                Line(
                    center,
                    center + r * np.array([np.cos(k * theta), np.sin(k * theta), 0.0]),
                    color=INK,
                    stroke_width=1.5,
                ).set_stroke(opacity=0.55)
                for k in range(n)
            ]
        )
        pieces = circle_fan(n, radius=r, center=center)

        with speech(
            self,
            "第一步，把圆像披萨一样切开。",
            spoken="第一步，把圆像披萨一样切开。",
        ):
            self.play_show_title("切一刀，看看里面是什么", "Slice the circle")
            self.play(Create(outline), run_time=1.0)
            self.play(LaggedStart(*[Create(s) for s in spokes], lag_ratio=0.12), run_time=1.8)

        with speech(
            self,
            "从圆心向圆周均匀切 n 刀，得到 n 个完全相同的扇形。",
            spoken="从圆心向圆周均匀地切 n 刀，得到 n 个完全相同的扇形。",
        ):
            self.play(FadeOut(outline, spokes), FadeIn(pieces), run_time=1.0)

        # 单独高亮 0 号扇形，标出两条直边 = r 与夹角 2π/n
        target = pieces[0]
        target.set_fill(ACCENT, opacity=0.75)
        target.set_stroke(ACCENT, width=3)

        mid_angle = theta / 2
        edge_a = center + r * np.array([1.0, 0.0, 0.0])
        edge_b = center + r * np.array([np.cos(theta), np.sin(theta), 0.0])
        edge_line = Line(center, edge_a, color=INK, stroke_width=3)
        r_label = self.make_math("r", font_size=34, color=INK).move_to(
            center + 0.55 * r * np.array([np.cos(mid_angle - 0.35), np.sin(mid_angle - 0.35), 0.0])
        )
        angle_arc = Arc(
            radius=0.55,
            start_angle=0,
            angle=theta,
            arc_center=center,
            color=ACCENT,
            stroke_width=3,
        )
        angle_label = self.make_math(r"\frac{2\pi}{n}", font_size=30, color=ACCENT).move_to(
            center + 0.92 * np.array([np.cos(mid_angle), np.sin(mid_angle), 0.0])
        )

        with speech(
            self,
            "每个扇形的两条直边都是半径 r，夹角是 2π 除以 n。",
            spoken="每个扇形的两条直边都是半径 r，夹角是二派除以 n。",
        ):
            self.play(FadeIn(edge_line), FadeIn(r_label), run_time=0.8)
            self.play(Create(angle_arc), FadeIn(angle_label), run_time=0.9)

        note = self.make_text("8 块拼图 · 面积守恒", font_size=24, color=MUTED)
        note.to_edge(DOWN, buff=1.05)

        with speech(
            self,
            "切只是分割，总面积一点没变。",
            spoken="切只是分割，总面积一点没变。现在，把这一堆扇形重新摆一摆。",
        ):
            self.play(FadeIn(note, shift=UP * 0.12), run_time=0.8)
            self.play(
                FadeOut(edge_line, r_label, angle_arc, angle_label),
                run_time=0.8,
            )
            target.set_fill(ACCENT, opacity=0.45)
            target.set_stroke(ACCENT, width=1.6)

        self.finish()
