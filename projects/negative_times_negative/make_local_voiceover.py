"""
离线配音生成器（本机 TTS 兜底方案）。

背景：微软 Edge 的免费朗读端点在本机网络下返回 403（`edge-tts` 任何版本都会被拒），
      因此改用 macOS 自带的 `say`（中文女声 Tingting）离线合成，
      并按 `theme_config.synthesize_speech` 的缓存键名写入 `media/voiceover_cache/`。
      流水线读到缓存后即视为命中，`videoctl build` 就能正常混流，且时间轴用的是真实音频时长。

用法：
    python make_local_voiceover.py            # 生成缺失的句子
    python make_local_voiceover.py --rebuild  # 强制重新生成全部
"""
import argparse
import ast
import hashlib
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
CACHE = PROJECT / "media" / "voiceover_cache"
VOICE_KEY = "zh-CN-YunxiNeural"   # 与各幕的 VOICE_NAME 一致，决定缓存文件名
SAY_VOICE = "Tingting"            # macOS 内置中文女声（zh_CN）


def collect_texts():
    """按分幕顺序抽出每一句真正送进 TTS 的口播文本（spoken 优先，其次 caption）。"""
    items = []
    for script in sorted(PROJECT.glob("scene_*.py")):
        tree = ast.parse(script.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.With):
                continue
            for item in node.items:
                call = item.context_expr
                if not (isinstance(call, ast.Call) and getattr(call.func, "id", "") == "speech"):
                    continue
                if len(call.args) < 2:
                    continue
                spoken = call.args[1]
                for kw in call.keywords:
                    if kw.arg == "spoken":
                        spoken = kw.value
                items.append((script.name, ast.literal_eval(spoken)))
    return items


def cache_path(text):
    digest = hashlib.md5(f"{VOICE_KEY}_{text}".encode("utf-8")).hexdigest()
    return CACHE / f"{digest}.mp3"


def duration_of(path):
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(res.stdout.strip())


def synth(text):
    target = cache_path(text)
    if target.exists() and target.stat().st_size > 0:
        return target, "cache"
    CACHE.mkdir(parents=True, exist_ok=True)
    aiff = target.with_suffix(".aiff")
    subprocess.run(["say", "-v", SAY_VOICE, "-o", str(aiff), text], check=True)
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(aiff), "-codec:a", "libmp3lame", "-q:a", "4", str(target)],
        check=True,
    )
    aiff.unlink(missing_ok=True)
    return target, "new"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true", help="忽略已有缓存，全部重新合成")
    args = parser.parse_args()

    if args.rebuild:
        for _name, text in collect_texts():
            cache_path(text).unlink(missing_ok=True)

    total, made = 0.0, 0
    for name, text in collect_texts():
        path, source = synth(text)
        seconds = duration_of(path)
        total += seconds
        made += source == "new"
        print(f"[{source:5s}] {seconds:5.2f}s  {name:22s} {text}")
    print(f"\n共 {len(collect_texts())} 句，新合成 {made} 句，语音总时长 {total:.1f}s")
    print(f"缓存目录：{CACHE}")


if __name__ == "__main__":
    sys.exit(main())
