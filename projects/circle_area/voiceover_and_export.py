"""
圆面积示例：把各幕配音混入画面并无损拼接成最终有声成片。
用法:
    python projects/circle_area/voiceover_and_export.py --quality h
前置条件:
    已用相同画质渲染过两幕（渲染时 ENABLE_VOICEOVER=True 会自动生成配音与时间轴 JSON）。
"""
import argparse
import json
import sys
from pathlib import Path

P_ROOT = Path(__file__).resolve().parent
REPO_ROOT = P_ROOT.parent.parent
sys.path.insert(0, str(REPO_ROOT / "skills" / "manim-video" / "templates"))
sys.path.insert(0, str(REPO_ROOT / "skills" / "manim-video" / "scripts"))

from audio_engine import AudioEngine
from render_manager import stitch_videos

RES_DIR = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}

SCENES = [
    ("scene_01_unroll", "Scene01Unroll", "voiceover_timeline_scene_01.json"),
    ("scene_02_formula", "Scene02Formula", "voiceover_timeline_scene_02.json"),
]


def mix_one(scene_stem, scene_name, timeline_name, quality):
    video = REPO_ROOT / "media" / "videos" / scene_stem / RES_DIR[quality] / f"{scene_name}.mp4"
    timeline = P_ROOT / timeline_name
    if not video.exists():
        raise FileNotFoundError(f"未找到渲染产物: {video}")
    if not timeline.exists():
        raise FileNotFoundError(f"未找到语音时间轴: {timeline}（请先带配音渲染该幕）")

    tracks = json.loads(timeline.read_text(encoding="utf-8"))
    out_dir = P_ROOT / "voiced" / quality
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{scene_name}_voiced.mp4"

    print(f"[Mix] {scene_name}: 混入 {len(tracks)} 段配音 -> {out}")
    ok = AudioEngine.mix_scene_audio(
        video_path=str(video),
        audio_files_with_offsets=[(t["audio"], t["start_time"]) for t in tracks],
        output_path=str(out),
    )
    if not ok:
        raise RuntimeError(f"混音失败: {scene_name}")
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quality", choices=["l", "m", "h", "k"], default="h")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    voiced = [mix_one(stem, name, timeline, args.quality) for stem, name, timeline in SCENES]

    output = Path(args.output) if args.output else P_ROOT / "circle_area_pi_r_squared_voiced.mp4"
    if not stitch_videos([str(p) for p in voiced], str(output)):
        raise RuntimeError("拼接失败")
    print(f"[Done] 有声成片: {output}")


if __name__ == "__main__":
    main()
