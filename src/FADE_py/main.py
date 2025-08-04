#!/usr/bin/env python3
"""
应用程序的主入口点
"""

import sys
import argparse
from PIL import Image
import matplotlib.pyplot as plt
import os
import numpy as np

from core.FADE import FADE

os.environ["PYTHONWARNINGS"] = "ignore"

CONST = {"image_path": "data/test_image1.png"}


def main():
    """主函数"""
    image = np.array(Image.open(CONST["image_path"]))

    density = FADE(image)


if __name__ == "__main__":
    main()
