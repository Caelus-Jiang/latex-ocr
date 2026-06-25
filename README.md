# 📐 LaTeX OCR

[![PyPI version](https://img.shields.io/pypi/v/latex-ocr)](https://pypi.org/project/latex-ocr/)
[![Python](https://img.shields.io/pypi/pyversions/latex-ocr)](https://pypi.org/project/latex-ocr/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

从图片或 macOS 剪贴板识别数学公式，一键输出 LaTeX。基于 [Pix2Text](https://github.com/breezedeus/Pix2Text)。

## ✨ 特性

- **文件识别**：支持 PNG / JPG / TIFF 等常见图片格式
- **剪贴板识别**：截图后直接识别，无需保存文件（仅 macOS）
- **自动复制**：识别结果可一键复制回剪贴板
- **MPS 加速**：Apple Silicon 自动启用 GPU 加速

> ⚠️ **平台说明**：剪贴板功能依赖 macOS AppKit，仅支持 macOS。Linux / Windows 用户请使用 `latex-ocr file` 命令识别图片文件。

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/<your-username>/latex-ocr.git
cd latex-ocr

# 基础安装（文件识别）
pip install .

# 完整安装（含剪贴板支持，仅 macOS）
pip install ".[clipboard]"
```

> 📦 本项目尚未发布到 PyPI，暂需从源码安装。后续发布后即可使用 `pip install latex-ocr`。

### 命令行使用

安装后可直接使用 `latex-ocr` 命令：

```bash
# 从图片文件识别
latex-ocr file formula.png

# 从剪贴板识别（macOS，先截图再运行）
latex-ocr clip

# 识别并自动复制到剪贴板
latex-ocr clip --copy
latex-ocr file formula.png --copy
```

如果不想安装，也可以直接运行模块（需在项目根目录下执行）：

```bash
python -m latex_ocr.cli file formula.png
python -m latex_ocr.cli clip
```

### Python API

```python
from latex_ocr import LatexOCR

ocr = LatexOCR()

# 从文件识别
latex = ocr.recognize_file("formula.png")

# 从 PIL Image 识别
from PIL import Image
image = Image.open("formula.png")
latex = ocr.recognize_image(image)

print(latex)
```

## 📋 开发环境搭建

如果你想参与开发或从源码运行：

```bash
# 1. 创建环境
conda create -n latex-ocr python=3.10 -y
conda activate latex-ocr

# 2. 安装 PyTorch（Apple Silicon 自动启用 MPS）
pip install torch torchvision torchaudio

# 3. 以开发模式安装本项目
pip install -e ".[clipboard,dev]"

# 4. 验证
latex-ocr --version
```

### 验证 MPS 是否可用

```python
python -c "import torch; print('MPS available:', torch.backends.mps.is_available())"
```

## ⚠️ 常见问题

### `libomp.dylib not found`

```bash
brew install libomp
```

### 模型下载太慢

首次运行时会自动从 Hugging Face 下载模型（约 600MB）。可手动下载：

1. 访问 [breezedeus/pix2text](https://huggingface.co/breezedeus/pix2text) 下载 `models.zip`
2. 解压到 `~/.pix2text/`

```bash
mkdir -p ~/.pix2text
unzip models.zip -d ~/.pix2text/
```

### 图像路径含中文或空格

```python
from pathlib import Path
latex = ocr.recognize_file(Path("我的公式.png"))
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

[MIT](LICENSE)