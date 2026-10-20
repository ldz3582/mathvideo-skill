"""
Scene 02: 从直角三角形面积公式平滑演化出圆的面积公式 pi*r^2。
主题: claude_light 象牙米纸 ｜ 配音: Microsoft 云希男声 (zh-CN-YunxiNeural)
收尾: 3b1b 式暗场聚光 + 极简地平线。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import (  # 工作台基础设施（自动同步，勿改）
    ClaudeLightScene,
    ClaudeLightTheme,
    speech,
    export_timeline,
)
from project_style import (  # 本项目专属几何装置
    build_bars,
    build_triangle_outline,
    build_triangle_labels,
)

TIMELINE_FILE = Path(__file__).resolve().parent / "voiceover_timeline_Scene02Formula.json"


class Scene02Formula(ClaudeLightScene):
    DEFAULT_THEME = "claude_light"
    ENABLE_VOICEOVER = True
    VOICE_NAME = "zh-CN-YunxiNeural"

    def construct(self):
        super().construct()

        # ---------- 1. 重现直角三角形 ----------
        bars = build_bars()
        tri = build_triangle_outline()
        lbl_base, lbl_h = build_triangle_labels(self)
        geo = VGroup(bars, tri, lbl_base, lbl_h)

        with speech(self, "刚才那个直角三角形，和圆拥有完全相同的面积。"):
            self.play_show_title("从三角形到 πr²", "From Triangle to πr²")
            self.play(FadeIn(bars), Create(tri), FadeIn(lbl_base), FadeIn(lbl_h), run_time=1.4)

        # ---------- 2. 三角形面积公式 ----------
        f1 = self.make_math(r"A = \frac{1}{2} \times b \times h", font_size=62)
        self.colorize_formula(f1, {
            "b": ClaudeLightTheme.secondary,
            "h": ClaudeLightTheme.primary,
        })
        f1.move_to([0.0, 0.95, 0.0])

        with speech(self, "三角形的面积公式是：二分之一，乘以底，再乘以高。"):
            self.play(Write(f1), run_time=1.4)

        # ---------- 3. 底与高的几何对应 ----------
        f2 = self.make_math(r"A = \frac{1}{2} \times 2\pi r \times r", font_size=62)
        self.colorize_formula(f2, {
            r"\pi": ClaudeLightTheme.secondary,
            "r": ClaudeLightTheme.primary,
        })
        f2.move_to(f1.get_center())

        with speech(
            self,
            "这里的底是 2πr，高是 r。",
            spoken="在这里，底就是最外圈拉直后的长度二派 r，高就是圆的半径 r。",
        ):
            self.play(
                Indicate(lbl_base, color=ClaudeLightTheme.secondary, scale_factor=1.35),
                Indicate(lbl_h, color=ClaudeLightTheme.primary, scale_factor=1.35),
                run_time=1.8,
            )
            self.stepwise_tex_transform(f1, f2, run_time=1.8)

        # ---------- 4. 约分演化出 πr² ----------
        f3 = self.make_math(r"A = \pi r^2", font_size=92)
        self.colorize_formula(f3, {
            r"\pi": ClaudeLightTheme.accent,
            "r": ClaudeLightTheme.secondary,
        })
        f3.move_to(f2.get_center())

        with speech(
            self,
            "约掉一个 r，只剩下 π 乘以 r 的平方。",
            spoken="约掉一个 r，二分之一乘以二等于一，于是只剩下派乘以 r 的平方。",
        ):
            self.stepwise_tex_transform(f2, f3, run_time=1.8)

        # ---------- 5. Aha! 暗场聚光 ----------
        with speech(
            self,
            "所以，圆的面积就是 π 乘以半径的平方。",
            spoken="所以，圆的面积，就是派乘以半径的平方。",
        ):
            self.play_focus_revelation(
                f3,
                accent_color=ClaudeLightTheme.accent,
                surround_mobjects_to_dim=[bars, tri, lbl_base, lbl_h],
            )

        # ---------- 6. 收尾：圆与公式并置 ----------
        self.clear_caption()
        self.play(
            FadeOut(geo),
            f3.animate.move_to([2.55, 0.45, 0.0]).scale(0.72),
            run_time=1.0,
        )

        final_circle = Circle(radius=1.15, color=ClaudeLightTheme.primary, stroke_width=3).move_to([-3.3, 0.45, 0])
        final_disk = Circle(radius=1.15, color=ClaudeLightTheme.primary, fill_opacity=0.10, stroke_width=0).move_to([-3.3, 0.45, 0])
        final_radius = Line([-3.3, 0.45, 0], [-3.3 + 1.15, 0.45, 0], color=ClaudeLightTheme.secondary, stroke_width=3)
        final_lbl_r = self.make_math("r", font_size=34, color=ClaudeLightTheme.secondary)
        final_lbl_r.next_to(final_radius, UP, buff=0.12)

        with speech(
            self,
            "半径为 r 的圆，面积就是 πr²。",
            spoken="半径为 r 的圆，面积就是派 r 的平方。",
        ):
            self.play(
                Create(final_circle), FadeIn(final_disk),
                GrowFromCenter(final_radius), FadeIn(final_lbl_r),
                run_time=1.2,
            )
            horizon = self.add_sleek_horizon(f3, accent_color=ClaudeLightTheme.accent)
            horizon.scale(0.82, about_point=horizon.get_center())

        export_timeline(self, TIMELINE_FILE)
