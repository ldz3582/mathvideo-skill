"""
Scene 05：实战 —— 斜边上的高把斜边分成 2 和 8，求这条高；顺便验算勾股定理。
按真实比例作图（缩放系数 0.475），所以图与数据自洽。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *

from theme_config import VideoScene, speech

from project_style import RIGHT_PANEL_X, custom_geometry, draw_geometry, fit

SCALE = 0.475  # 2 → 0.95，8 → 3.80，4 → 1.90（真实比例）


class Scene05Example(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        th = self.theme

        geo = custom_geometry(2 * SCALE, 8 * SCALE, left_x=-5.15, base_y=-1.35)
        A, B, C, D = geo["A"], geo["B"], geo["C"], geo["D"]

        # ---------- 1. 出题 ----------
        with speech(
            self,
            "来一道题：斜边上的高把斜边分成 2 和 8，求这条高。",
            spoken="来一道题：斜边上的高把斜边分成 二 和 八，求这条高。",
        ):
            self.play_show_title("实战一下", "已知两段射影，求斜边上的高")
            figure, _ = draw_geometry(self, geo)
            self.play(Create(figure), run_time=1.5)

            lab_ad = self.make_math("2", font_size=32, color=th.primary)
            lab_ad.move_to((A + D) / 2 + np.array([0.0, -0.42, 0.0]))
            lab_db = self.make_math("8", font_size=32, color=th.secondary)
            lab_db.move_to((D + B) / 2 + np.array([0.0, -0.42, 0.0]))
            lab_cd = self.make_math("?", font_size=32, color=th.accent)
            lab_cd.move_to((C + D) / 2 + np.array([0.40, 0.0, 0.0]))
            self.play(FadeIn(VGroup(lab_ad, lab_db, lab_cd), shift=UP * 0.12), run_time=0.8)

        # ---------- 2. 套公式 ----------
        step1 = self.make_math(r"CD^2 = 2 \times 8 = 16", font_size=44, color=th.accent)
        step1.move_to(np.array([RIGHT_PANEL_X, 0.55, 0.0]))
        with speech(
            self,
            "直接用高的公式：CD² 等于 2 乘 8，等于 16。",
            spoken="直接用高的公式：C D 的平方等于 二 乘 八，等于 十六。",
        ):
            self.play(Write(step1), run_time=1.6)

        # ---------- 3. 答案 ----------
        answer = self.make_math(r"CD = 4", font_size=52, color=th.accent)
        answer.move_to(np.array([RIGHT_PANEL_X, -0.70, 0.0]))
        with speech(
            self,
            "所以这条高等于 4。",
            spoken="所以这条高等于 四。",
        ):
            self.play(Write(answer), run_time=1.0)
            self.focus_on(answer, color=th.accent)
            self.play(ReplacementTransform(lab_cd, self.make_math("4", font_size=32, color=th.accent).move_to(lab_cd)), run_time=0.6)
        # ---------- 4. 验算勾股 ----------
        check = self.make_math(r"AC^2 + BC^2 = 20 + 80 = 100 = 10^2", font_size=32, color=th.success)
        fit(check, 5.2)
        check.move_to(np.array([RIGHT_PANEL_X, -1.85, 0.0]))
        with speech(
            self,
            "顺便验算：两条直角边的平方和是 20 加 80，正好等于 10 的平方。",
            spoken="顺便验算：两条直角边的平方和是 二十 加 八十，正好等于 十 的平方。",
        ):
            self.play(Write(check), run_time=1.8)
            self.play(Circumscribe(check, color=th.success, run_time=0.9))

        self.finish()
