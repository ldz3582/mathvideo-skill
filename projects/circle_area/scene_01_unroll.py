"""
Scene 01: 把圆切成同心圆环，再逐条拉直、堆叠成一个直角三角形。
主题: claude_light 象牙米纸 ｜ 配音: Microsoft 云希男声 (zh-CN-YunxiNeural)
运镜: 推镜特写圆环剖面 -> 广角拉回看堆叠成形。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import *
from theme_config import (  # 工作台基础设施（自动同步，勿改）
    MovingCameraMathScene,
    ClaudeLightTheme,
    speech,
    export_timeline,
)
from project_style import (  # 本项目专属几何装置
    R_CIRCLE,
    CIRCLE_CENTER,
    build_rings,
    build_bars,
    build_triangle_outline,
    build_triangle_labels,
)

TIMELINE_FILE = Path(__file__).resolve().parent / "voiceover_timeline_Scene01Unroll.json"


class Scene01Unroll(MovingCameraMathScene):
    DEFAULT_THEME = "claude_light"
    ENABLE_VOICEOVER = True
    VOICE_NAME = "zh-CN-YunxiNeural"

    def construct(self):
        super().construct()

        # ---------- 1. 开场：一个半径为 r 的圆 ----------
        with speech(self, "一个半径为 r 的圆，它的面积，究竟藏在哪里？"):
            self.play_show_title("圆的面积为什么是 πr² ？", "Unrolling the Circle")

            circle = Circle(radius=R_CIRCLE, color=ClaudeLightTheme.primary, stroke_width=3.5).move_to(CIRCLE_CENTER)
            disk = Circle(radius=R_CIRCLE, color=ClaudeLightTheme.primary, fill_opacity=0.10, stroke_width=0).move_to(CIRCLE_CENTER)
            radius_line = Line(CIRCLE_CENTER, CIRCLE_CENTER + RIGHT * R_CIRCLE, color=ClaudeLightTheme.secondary, stroke_width=3)
            lbl_r = self.make_math("r", font_size=36, color=ClaudeLightTheme.secondary)
            lbl_r.next_to(radius_line, UP, buff=0.14)

            self.play(Create(circle), FadeIn(disk), run_time=1.0)
            self.play(GrowFromCenter(radius_line), FadeIn(lbl_r), run_time=0.8)

        # ---------- 2. 推镜特写：切成极细同心圆环 ----------
        self.clear_caption()
        self.play(FadeOut(self.title_mobject, shift=UP * 0.2), run_time=0.5)
        self.camera_zoom_to(VGroup(circle, disk), scale_factor=0.62, buff=1.0, run_time=1.4)

        rings = build_rings()
        with speech(self, "把它切成无数个极细的同心圆环。"):
            self.play(
                FadeOut(disk, run_time=0.8),
                LaggedStart(*[FadeIn(r, scale=1.02) for r in rings], lag_ratio=0.05),
                run_time=1.5,
            )
            self.bring_to_front(radius_line, lbl_r)

        # ---------- 3. 广角拉回：把每一圈圆环拉直成长条 ----------
        self.clear_caption()
        self.camera_reset(run_time=1.4)
        self.play(FadeIn(self.title_mobject, shift=DOWN * 0.2), run_time=0.5)

        bars = build_bars()
        unroll = [
            AnimationGroup(
                FadeOut(ring, run_time=1.0),
                GrowFromEdge(bar, LEFT, run_time=1.0),
            )
            for ring, bar in zip(rings, bars)
        ]
        with speech(self, "每一圈被拉直之后，都是一条细长的直条，越靠外越长。"):
            self.play(
                LaggedStart(*unroll, lag_ratio=0.12),
                FadeOut(circle, run_time=1.4),
                FadeOut(radius_line, run_time=1.4),
                FadeOut(lbl_r, run_time=1.4),
                run_time=4.2,
            )

        # ---------- 4. 由短到长堆叠成直角三角形 ----------
        tri = build_triangle_outline()
        lbl_base, lbl_h = build_triangle_labels(self)

        with speech(self, "把它们由短到长堆叠起来，恰好拼成一个直角三角形。"):
            self.play(
                Create(tri),
                FadeIn(lbl_base, shift=UP * 0.2),
                FadeIn(lbl_h, shift=RIGHT * 0.2),
                run_time=1.6,
            )

        with speech(
            self,
            "底就是圆的周长 2πr，高就是圆的半径 r。",
            spoken="底就是圆的周长二派 r，高就是圆的半径 r。",
        ):
            self.focus_on(lbl_base, color=ClaudeLightTheme.secondary, scale_factor=1.12)
            self.focus_on(lbl_h, color=ClaudeLightTheme.primary, scale_factor=1.12)

        export_timeline(self, TIMELINE_FILE)
