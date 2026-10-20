"""
Scene 03：BC² = BD·AB 与 CD² = AD·BD —— 对称的一条 + 高的那一条，最后三式并列。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from manim import *

from theme_config import VideoScene, speech

from project_style import RIGHT_PANEL_X, fit, static_figure, sub_triangle


class Scene03Height(VideoScene):
    DEFAULT_THEME = "claude_light"

    def construct(self):
        super().construct()
        th = self.theme

        fig, _ = static_figure(self)

        # ---------- 1. △CBD ∽ △ABC ----------
        sim2 = self.make_math(r"\triangle CBD \sim \triangle ABC", font_size=34, color=th.secondary)
        sim2.move_to(np.array([RIGHT_PANEL_X, 1.50, 0.0]))
        with speech(
            self,
            "同样地，右边的三角形 CBD 也与三角形 ABC 相似。",
            spoken="同样地，右边的三角形 C B D 也与大三角形 A B C 相似。",
        ):
            self.add(fig)
            self.play_show_title("第二步 · 另一条直角边", "△CBD ∽ △ABC")
            cbd = sub_triangle(self, "cbd")
            self.play(FadeIn(cbd), run_time=1.0)
            self.play(Write(sim2), run_time=1.1)

        # ---------- 2. BC² = BD·AB ----------
        bc_eq = self.make_math(r"BC^2 = BD \cdot AB", font_size=44, color=th.secondary)
        bc_eq.move_to(np.array([RIGHT_PANEL_X, 0.50, 0.0]))
        with speech(
            self,
            "于是 BC 的平方等于 BD 乘以 AB。",
            spoken="于是 B C 的平方等于 B D 乘以 A B。",
        ):
            self.play(Write(bc_eq), run_time=1.2)
            self.focus_on(bc_eq, color=th.secondary)

        # ---------- 3. 两个小三角形也相似 ----------
        sim3 = self.make_math(r"\triangle ACD \sim \triangle CBD", font_size=34, color=th.accent)
        sim3.move_to(np.array([RIGHT_PANEL_X, 1.50, 0.0]))
        with speech(
            self,
            "再把两个小三角形单独拿出来，它们也互相相似。",
            spoken="再把两个小三角形单独拿出来，它们也互相相似。",
        ):
            self.play(FadeOut(VGroup(sim2, bc_eq, cbd), shift=UP * 0.2), run_time=0.6)
            acd2 = sub_triangle(self, "acd")
            cbd2 = sub_triangle(self, "cbd")
            self.play(FadeIn(acd2), FadeIn(cbd2), run_time=0.9)
            self.play(Write(sim3), run_time=1.1)

        # ---------- 4. 对应边成比例 ----------
        ratio3 = self.make_math(r"\frac{CD}{BD} = \frac{AD}{CD}", font_size=40)
        ratio3.move_to(np.array([RIGHT_PANEL_X, 0.50, 0.0]))
        with speech(
            self,
            "对应边成比例：CD 比 BD 等于 AD 比 CD。",
            spoken="对应边成比例：C D 比 B D 等于 A D 比 C D。",
        ):
            self.play(Write(ratio3), run_time=1.3)

        # ---------- 5. CD² = AD·BD ----------
        cd_eq = self.make_math(r"CD^2 = AD \cdot BD", font_size=46, color=th.accent)
        cd_eq.move_to(np.array([RIGHT_PANEL_X, -0.75, 0.0]))
        with speech(
            self,
            "交叉相乘，斜边上的高的平方，等于两段射影的乘积。",
            spoken="交叉相乘，斜边上的高的平方，等于两段射影的乘积。",
        ):
            self.play(Write(cd_eq), run_time=1.3)
            self.focus_on(cd_eq, color=th.accent)

        # ---------- 6. 三式并列 ----------
        rows = VGroup(
            self.make_math(r"AC^2 = AD \cdot AB", font_size=40, color=th.primary),
            self.make_math(r"BC^2 = BD \cdot AB", font_size=40, color=th.secondary),
            self.make_math(r"CD^2 = AD \cdot BD", font_size=40, color=th.accent),
        ).arrange(DOWN, buff=0.62)
        rows.move_to(np.array([RIGHT_PANEL_X, 0.10, 0.0]))
        with speech(
            self,
            "三式集齐：直角边² = 它的射影 × 斜边，高² = 两段射影之积。",
            spoken="三式集齐：直角边的平方等于它的射影乘以斜边；高的平方等于两段射影之积。",
        ):
            self.play(
                FadeOut(VGroup(sim3, ratio3, cd_eq), shift=LEFT * 0.3),
                FadeOut(VGroup(acd2, cbd2)),
                run_time=0.7,
            )
            self.play(
                LaggedStart(*[Write(r) for r in rows], lag_ratio=0.45),
                run_time=2.4,
            )

        self.finish()
