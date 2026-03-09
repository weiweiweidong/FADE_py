# FADE (Fog Aware Density Evaluator)

[中文文档 / Chinese README](doc/readme_CN.md)

High-performance Python implementation of the FADE algorithm from:

> Choi, L. K., You, J., & Bovik, A. C. (2015).  
> _Referenceless prediction of perceptual fog density and perceptual image quality._

This project estimates fog density from a single RGB image using 12 handcrafted features and reference statistics.

## Features

- Vectorized implementation for faster inference
- Full 12-feature FADE pipeline
- Modular architecture (`features`, `ops`, `models`, `pipeline`)
- Public API: `fade(image)` and `fade_with_map(image)`
- Reference `.mat` stats under `src/fade/data`

## Installation

### Requirements

- Python `>= 3.13`

### Install dependencies

```bash
python -m pip install numpy scipy matplotlib pillow
```

### Install package (editable)

```bash
python -m pip install -e .
```

## Quick Start

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

## Test Notebook

Use `test_fade.ipynb` to compute FADE scores for sample images.

Output includes:

- image name
- image shape
- FADE score
- elapsed time

## Project Structure

```text
src/fade/
  api.py            # public API
  pipeline.py       # end-to-end orchestration
  features/         # f01 ~ f12 feature modules
  ops/              # low-level operators
  models/           # context + reference stats
  data/             # reference .mat files
  fade.py           # legacy baseline implementation
```

## Notes

- Input should be RGB `np.ndarray`, shape `(H, W, 3)`.
- The pipeline uses non-overlapping `8x8` patches.
- Higher FADE score means denser fog.

## Reference Assets

- `reference/FADE.pdf`: original paper
- `reference/FADE_py-main.zip`: previous implementation archive

## License

MIT (see [LICENSE](LICENSE))
