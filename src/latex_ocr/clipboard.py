"""macOS 剪贴板图像读取与写入工具"""

import sys
from io import BytesIO
from PIL import Image


def _check_macos():
    """检查是否在 macOS 上运行"""
    if sys.platform != "darwin":
        raise OSError(
            f"剪贴板功能仅支持 macOS，当前系统: {sys.platform}\n"
            "请使用 `latex-ocr file <图片路径>` 方式识别"
        )


def get_image_from_clipboard() -> Image.Image | None:
    """从 macOS 剪贴板读取图像，返回 PIL Image 或 None"""
    _check_macos()

    try:
        from AppKit import NSPasteboard, NSImage
    except ImportError:
        raise ImportError(
            "请安装 pyobjc: pip install pyobjc-core pyobjc-framework-Cocoa"
        )

    pasteboard = NSPasteboard.generalPasteboard()
    image_types = [
        "public.png",
        "public.jpeg",
        "public.tiff",
        "com.apple.quicktime-image",
    ]

    for img_type in image_types:
        if img_type in pasteboard.types():
            data = pasteboard.dataForType_(img_type)
            if data:
                img_bytes = data.bytes().tobytes()
                try:
                    return Image.open(BytesIO(img_bytes)).convert("RGB")
                except Exception as exc:
                    print(f"⚠️ 图像解析失败: {exc}")
                    return None

    # 兼容旧版 NSImage 方式
    try:
        nsimage = NSImage.imageWithPasteboard_(pasteboard)
        if nsimage:
            tiff_data = nsimage.TIFFRepresentation()
            if tiff_data:
                img_bytes = tiff_data.bytes().tobytes()
                return Image.open(BytesIO(img_bytes)).convert("RGB")
    except Exception:
        pass

    return None


def copy_to_clipboard(text: str) -> bool:
    """将文本复制到 macOS 剪贴板，成功返回 True"""
    _check_macos()

    try:
        from AppKit import NSPasteboard, NSStringPboardType
        from Foundation import NSString

        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()
        new_str = NSString.stringWithString_(text)
        pasteboard.setString_forType_(new_str, NSStringPboardType)
        return True
    except Exception as exc:
        print(f"⚠️ 复制到剪贴板失败: {exc}")
        return False
