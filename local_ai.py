#!/usr/bin/env python3
"""
本地AI工具箱 - 完全免费！
功能：Stable Diffusion绘图、Ollama AI对话、离线语音合成
"""

import os
import subprocess
import sys
from pathlib import Path

# 配置路径
WORKSPACE = Path(r"C:\Users\WUccc\.openclaw\workspace")
SD_DIR = WORKSPACE / "stable-diffusion"
OLLAMA_DIR = WORKSPACE / "ollama_models"

class LocalAITools:
    def __init__(self):
        self.workspace = WORKSPACE
    
    # ==================== Stable Diffusion ====================
    
    def install_sd_webui(self):
        """安装 Stable Diffusion WebUI"""
        print("""
📥 安装 Stable Diffusion WebUI...

方法1: 使用 Fooocus (推荐，最简单)
  1. 下载: https://github.com/lllyasviel/Fooocus/releases
  2. 解压后运行 run.bat

方法2: 使用 ComfyUI (更专业)
  1. 下载: https://github.com/comfyanonymous/ComfyUI
  2. 运行 run_nvidia_gpu.bat

方法3: 使用 diffusers Python库
  已安装! 可以用以下代码:
  
```python
from diffusers import StableDiffusionPipeline
import torch

model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

image = pipe("中国传统建筑，灯笼，对联").images[0]
image.save("output.png")
```

注意: 首次运行会自动下载模型(约4GB)
""")
        return "📥 请下载 Stable Diffusion WebUI"
    
    # ==================== Ollama ====================
    
    def check_ollama(self):
        """检查Ollama是否安装"""
        try:
            result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
            return f"✅ Ollama已安装: {result.stdout.strip()}"
        except:
            return """
❌ Ollama未安装

📥 安装 Ollama:
  1. 访问: https://ollama.com
  2. 下载 Windows 版本
  3. 安装后运行: ollama serve
  
📦 常用模型:
  ollama pull llama2      # 下载Llama 2
  ollama pull qwen        # 下载通义千问
  ollama pull mistral    # 下载Mistral
  ollama pull codellama  # 下载代码模型

🤖 使用示例:
  ollama run llama2 "你好，请介绍一下自己"
"""
    
    def use_ollama(self, prompt, model="qwen"):
        """使用Ollama运行AI"""
        try:
            result = subprocess.run(
                ["ollama", "run", model, prompt],
                capture_output=True, text=True, timeout=120
            )
            return result.stdout
        except Exception as e:
            return f"❌ 错误: {str(e)}\n请先安装 Ollama: https://ollama.com"
    
    # ==================== 本地语音合成 ====================
    
    def use_tts(self, text, voice="zh-CN-XiaoxiaoNeural"):
        """使用本地TTS (Windows内置)"""
        # 使用Windows自带的语音合成
        script = f'''
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0
$synth.SelectVoice("{voice}")
$synth.Speak("{text}")
'''
        temp_ps = self.workspace / "temp_tts.ps1"
        with open(temp_ps, "w", encoding="utf-8") as f:
            f.write(script)
        
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(temp_ps)])
        temp_ps.unlink(missing_ok=True)
        return "✅ 语音播放完成"
    
    def list_voices(self):
        """列出可用的Windows语音"""
        script = '''
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name }
'''
        result = subprocess.run(
            ["powershell", "-Command", script],
            capture_output=True, text=True
        )
        return f"🎙️ 可用语音:\n{result.stdout}"
    
    # ==================== 离线AI绘图 ====================
    
    def generate_image(self, prompt):
        """使用本地Diffusers生成图片"""
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            
            print("📥 首次运行，正在下载模型...")
            pipe = StableDiffusionPipeline.from_pretrained(
                "CompVis/stable-diffusion-v1-4",
                torch_dtype=torch.float16
            )
            pipe = pipe.to("cuda")
            
            print("🎨 正在生成图片...")
            image = pipe(prompt).images[0]
            
            output_path = self.workspace / "ai_art.png"
            image.save(output_path)
            
            return f"✅ 图片已保存: {output_path}"
        except Exception as e:
            return f"❌ 错误: {str(e)}"
    
    # ==================== 帮助 ====================
    
    def help(self):
        return """
🤖 本地AI工具箱 - 帮助

📦 已安装的库:
  - diffusers: AI绘图
  - transformers: AI模型
  - whisper: 语音转文字
  - ollama: AI对话

📥 需要手动下载:
  - Stable Diffusion WebUI: https://github.com/lllyasviel/Fooocus
  - Ollama: https://ollama.com
  - GPT-SoVITS: https://github.com/RVC-Boss/GPT-SoVITS

🖥️ 使用示例:

# 1. 语音合成 (Windows内置)
python local_ai.py tts "你好，这是一个测试"

# 2. 列出可用语音
python local_ai.py voices

# 3. 使用Ollama (需安装)
ollama run qwen "你好"

# 4. AI绘图 (需下载模型)
python local_ai.py draw "一只可爱的熊猫"
"""


if __name__ == "__main__":
    tools = LocalAITools()
    
    if len(sys.argv) < 2:
        print(tools.help())
        sys.exit(1)
    
    cmd = sys.argv[1].lower()
    args = " ".join(sys.argv[2:])
    
    if cmd == "help":
        print(tools.help())
    
    elif cmd == "tts":
        print(tools.use_tts(args if args else "你好"))
    
    elif cmd == "voices":
        print(tools.list_voices())
    
    elif cmd == "ollama":
        model = sys.argv[2] if len(sys.argv) > 2 else "qwen"
        print(tools.use_ollama(args, model))
    
    elif cmd == "draw":
        print(tools.generate_image(args if args else "一只猫"))
    
    elif cmd == "check":
        print(f"✅ Ollama状态: {tools.check_ollama()}")
        print(f"📥 SD安装: {tools.install_sd_webui()}")
    
    else:
        print(tools.help())
