#!/usr/bin/env python3
"""
简化的视频处理工具 - 常用功能集合
"""

import os
import subprocess
import sys
from pathlib import Path

FFMPEG = r"C:\Users\WUccc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
FFPROBE = r"C:\Users\WUccc\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffprobe.exe"

def run(cmd, capture=True):
    """运行命令"""
    print(f"🔧 运行: {' '.join(cmd[:3])}...")
    result = subprocess.run(cmd, capture_output=capture, text=True)
    if result.returncode != 0 and capture:
        print(f"⚠️ 警告: {result.stderr[:200]}")
    return result

def get_video_info(video_path):
    """获取视频信息"""
    cmd = [FFPROBE, "-v", "quiet", "-print_format", "json", "-show_format", video_path]
    result = run(cmd)
    import json
    info = json.loads(result.stdout)
    return {
        'duration': float(info['format'].get('duration', 0)),
        'size': int(info['format'].get('size', 0))
    }

def split_video(video_path, duration_min=10, output_dir=None):
    """分割视频"""
    info = get_video_info(video_path)
    duration = info['duration']
    output_dir = Path(output_dir) or Path(video_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    segments = []
    start = 0
    idx = 1
    while start < duration:
        end = min(start + duration_min*60, duration)
        output = output_dir / f"part_{idx:02d}.mp4"
        
        cmd = [FFMPEG, "-y", "-i", video_path, "-ss", str(start), "-to", str(end), "-c", "copy", str(output)]
        run(cmd)
        
        segments.append(str(output))
        print(f"✅ 分段 {idx}: {output.name}")
        start = end
        idx += 1
    
    return segments

def enhance_video(video_path, output_path=None):
    """增强视频质量 - 降噪+调色"""
    output_path = output_path or str(Path(video_path).with_suffix('_enhanced.mp4'))
    
    cmd = [
        FFMPEG, "-y", "-i", video_path,
        "-vf", "hqdn3d=3:2:4:3,unsharp=3:3:0.5",
        "-c:a", "copy",
        output_path
    ]
    run(cmd)
    print(f"✅ 增强完成: {output_path}")
    return output_path

def add_subtitle(video_path, srt_path, output_path=None):
    """添加字幕"""
    output_path = output_path or str(Path(video_path).with_suffix('_subtitled.mp4'))
    
    cmd = [FFMPEG, "-y", "-i", video_path, "-vf", f"subtitles='{srt_path}'", output_path]
    run(cmd)
    print(f"✅ 字幕添加完成: {output_path}")
    return output_path

def add_music(video_path, music_path, output_path=None, music_volume=0.2):
    """添加背景音乐"""
    output_path = output_path or str(Path(video_path).with_suffix('_music.mp4'))
    
    cmd = [
        FFMPEG, "-y", "-i", video_path, "-i", music_path,
        "-filter_complex", f"[1:a]volume={music_volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]",
        "-map", "0:v", "-map", "[aout]", "-c:v", "copy",
        output_path
    ]
    run(cmd)
    print(f"✅ 背景音乐添加完成: {output_path}")
    return output_path

def merge_videos(video_paths, output_path):
    """合并视频"""
    list_file = Path(output_path).parent / "merge_list.txt"
    with open(list_file, "w") as f:
        for v in video_paths:
            f.write(f"file '{v}'\n")
    
    cmd = [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", output_path]
    run(cmd)
    list_file.unlink(missing_ok=True)
    print(f"✅ 合并完成: {output_path}")
    return output_path

def extract_audio(video_path, output_path=None):
    """提取音频"""
    output_path = output_path or str(Path(video_path).with_suffix('.wav'))
    cmd = [FFMPEG, "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", output_path]
    run(cmd)
    print(f"✅ 音频提取完成: {output_path}")
    return output_path

def speed_change(video_path, speed=1.0, output_path=None):
    """调整速度"""
    output_path = output_path or str(Path(video_path).with_suffix(f'_speed{speed}.mp4'))
    cmd = [FFMPEG, "-y", "-i", video_path, "-filter:v", f"setpts={1/speed}*PTS", "-filter:a", f"atempo={speed}", output_path]
    run(cmd)
    print(f"✅ 速度调整完成: {output_path}")
    return output_path

def resize_video(video_path, width=None, height=1080, output_path=None):
    """调整分辨率"""
    output_path = output_path or str(Path(video_path).with_suffix('_resized.mp4'))
    scale = f"scale={width}:{height}" if width else f"scale=-2:{height}"
    cmd = [FFMPEG, "-y", "-i", video_path, "-vf", scale, "-c:a", "copy", output_path]
    run(cmd)
    print(f"✅ 分辨率调整完成: {output_path}")
    return output_path

# 命令行接口
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("""
📹 视频处理工具

用法:
  python video_tools.py split <视频文件> [每段分钟数]
  python video_tools.py enhance <视频文件>
  python video_tools.py merge <视频1> <视频2> ... <输出文件>
  python video_tools.py audio <视频文件>
  python video_tools.py subtitle <视频文件> <字幕.srt>
  python video_tools.py music <视频文件> <音乐文件>
  python video_tools.py speed <视频文件> <速度倍数>
  python video_tools.py resize <视频文件> <宽度>
""")
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == "split":
        duration = int(args[1]) if len(args) > 1 else 10
        split_video(args[0], duration)
    elif cmd == "enhance":
        enhance_video(args[0])
    elif cmd == "merge":
        merge_videos(args[:-1], args[-1])
    elif cmd == "audio":
        extract_audio(args[0])
    elif cmd == "subtitle":
        add_subtitle(args[0], args[1])
    elif cmd == "music":
        add_music(args[0], args[1])
    elif cmd == "speed":
        speed_change(args[0], float(args[1]))
    elif cmd == "resize":
        resize_video(args[0], int(args[1]))
    else:
        print(f"未知命令: {cmd}")
