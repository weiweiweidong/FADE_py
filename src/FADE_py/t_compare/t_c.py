# test_compare.py - 简单的变量比较测试文件

import numpy as np
from scipy.io import loadmat
from PIL import Image

# 导入你的FADE函数
# from fade import FADE


class FADEComparator:
    """FADE函数中间变量比较器"""

    def __init__(self, mat_file="FADE_key_variables.mat"):
        """初始化，加载MATLAB数据"""
        try:
            self.matlab_data = loadmat(mat_file)
            print(f"✅ 成功加载MATLAB数据: {mat_file}")
            print(f"可用变量: {list(self.matlab_data.keys())}")
        except FileNotFoundError:
            print(f"❌ 找不到文件: {mat_file}")
            self.matlab_data = None
        except Exception as e:
            print(f"❌ 加载文件时出错: {e}")
            self.matlab_data = None

    def compare_variable(self, var_name, python_value, tolerance=1e-10):
        """比较单个变量"""
        if self.matlab_data is None:
            print("❌ MATLAB数据未加载")
            return False

        if var_name not in self.matlab_data:
            print(f"⚠️  变量 '{var_name}' 不在MATLAB数据中")
            return False

        matlab_value = self.matlab_data[var_name]

        print(f"\n=== 比较变量: {var_name} ===")
        print(f"Python shape: {python_value.shape}")
        print(f"MATLAB shape: {matlab_value.shape}")
        print(f"Python dtype: {python_value.dtype}")
        print(f"MATLAB dtype: {matlab_value.dtype}")

        # 检查形状是否相同
        if python_value.shape != matlab_value.shape:
            print("❌ 形状不匹配!")
            return False

        # 转换为相同的数据类型进行比较
        python_float = python_value.astype(np.float64)
        matlab_float = matlab_value.astype(np.float64)

        # 计算差异
        diff = np.abs(python_float - matlab_float)
        max_diff = np.max(diff)
        mean_diff = np.mean(diff)

        print(f"最大差异: {max_diff}")
        print(f"平均差异: {mean_diff}")

        # 判断是否相等
        if max_diff < tolerance:
            print("✅ 变量匹配!")
            return True
        else:
            print("❌ 变量不匹配!")
            # 显示一些不匹配的位置
            diff_positions = np.where(diff > tolerance)
            if len(diff_positions[0]) > 0:
                print(f"不匹配位置数量: {len(diff_positions[0])}")
                # 显示前几个不匹配的位置
                for i in range(min(5, len(diff_positions[0]))):
                    pos = tuple(coord[i] for coord in diff_positions)
                    print(
                        f"  位置 {pos}: Python={python_float[pos]:.6f}, MATLAB={matlab_float[pos]:.6f}"
                    )
            return False

    def compare_multiple(self, variables_dict, tolerance=1e-10):
        """比较多个变量"""
        results = {}

        print(f"\n{'='*50}")
        print("开始批量比较变量")
        print(f"{'='*50}")

        for var_name, python_value in variables_dict.items():
            results[var_name] = self.compare_variable(var_name, python_value, tolerance)

        # 总结
        print(f"\n{'='*50}")
        print("比较结果总结:")
        passed = sum(results.values())
        total = len(results)

        for var_name, result in results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"  {var_name}: {status}")

        print(f"\n总计: {passed}/{total} 个变量匹配")
        print(f"成功率: {passed/total*100:.1f}%")

        return results


def test_fade_step_by_step():
    """逐步测试FADE函数的各个步骤"""

    # 创建比较器
    comparator = FADEComparator("FADE_key_variables.mat")

    if comparator.matlab_data is None:
        print("无法加载MATLAB数据，退出测试")
        return

    # 加载测试图像
    try:
        image = np.array(Image.open("test_image1.png"))
        print(f"✅ 加载图像成功: {image.shape}")
    except:
        print("⚠️  无法加载test_image1.png，创建合成图像")
        image = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)

    # 开始逐步计算并比较
    print("\n🚀 开始逐步计算FADE...")

    # 步骤1: 基本设置
    ps = 8
    row, col, dim = image.shape
    patch_row_num = row // ps
    patch_col_num = col // ps
    I = image[: patch_row_num * ps, : patch_col_num * ps, :3]

    # 比较基本变量
    basic_vars = {
        "ps": np.array([[ps]]),  # MATLAB中标量通常是1x1矩阵
        "row": np.array([[row]]),
        "col": np.array([[col]]),
        "patch_row_num": np.array([[patch_row_num]]),
        "patch_col_num": np.array([[patch_col_num]]),
        "I": I,
    }

    print("\n--- 步骤1: 基本设置 ---")
    comparator.compare_multiple(basic_vars)

    # 步骤2: RGB和灰度通道
    R = I[:, :, 0].astype(np.float64)
    G = I[:, :, 1].astype(np.float64)
    B = I[:, :, 2].astype(np.float64)

    # 这里需要你实现rgb2gray的Python版本
    # 简单实现：
    Ig = 0.2989 * R + 0.5870 * G + 0.1140 * B

    rgb_vars = {"R": R, "G": G, "B": B, "Ig": Ig}

    print("\n--- 步骤2: RGB和灰度通道 ---")
    comparator.compare_multiple(rgb_vars)

    # 可以继续添加更多步骤...
    # 这里只是示例，你可以根据需要添加更多计算步骤

    return comparator


def quick_compare(var_name, python_value, mat_file="FADE_key_variables.mat"):
    """快速比较单个变量的便捷函数"""
    comparator = FADEComparator(mat_file)
    return comparator.compare_variable(var_name, python_value)


def show_matlab_variables(mat_file="FADE_key_variables.mat"):
    """显示MATLAB文件中的所有变量信息"""
    try:
        data = loadmat(mat_file)
        print(f"\n=== MATLAB文件 {mat_file} 中的变量 ===")

        for key, value in data.items():
            if not key.startswith("__"):  # 跳过元数据
                if isinstance(value, np.ndarray):
                    print(f"{key}: shape={value.shape}, dtype={value.dtype}")
                    if value.size < 10:  # 小数组显示值
                        print(f"  值: {value.flatten()}")
                    else:
                        print(f"  范围: [{value.min():.6f}, {value.max():.6f}]")
                else:
                    print(f"{key}: {type(value)}")

    except Exception as e:
        print(f"❌ 无法读取文件: {e}")
