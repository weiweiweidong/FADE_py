# FADE（雾感知密度评估器）

[English README](../README.md)

这是一个 FADE 算法的高性能 Python 实现。  
项目通过 12 个手工特征和参考统计量，对单张 RGB 图像进行无参考雾浓度估计。

论文来源：

> Choi, L. K., You, J., & Bovik, A. C. (2015).  
> _Referenceless prediction of perceptual fog density and perceptual image quality._

## 功能特性

- 向量化实现，加速推理
- 完整支持 12 维 FADE 特征流程
- 模块化架构（`features`、`ops`、`models`、`pipeline`）
- 对外 API：`fade(image)` 与 `fade_with_map(image)`
- 参考 `.mat` 统计文件位于 `src/fade/data`

## 安装

### 环境要求

- Python `>= 3.13`

### 安装依赖

```bash
python -m pip install numpy scipy matplotlib pillow
```

### 以可编辑模式安装

```bash
python -m pip install -e .
```

## 快速开始

```python
from PIL import Image
import numpy as np
from fade import fade, fade_with_map

img = np.array(Image.open("test_image/test_image1.png").convert("RGB"))

score = fade(img)
print("FADE score:", score)

score, dmap = fade_with_map(img)
print("score:", score, "map shape:", dmap.shape)
```

## 测试 Notebook

使用 `test_fade.ipynb` 可以对样例图片计算 FADE 分值。

输出包括：

- 图片名
- 图片尺寸
- FADE 分值
- 耗时

## 项目结构

```text
src/fade/
  api.py            # 对外 API
  pipeline.py       # 主流程编排
  features/         # f01 ~ f12 特征模块
  ops/              # 底层算子
  models/           # 上下文与参考统计
  data/             # 参考 .mat 文件
  fade.py           # 旧版基线实现
```

## 说明

- 输入应为 RGB `np.ndarray`，形状 `(H, W, 3)`。
- 流程使用不重叠 `8x8` 图像块。
- FADE 分值越高，表示雾越浓。

## 参考资料

- `reference/FADE.pdf`：原论文
- `reference/FADE_py-main.zip`：旧实现归档

## 许可证

MIT（见 [LICENSE](../LICENSE)）
