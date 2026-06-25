"""LaTeX 公式识别核心逻辑"""

from pathlib import Path
from PIL import Image
from pix2text import Pix2Text


class LatexOCR:
    """封装 Pix2Text 的公式识别器"""

    def __init__(self):
        self._recognizer: Pix2Text | None = None

    @property
    def recognizer(self) -> Pix2Text:
        """懒加载模型，首次调用时初始化"""
        if self._recognizer is None:
            print("🧠 加载模型中…")
            self._recognizer = Pix2Text()
        return self._recognizer

    def recognize_file(self, image_path: str | Path) -> str:
        """从图片文件识别 LaTeX 公式"""
        path = Path(image_path).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"图片不存在: {path}")
        return self.recognizer.recognize_formula(str(path))

    def recognize_image(self, image: Image.Image) -> str:
        """从 PIL Image 对象识别 LaTeX 公式"""
        return self.recognizer.recognize_formula(image)
