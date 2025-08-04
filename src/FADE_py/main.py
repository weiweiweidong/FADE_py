#!/usr/bin/env python3
"""
应用程序的主入口点
"""

import sys
import argparse
from PIL import Image
import matplotlib.pyplot as plt
import os

from core.FADE import FADE

os.environ["PYTHONWARNINGS"] = "ignore"

CONST = {"image_path": "data/test_image2.JPG"}


def main():
    """主函数"""
    image = Image.open(CONST["image_path"])

    FADE("dong")


if __name__ == "__main__":
    main()
