# 示例工程：圆的面积为什么是 πr² ？

这是 manim-video 技能的一次完整闭环示范：脚本 → 分镜 → 编码 → 快检 → **配音** → 高清成片。

## 成片

| 文件 | 说明 |
| :--- | :--- |
| `circle_area_pi_r_squared_voiced.mp4` | **有声成片**：1920×1080 / 60fps / 69 秒，微软云希男声解说（zh-CN-YunxiNeural） |
| `circle_area_pi_r_squared.mp4` | 纯净无声版（同一套画面，适合后期自行录音或配乐） |

## 文件说明

| 文件 | 作用 |
| :--- | :--- |
| `script_and_timeline.md` | 第 1 步：时间轴字幕与口播脚本（Rule 0 门控产物） |
| `theme_config.py` | 主题基类 + 中文字体自适应 + 公共几何装置 + `speech()` 语画同步块 |
| `scene_01_unroll.py` | 第 1 幕：圆 → 同心圆环 → 拉直堆叠成直角三角形 |
| `scene_02_formula.py` | 第 2 幕：三角形面积公式 → 逐步演化为 πr² |
| `voiceover_timeline_scene_0*.json` | 渲染时自动落盘的配音时间轴（音频文件 + 起始秒） |
| `voiceover_and_export.py` | 把配音混入各幕画面并拼接成最终有声成片 |
| `voiced/` | 中间产物：各幕的配音版 mp4 |

## 重新渲染

```bash
# 1) 单帧排版快检
python -m manim render -ql -s projects/circle_area/scene_01_unroll.py Scene01Unroll

# 2) 低清预览（带配音）
python -m manim render -ql projects/circle_area/scene_01_unroll.py Scene01Unroll

# 3) 高清渲染（渲染时会自动生成/复用配音，并写出时间轴 JSON）
python skills/manim-video/scripts/render_manager.py --action render --quality h \
  --scenes projects/circle_area/scene_01_unroll.py:Scene01Unroll \
           projects/circle_area/scene_02_formula.py:Scene02Formula

# 4) 混入配音并拼接成有声成片
python projects/circle_area/voiceover_and_export.py --quality h
```

## 配音是怎么对齐的

1. 每一句台词包在 `with speech(self, 字幕文本, spoken=口播文本) as tracker:` 里；
   - `字幕文本` 可以放心写 `2πr`、`πr²` 这类符号，保持排版好看；
   - `spoken` 用纯中文写「二派 r」，避免语音引擎把符号念错。
2. 块结束时自动计算「配音实际时长 − 已播放动画时长」，把差额 `wait` 掉，
   因此每句台词与画面严格锁死，下一句也绝不会压到上一句（实测句间留白 0.5s+）。
3. 渲染过程中 `voiceover_timeline` 会记录每段音频的起始秒，落盘成 JSON；
   `voiceover_and_export.py` 用 `AudioEngine.mix_scene_audio()` 按偏移量 `adelay + amix` 混流，
   各幕分别混音后再无损拼接，保证跨幕时序不漂移。

## 换音色 / 关配音 / 换肤

- **换音色**：把两幕里的 `VOICE_NAME` 改成 `"zh-CN-XiaoxiaoNeural"`（知性女声）、`"zh-CN-YunyangNeural"`（新闻男声）等即可。
- **关闭配音**：把 `ENABLE_VOICEOVER` 改为 `False`，画面节奏会自动按文本长度估算，无需删代码。
- **一键换肤**：把 `DEFAULT_THEME` 改成 `"3b1b_dark"`、`"chalkboard"`、`"nord"` 等，公式与文字颜色自动适配深浅底。

> 注：仓库默认中文字体为 Windows 的 `Microsoft YaHei`，本工程的 `theme_config.py` 会自动降级到本机可用字体（macOS 为 `PingFang SC`）。
