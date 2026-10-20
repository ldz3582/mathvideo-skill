"""
Scene 04：两次算法相减 —— 公共的四个三角形被同时去掉，剩下的必然相等。

结论：c² = a² + b²，并补上 3-4-5 的数值验证。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *  # noqa: F401,F403
from theme_config import VideoScene, speech

COMMON_TEX = r"4\times\frac{1}{2}ab"


class Scene04Conclude(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()

        # ---------- 1. 两条面积恒等式并排 ----------
        with speech(self, "把两次的算法并排放在一起：两次都有一块 4·½ab，其余分别多出 c² 与 a² + b²。",
                    spoken="把两次的算法，并排放在一起。两次的面积里，都有一块 四乘二分之一 ab，"
                           "其余的，分别多出一个 c 的平方，和一个 a 的平方加 b 的平方。"):
            eq_top = self.make_math(r"(a+b)^2=" + COMMON_TEX + r"+c^2", font_size=44)
            eq_bot = self.make_math(r"(a+b)^2=" + COMMON_TEX + r"+a^2+b^2", font_size=44)
            for eq in (eq_top, eq_bot):
                eq.set_color_by_tex("c^2", self.theme.accent)
                eq.set_color_by_tex("a^2", self.theme.primary)
                eq.set_color_by_tex("b^2", self.theme.secondary)
                eq.set_color_by_tex(COMMON_TEX, self.theme.text_muted)
                eq.scale_to_fit_width(9.2)
                eq.move_to(np.array([-4.5, 0.0, 0.0]), aligned_edge=LEFT)

            eq_top.move_to(np.array([0.0, 1.30, 0.0]), aligned_edge=LEFT).align_to(
                np.array([-4.5, 0.0, 0.0]), LEFT)
            eq_bot.move_to(np.array([0.0, 0.40, 0.0]), aligned_edge=LEFT).align_to(
                np.array([-4.5, 0.0, 0.0]), LEFT)

            self.play(Write(eq_top), run_time=1.6)
            self.play(Write(eq_bot), run_time=1.6)

            box_top = SurroundingRectangle(eq_top.get_part_by_tex(COMMON_TEX),
                                           color=self.theme.accent, buff=0.08,
                                           stroke_width=2.5, corner_radius=0.08)
            box_bot = SurroundingRectangle(eq_bot.get_part_by_tex(COMMON_TEX),
                                           color=self.theme.accent, buff=0.08,
                                           stroke_width=2.5, corner_radius=0.08)
            self.play(Create(box_top), Create(box_bot), run_time=1.0)
            self.wait(0.3)

        # ---------- 2. 公共项同时划掉 ----------
        with speech(self, "同一块大正方形，去掉同样四个三角形，剩下的面积必须相等。",
                    spoken="同一块大正方形，去掉同样的四个三角形，剩下的面积，必然相等。"):
            strikes = VGroup(
                Line(eq_top.get_part_by_tex(COMMON_TEX).get_left() + LEFT * 0.06,
                     eq_top.get_part_by_tex(COMMON_TEX).get_right() + RIGHT * 0.06,
                     color=self.theme.alert, stroke_width=5),
                Line(eq_bot.get_part_by_tex(COMMON_TEX).get_left() + LEFT * 0.06,
                     eq_bot.get_part_by_tex(COMMON_TEX).get_right() + RIGHT * 0.06,
                     color=self.theme.alert, stroke_width=5),
            )
            self.play(FadeOut(box_top), FadeOut(box_bot), run_time=0.4)
            self.play(Create(strikes[0]), run_time=0.8)
            self.play(Create(strikes[1]), run_time=0.8)
            self.play(FadeOut(VGroup(eq_top, eq_bot, strikes), shift=UP * 0.5), run_time=1.1)

        # ---------- 3. 结论 ----------
        final = self.make_math(r"c^2=a^2+b^2", font_size=96)
        final.set_color_by_tex("c^2", self.theme.accent)
        final.set_color_by_tex("a^2", self.theme.primary)
        final.set_color_by_tex("b^2", self.theme.secondary)
        final.scale_to_fit_width(7.4)
        final.move_to(np.array([0.0, 0.75, 0.0]))

        with speech(self, "所以，c² 就等于 a² 加上 b²。",
                    spoken="所以，c 的平方，就等于 a 的平方，加上 b 的平方。"):
            self.play(Write(final), run_time=1.8)
            self.play_focus_revelation(final, accent_color=self.theme.accent, run_time=1.6)
            self.wait(0.4)

        # ---------- 4. 3-4-5 数值验证 ----------
        with speech(self, "比如三、四、五：3² + 4² = 9 + 16 = 25，正好是 5²。",
                    spoken="比如我们最熟悉的三、四、五。三的平方加四的平方，等于九加十六，"
                           "正好是二十五，也就是五的平方。"):
            numbers = self.make_math(r"3^2+4^2=9+16=25=5^2", font_size=42)
            numbers.set_color_by_tex("3^2", self.theme.primary)
            numbers.set_color_by_tex("4^2", self.theme.secondary)
            numbers.set_color_by_tex("5^2", self.theme.accent)
            numbers.set_color_by_tex("9+16", self.theme.text_main)
            numbers.scale_to_fit_width(8.6)
            numbers.move_to(np.array([0.0, -0.85, 0.0]))
            self.play(Write(numbers), run_time=1.8)
            self.wait(0.4)

        self.finish()
