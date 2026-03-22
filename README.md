# FADE — Fog Aware Density Evaluator

[![Python](https://img.shields.io/badge/python-%3E%3D3.10-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[中文文档](doc/README_CN.md)

A high-performance Python implementation of the **FADE** fog density estimation algorithm, based on:

> Choi, L. K., You, J., & Bovik, A. C. (2015).
> *Referenceless prediction of perceptual fog density and perceptual image quality.*
> IEEE Transactions on Image Processing, 24(11), 3888–3901.

FADE estimates fog density from a **single RGB image** using 12 handcrafted perceptual features and pre-computed reference statistics — no reference image required.

---

## Features

- **No-reference fog estimation** — works on a single image
- **Vectorized pipeline** — fast NumPy/SciPy implementation
- **12-feature FADE pipeline** — faithful reproduction of the original algorithm
- **Modular architecture** — `features`, `ops`, `models`, `pipeline` sub-packages
- **Simple public API** — `fade(image)` and `fade_with_map(image)`
- **256-test suite** — pytest coverage across all modules

---

## Installation

**Requirements:** Python >= 3.10

This project is managed with [uv](https://github.com/astral-sh/uv). Using `uv` is recommended, but a standard `pip` workflow is also supported.

### Option 1: uv (recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install all dependencies
uv sync

# Install with test dependencies
uv sync --extra test

# Install fade in editable mode so it can be imported in the environment
uv pip install -e .

# Run any command inside the managed environment
uv run python -c "from fade import fade; print('OK')"
```

### Option 2: pip + venv

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install numpy scipy matplotlib pillow
pip install -e .
```

---

## Quick Start

```python
from PIL import Image
import numpy as np
from fade import fade, fade_with_map

img = np.array(Image.open("test_image/test_image1.png").convert("RGB"))

# Scalar fog density score
score = fade(img)
print(f"FADE score: {score:.4f}")

# Score + per-patch density map
score, density_map = fade_with_map(img)
print(f"Score: {score:.4f} | Map shape: {density_map.shape}")
```

A higher FADE score indicates **denser fog**.

---

## Project Structure

```text
fade_py/
├── src/fade/
│   ├── api.py            # Public API: fade() and fade_with_map()
│   ├── pipeline.py       # End-to-end orchestration (FadePipeline)
│   ├── features/         # f01 ~ f12 — individual feature modules
│   │   ├── base.py       # Abstract base class for features
│   │   ├── registry.py   # Feature registry
│   │   └── f01.py ~ f12.py
│   ├── ops/              # Low-level operators (MSCN, entropy, patches, …)
│   ├── models/           # Context model + reference statistics loader
│   ├── data/             # Pre-computed reference .mat files
│   └── fade.py           # Legacy baseline implementation
├── tests/                # pytest suite (256 tests)
├── reference/            # Original paper (FADE.pdf) and archive
├── test_image/           # Sample images
├── test_fade.ipynb       # Interactive demo notebook
└── pyproject.toml
```

---

## Running Tests

With `uv`:

```bash
uv run pytest
uv run pytest -m "not slow"   # skip slow image-loading tests
```

With standard `pytest`:

```bash
pytest
pytest -m "not slow"
```

---

## Demo Notebook

Open `test_fade.ipynb` to compute FADE scores for sample images interactively.

Each row in the output shows:

| Field | Description |
|---|---|
| Image name | File name of the input image |
| Shape | Height × Width × Channels |
| FADE score | Estimated fog density (higher = denser) |
| Elapsed time | Wall-clock inference time |

---

## Notes

- Input must be an RGB `np.ndarray` with shape `(H, W, 3)` and dtype `uint8`.
- The pipeline operates on non-overlapping `8×8` patches.
- Reference statistics are loaded from `.mat` files in `src/fade/data/`.

---

## Reference Assets

- `reference/FADE.pdf` — original paper
- `reference/FADE_py-main.zip` — previous Python implementation archive

---

## License

[MIT](LICENSE)
