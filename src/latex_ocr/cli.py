"""命令行入口"""

import argparse
import sys

from latex_ocr import __version__
from latex_ocr.recognizer import LatexOCR


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="latex-ocr",
        description="📐 从图片或剪贴板识别数学公式，输出 LaTeX",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # clipboard 子命令
    clip_parser = subparsers.add_parser(
        "clip", help="从剪贴板读取图片并识别（仅 macOS）"
    )
    clip_parser.add_argument(
        "-c", "--copy", action="store_true", help="自动将结果复制到剪贴板"
    )

    # file 子命令
    file_parser = subparsers.add_parser("file", help="从图片文件识别")
    file_parser.add_argument("path", help="图片文件路径")
    file_parser.add_argument(
        "-c", "--copy", action="store_true", help="将结果复制到剪贴板（仅 macOS）"
    )

    return parser


def cmd_clip(args: argparse.Namespace) -> None:
    """处理剪贴板识别"""
    from latex_ocr.clipboard import get_image_from_clipboard, copy_to_clipboard

    print("📋 正在从剪贴板读取图像…")
    image = get_image_from_clipboard()

    if image is None:
        print("❌ 剪贴板中没有找到图像！请先截图或复制一张图片。")
        sys.exit(1)

    print(f"🖼️  检测到图像尺寸: {image.size}")

    ocr = LatexOCR()
    print("🔍 正在识别公式…")
    latex = ocr.recognize_image(image)

    print("\n✨ 识别结果（LaTeX）:")
    print(latex)

    if args.copy:
        if copy_to_clipboard(latex):
            print("✅ LaTeX 已复制到剪贴板！")
    else:
        if input("\n是否将结果复制到剪贴板？(y/n): ").strip().lower() == "y":
            if copy_to_clipboard(latex):
                print("✅ LaTeX 已复制到剪贴板！")


def cmd_file(args: argparse.Namespace) -> None:
    """处理文件识别"""
    ocr = LatexOCR()
    print(f"🔍 正在识别: {args.path}")
    latex = ocr.recognize_file(args.path)

    print("\n✨ 识别结果（LaTeX）:")
    print(latex)

    if args.copy:
        from latex_ocr.clipboard import copy_to_clipboard

        if copy_to_clipboard(latex):
            print("✅ LaTeX 已复制到剪贴板！")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    handlers = {
        "clip": cmd_clip,
        "file": cmd_file,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
