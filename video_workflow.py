#!/usr/bin/env python3
"""
专业视频处理工作流 - 非遗文化博主专用
功能：长视频自动分段、转写、分析、整合
"""

import os
import sys
import json
import subprocess
import whisper
from pathlib import Path

# 配置
PROJECT_DIR = Path(r"C:\Users\WUccc\.openclaw\workspace\videos")
SEGMENT_DURATION = 600  # 每段10分钟

class VideoWorkflow:
    def __init__(self, video_path, project_name=None):
        self.video_path = Path(video_path)
        self.project_name = project_name or self.video_path.stem
        self.project_dir = PROJECT_DIR / self.project_name
        self.segments_dir = self.project_dir / "segments"
        self.transcripts_dir = self.project_dir / "transcripts"
        self.summaries_dir = self.project_dir / "summaries"
        
        # 创建目录
        for d in [self.project_dir, self.segments_dir, self.transcripts_dir, self.summaries_dir]:
            d.mkdir(parents=True, exist_ok=True)
    
    def get_video_info(self):
        """获取视频信息"""
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", str(self.video_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        info = json.loads(result.stdout)
        duration = float(info.get('format', {}).get('duration', 0))
        return {
            'duration': duration,
            'duration_str': f"{int(duration//60)}:{int(duration%60):02d}",
            'size': info.get('format', {}).get('size', 0)
        }
    
    def split_video(self, duration_per_segment=SEGMENT_DURATION):
        """自动分割视频"""
        info = self.get_video_info()
        total_duration = info['duration']
        segments = []
        
        print(f"📹 视频总时长: {info['duration_str']}")
        print(f"✂️ 正在分割视频，每段 {duration_per_segment//60} 分钟...")
        
        start = 0
        segment_idx = 1
        while start < total_duration:
            end = min(start + duration_per_segment, total_duration)
            output_file = self.segments_dir / f"segment_{segment_idx:03d}.mp4"
            
            cmd = [
                "ffmpeg", "-y", "-i", str(self.video_path),
                "-ss", str(start), "-to", str(end),
                "-c", "copy", str(output_file)
            ]
            subprocess.run(cmd, capture_output=True)
            
            segments.append({
                'index': segment_idx,
                'file': str(output_file),
                'start': start,
                'end': end
            })
            
            print(f"  ✅ 分段 {segment_idx}: {start//60}:{start%60:02d} - {end//60}:{end%60:02d}")
            start = end
            segment_idx += 1
        
        # 保存分段信息
        with open(self.project_dir / "segments.json", "w") as f:
            json.dump(segments, f, indent=2)
        
        print(f"✅ 共生成 {len(segments)} 个分段")
        return segments
    
    def transcribe_segment(self, segment_file, model="base"):
        """转写单个分段"""
        print(f"  📝 转写中: {Path(segment_file).name}...")
        
        # 提取音频
        audio_file = Path(segment_file).with_suffix('.wav')
        cmd = [
            "ffmpeg", "-y", "-i", segment_file,
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000",
            "-ac", "1", str(audio_file)
        ]
        subprocess.run(cmd, capture_output=True)
        
        # 转写
        result = model.transcribe(str(audio_file), language="zh")
        text = result["text"]
        
        # 保存
        transcript_file = self.transcripts_dir / f"{Path(segment_file).stem}.txt"
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(text)
        
        # 删除临时音频
        audio_file.unlink(missing_ok=True)
        
        print(f"  ✅ 转写完成: {len(text)} 字符")
        return text
    
    def transcribe_all(self, segments):
        """转写所有分段"""
        print("\n🎙️ 开始语音转写...")
        model = whisper.load_model("base")
        
        transcripts = []
        for seg in segments:
            text = self.transcribe_segment(seg['file'], model)
            transcripts.append({
                'segment': seg['index'],
                'text': text,
                'file': seg['file']
            })
        
        # 合并所有转写
        full_text = "\n\n".join([t['text'] for t in transcripts])
        with open(self.project_dir / "full_transcript.txt", "w", encoding="utf-8") as f:
            f.write(full_text)
        
        print(f"✅ 全部转写完成: {len(full_text)} 字符")
        return transcripts
    
    def enhance_video(self, input_file, output_file=None):
        """增强视频质量"""
        output_file = output_file or Path(input_file).with_suffix('_enhanced.mp4')
        
        print(f"🎨 增强视频质量: {Path(input_file).name}...")
        
        # 降噪 + 调色 + 增强
        cmd = [
            "ffmpeg", "-y", "-i", input_file,
            # 降噪
            "-vf", "hqdn3d=4:3:6:4.5",
            # 锐化
            "-vf", "unsharp=5:5:1.0:5:5:0.0",
            # 亮度对比度
            "-vf", "eq=brightness=0.06:contrast=1.2",
            "-c:a", "copy",
            str(output_file)
        ]
        subprocess.run(cmd, capture_output=True)
        
        print(f"  ✅ 增强完成: {output_file}")
        return str(output_file)
    
    def create_clip(self, input_file, start_time, duration, output_file):
        """从视频中截取精彩片段"""
        cmd = [
            "ffmpeg", "-y", "-i", input_file,
            "-ss", str(start_time), "-t", str(duration),
            "-c", "copy", str(output_file)
        ]
        subprocess.run(cmd, capture_output=True)
        return str(output_file)
    
    def add_subtitle(self, video_file, subtitle_file, output_file):
        """添加字幕"""
        cmd = [
            "ffmpeg", "-y", "-i", video_file,
            "-vf", f"subtitles='{subtitle_file}'",
            str(output_file)
        ]
        subprocess.run(cmd, capture_output=True)
        return str(output_file)
    
    def add_audio(self, video_file, audio_file, output_file, volume=0.3):
        """添加背景音乐"""
        cmd = [
            "ffmpeg", "-y", "-i", video_file, "-i", audio_file,
            "-filter_complex", f"[1:a]volume={volume}[bgm];[0:a][bgm]amix=inputs=2:duration=first[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy", str(output_file)
        ]
        subprocess.run(cmd, capture_output=True)
        return str(output_file)
    
    def merge_videos(self, video_files, output_file):
        """合并多个视频"""
        # 创建文件列表
        list_file = self.project_dir / "filelist.txt"
        with open(list_file, "w") as f:
            for v in video_files:
                f.write(f"file '{v}'\n")
        
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(list_file), "-c", "copy", str(output_file)
        ]
        subprocess.run(cmd, capture_output=True)
        
        list_file.unlink(missing_ok=True)
        return str(output_file)
    
    def run_full_pipeline(self):
        """运行完整工作流"""
        print("="*50)
        print(f"🎬 视频处理工作流启动: {self.project_name}")
        print("="*50)
        
        # 1. 获取信息
        info = self.get_video_info()
        print(f"\n📊 视频信息:")
        print(f"   时长: {info['duration_str']}")
        print(f"   大小: {int(info['size'])/1024/1024:.1f} MB")
        
        # 2. 分割
        segments = self.split_video()
        
        # 3. 转写
        transcripts = self.transcribe_all(segments)
        
        print("\n" + "="*50)
        print("✅ 工作流第一阶段完成!")
        print(f"📁 项目目录: {self.project_dir}")
        print("="*50)
        
        return {
            'segments': segments,
            'transcripts': transcripts,
            'project_dir': str(self.project_dir)
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python video_workflow.py <视频文件路径>")
        sys.exit(1)
    
    workflow = VideoWorkflow(sys.argv[1])
    workflow.run_full_pipeline()
