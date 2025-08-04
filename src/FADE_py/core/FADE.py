import numpy as np

from t_compare.t_c import FADEComparator, quick_compare


def FADE(I: np.ndarray) -> float:

    comparator = FADEComparator("data/FADE_key_variables.mat")

    ps = 8
    # Size of a test image for checking possilbe distinct patches
    row, col, dim = I.shape
    patch_row_num = row // ps  # 向下取整
    patch_col_num = col // ps
    I = I[: patch_row_num * ps, : patch_col_num * ps, :3]

    # RGB and gray channel
    R = I[:, :, 0].astype(np.float64)  # Red channel
    G = I[:, :, 1].astype(np.float64)  # Green channel
    B = I[:, :, 2].astype(np.float64)  # Blue channel
    Ig = 0.2989 * R + 0.5870 * G + 0.1140 * B  # Gray channel

    variables_to_compare = {
        "ps": np.array([[ps]]),
        "row": np.array([[row]]),
        "R": R,
        "G": G,
        "B": B,
    }

    # 举例
    comparator.compare_variable("R", R)
    comparator.compare_variable("ps", np.array([[ps]]))
    comparator.compare_multiple(variables_to_compare)
    return 1.0
