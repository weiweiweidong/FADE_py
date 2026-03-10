# FADE 项目 `src` 目录学习笔记

这份文档整理了前面对 `src` 目录代码的讲解，目标读者是正在阅读这份项目代码的 Python 初学者。

内容包括：

- `src` 目录的整体结构
- 模块化版本的调用流程图
- `FeatureContext` 的数据依赖图
- `f01 ~ f12` 这 12 个特征的含义与计算方法
- 一张适合复习的特征学习表格

源码跳转入口：

- 包入口：[src/fade/**init**.py](/home/dong/workspace/my_github_repository/fade/src/fade/__init__.py)、[src/fade/api.py](/home/dong/workspace/my_github_repository/fade/src/fade/api.py)
- 主流程：[src/fade/pipeline.py](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py)
- 上下文与参考数据：[src/fade/models/context.py](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py)、[src/fade/models/reference_stats.py](/home/dong/workspace/my_github_repository/fade/src/fade/models/reference_stats.py)
- 底层算子：[src/fade/ops/patches.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/patches.py)、[src/fade/ops/entropy.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/entropy.py)、[src/fade/ops/mscn.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/mscn.py)、[src/fade/ops/distance.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/distance.py)、[src/fade/ops/ce.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/ce.py)
- 特征注册与接口：[src/fade/features/base.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/base.py)、[src/fade/features/registry.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/registry.py)
- 12 个特征文件：[f01.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f01.py)、[f02.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f02.py)、[f03.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f03.py)、[f04.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f04.py)、[f05.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f05.py)、[f06.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f06.py)、[f07.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f07.py)、[f08.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f08.py)、[f09.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f09.py)、[f10.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f10.py)、[f11.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f11.py)、[f12.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f12.py)
- 单文件版实现：[src/fade/fade.py](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py)
- CE 具体实现：[src/fade/ce.py](/home/dong/workspace/my_github_repository/fade/src/fade/ce.py)

关键函数定位：

- API 入口：[fade()](/home/dong/workspace/my_github_repository/fade/src/fade/api.py#L14)、[fade_with_map()](/home/dong/workspace/my_github_repository/fade/src/fade/api.py#L20)
- 流水线主类：[FadePipeline](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L17)
- 流水线步骤：[FadePipeline.default()](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L29)、[build_context()](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L33)、[compute_feature_maps()](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L36)、[build_feature_matrix()](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L40)、[run()](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L54)
- 上下文主类：[FeatureContext](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L15)
- 上下文关键属性：[image_rgb](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L23)、[Ig_int](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L58)、[Id](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L64)、[Is](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L70)、[rg](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L76)、[by](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L82)
- MSCN 相关定位：[FeatureContext.mscn](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L88)、[FeatureContext.sigma_map](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L97)、[FeatureContext.cv](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L102)、[FeatureContext.mscn_v](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L107)、[FeatureContext.mscn_v_patches](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L113)
- CE 相关定位：[FeatureContext.CE_gray](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L119)、[FeatureContext.CE_by](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L128)、[FeatureContext.CE_rg](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L133)、[compute_ce()](/home/dong/workspace/my_github_repository/fade/src/fade/ce.py#L68)
- Patch 与底层算子：[FeatureContext.to_patches()](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L138)、[to_patches()](/home/dong/workspace/my_github_repository/fade/src/fade/ops/patches.py#L8)、[compute_mscn_components()](/home/dong/workspace/my_github_repository/fade/src/fade/ops/mscn.py#L19)、[patch_entropy()](/home/dong/workspace/my_github_repository/fade/src/fade/ops/entropy.py#L8)、[batch_mahalanobis()](/home/dong/workspace/my_github_repository/fade/src/fade/ops/distance.py#L8)
- 参考统计数据：[load_reference_stats()](/home/dong/workspace/my_github_repository/fade/src/fade/models/reference_stats.py#L12)
- 特征接口与注册：[Feature](/home/dong/workspace/my_github_repository/fade/src/fade/features/base.py#L12)、[canonical_feature_registry()](/home/dong/workspace/my_github_repository/fade/src/fade/features/registry.py#L9)、[default_feature_registry()](/home/dong/workspace/my_github_repository/fade/src/fade/features/registry.py#L32)
- 12 个特征实现：[f01.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f01.py#L16)、[f02.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f02.py#L16)、[f03.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f03.py#L16)、[f04.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f04.py#L16)
- 更多特征实现：[f05.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f05.py#L16)、[f06.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f06.py#L16)、[f07.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f07.py#L16)、[f08.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f08.py#L16)
- 更多特征实现续：[f09.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f09.py#L17)、[f10.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f10.py#L16)、[f11.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f11.py#L16)、[f12.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f12.py#L16)
- 单文件版总览：[fade()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L176)、[fade_with_map()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L194)、[\_patch_entropy()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L75)、[\_batch_mahalanobis()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L142)

---

## 1. `src` 目录整体结构

`src` 目录里实现的是这个项目的核心 Python 包 `fade`。如果把它看成一条“从输入图片到输出雾浓度分数”的流水线，会比较容易理解：

1. 外部入口：别人怎么调用这个包
2. 流水线调度：按顺序执行哪些步骤
3. 特征提取：从图片里算出 12 个数值特征
4. 底层算子：被多个模块复用的数学工具
5. 参考数据：和“有雾/无雾”的统计模板做比较

### 1.1 目录分层

- [src/fade/**init**.py](/home/dong/workspace/my_github_repository/fade/src/fade/__init__.py) / [src/fade/api.py](/home/dong/workspace/my_github_repository/fade/src/fade/api.py)
  - 对外暴露的接口
- [src/fade/pipeline.py](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py)
  - 主执行流程
- [src/fade/features/](/home/dong/workspace/my_github_repository/fade/src/fade/features)
  - 12 个特征提取模块
- [src/fade/models/](/home/dong/workspace/my_github_repository/fade/src/fade/models)
  - 上下文对象、参考统计数据加载
- [src/fade/ops/](/home/dong/workspace/my_github_repository/fade/src/fade/ops)
  - 底层公共运算
- [src/fade/data/](/home/dong/workspace/my_github_repository/fade/src/fade/data)
  - MATLAB `.mat` 参考数据
- [src/fade/fade.py](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py)
  - 单文件版完整 FADE 实现
- [src/fade/ce.py](/home/dong/workspace/my_github_repository/fade/src/fade/ce.py)
  - Contrast Energy 的具体实现

### 1.2 各文件作用

#### [src/fade/**init**.py](/home/dong/workspace/my_github_repository/fade/src/fade/__init__.py)

作用很简单：定义这个包对外最重要的公开接口。

- 从 `api.py` 导入 `fade` 和 `fade_with_map`
- 用 `__all__` 声明这个包最希望别人使用的内容

这样用户可以直接写：

```python
from fade import fade, fade_with_map
```

#### [src/fade/api.py](/home/dong/workspace/my_github_repository/fade/src/fade/api.py)

这是对外 API 层，也就是别人真正调用的函数。

它包含：

- `_default_pipeline = FadePipeline.default()`
- `fade(I)`：输入图片，返回一个分数
- `fade_with_map(I)`：输入图片，返回“总分 + 每个 patch 的局部分布图”

这里的关键思想是：

- 真正复杂的逻辑不放在 API 里
- API 只是调用 `FadePipeline`

关键定位：

- [fade()](/home/dong/workspace/my_github_repository/fade/src/fade/api.py#L14)
- [fade_with_map()](/home/dong/workspace/my_github_repository/fade/src/fade/api.py#L20)

#### [src/fade/pipeline.py](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py)

这是整个项目最值得重点读的文件之一。它把 FADE 算法拆成了清晰的步骤。

核心类：

```python
@dataclass(slots=True)
class FadePipeline:
```

最重要的方法：

- [default()](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L29)：创建默认流水线，注册全部 12 个特征
- [build_context(image)](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L33)：把原图包装成 `FeatureContext`
- [compute_feature_maps(context)](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L36)：逐个运行特征模块
- [build_feature_matrix(feature_maps)](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L40)：把 12 张特征图拼成一个特征矩阵
- [run(image)](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py#L54)：完整执行一次 FADE

`run()` 的逻辑可以概括成：

1. 创建上下文对象 `FeatureContext`
2. 计算 12 个特征图
3. 把每个 patch 的 12 维特征拼成矩阵
4. 做 `log1p` 变换
5. 载入“无雾”和“有雾”的参考统计数据
6. 分别计算当前图像到这两类参考分布的马氏距离
7. 得到最终分数 `score = Df / (Dff + 1.0)`

#### [src/fade/fade.py](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py)

这个文件实现的也是 FADE，但它不是现在主流程用的模块化版本，而是“完整逻辑都写在一个文件里”的版本。

它包含：

- [\_gaussian_window()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L43)：高斯窗口
- [\_to_patches()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L53)：切 patch
- [\_patch_entropy()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L75)：计算每个 patch 的熵
- [\_load_reference_data()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L125)：加载参考 `.mat` 文件
- [\_batch_mahalanobis()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L142)：批量计算马氏距离
- [fade()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L176) / [fade_with_map()](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py#L194)：完整主算法

这个文件最大的价值是“把完整公式集中展示出来”。

- `fade.py`：一个大而全的实现
- `pipeline.py`：一个拆模块、易维护的实现

目前 `api.py` 实际调用的是 `pipeline.py` 这套模块化实现，不是这个单文件版。

#### [src/fade/ce.py](/home/dong/workspace/my_github_repository/fade/src/fade/ce.py)

这个文件专门负责计算 CE，也就是 Contrast Energy，对应 FADE 的 `f06/f07/f08` 三个特征。

主要函数有：

- `_build_log_filter()`：构造 LoG 滤波器
- `_pad_border()` / `_unpad_border()`：边缘填充和去除
- `_contrast_energy()`：对单通道计算对比能量
- `compute_ce(I)`：对 RGB 图像一次性算出三个 CE 图

输出是：

- `CE_gray`：灰度通道对比能量
- `CE_by`：蓝黄通道对比能量
- `CE_rg`：红绿通道对比能量

#### [src/fade/models/context.py](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py)

这个文件非常重要。它定义了 `FeatureContext`，相当于“特征计算时共享的中间数据仓库”。

为什么要有它？

因为 12 个特征里很多东西会重复用到，比如：

- RGB 三个通道
- 灰度图
- 暗通道 `Id`
- 饱和度 `Is`
- `rg` / `by` 色彩对手通道
- MSCN 图
- `sigma_map`
- `cv`
- CE 图
- patch 切分结果

如果每个特征文件都自己重复算一次，会很浪费。

所以 `FeatureContext` 用了很多 `@property` 和 `_cache`：

- 第一次访问时才计算
- 计算完后放进缓存
- 后面其他特征直接复用

这是一种“惰性计算 + 缓存”的工程写法。

关键定位：

- [FeatureContext](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L15)
- [image_rgb](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L23)
- [Ig_int](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L58)
- [Id](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L64)
- [Is](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L70)
- [rg](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L76)
- [by](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L82)
- [mscn](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L88)
- [sigma_map](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L97)
- [cv](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L102)
- [mscn_v](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L107)
- [mscn_v_patches](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L113)
- [CE_gray](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L119)
- [CE_by](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L128)
- [CE_rg](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L133)
- [to_patches()](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py#L138)

#### [src/fade/models/reference_stats.py](/home/dong/workspace/my_github_repository/fade/src/fade/models/reference_stats.py)

作用是加载参考统计数据：

- `natural_fogfree_image_features_ps8.mat`
- `natural_foggy_image_features_ps8.mat`

使用了：

```python
@lru_cache(maxsize=1)
```

意思是：

- 第一次加载文件时读磁盘
- 后面再调用直接用缓存，不重复读取

这些 `.mat` 文件里存的是训练阶段得到的统计量，比如：

- 均值向量 `mu_*`
- 协方差矩阵 `cov_*`

关键定位：

- [load_reference_stats()](/home/dong/workspace/my_github_repository/fade/src/fade/models/reference_stats.py#L12)

#### [src/fade/ops/](/home/dong/workspace/my_github_repository/fade/src/fade/ops)

这一层是底层公共运算：

- `patches.py`
  - 把二维图像切成很多不重叠的 patch
- `entropy.py`
  - 计算每个 patch 的香农熵
- `mscn.py`
  - 计算 `mscn`、`sigma_map`、`cv`
- `distance.py`
  - 批量计算马氏距离
- `ce.py`
  - 作为适配层导出 `compute_ce`

对应源码：

- [src/fade/ops/patches.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/patches.py)
- [src/fade/ops/entropy.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/entropy.py)
- [src/fade/ops/mscn.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/mscn.py)
- [src/fade/ops/distance.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/distance.py)
- [src/fade/ops/ce.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/ce.py)

关键定位：

- [to_patches()](/home/dong/workspace/my_github_repository/fade/src/fade/ops/patches.py#L8)
- [patch_entropy()](/home/dong/workspace/my_github_repository/fade/src/fade/ops/entropy.py#L8)
- [gaussian_window()](/home/dong/workspace/my_github_repository/fade/src/fade/ops/mscn.py#L9)
- [compute_mscn_components()](/home/dong/workspace/my_github_repository/fade/src/fade/ops/mscn.py#L19)
- [batch_mahalanobis()](/home/dong/workspace/my_github_repository/fade/src/fade/ops/distance.py#L8)
- [compute_ce()](/home/dong/workspace/my_github_repository/fade/src/fade/ce.py#L68)

#### [src/fade/features/](/home/dong/workspace/my_github_repository/fade/src/fade/features)

这一层是整个项目最“算法化”的部分。每个文件对应 FADE 的一个特征。

- `base.py`
  - 定义特征模块都要遵守的接口
- `registry.py`
  - 按固定顺序注册 `f01 ~ f12`
- `f01.py ~ f12.py`
  - 各个具体特征的实现

对应源码：

- [src/fade/features/base.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/base.py)
- [src/fade/features/registry.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/registry.py)
- [f01.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f01.py)、[f02.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f02.py)、[f03.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f03.py)、[f04.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f04.py)
- [f05.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f05.py)、[f06.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f06.py)、[f07.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f07.py)、[f08.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f08.py)
- [f09.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f09.py)、[f10.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f10.py)、[f11.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f11.py)、[f12.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f12.py)

关键定位：

- [Feature 协议](/home/dong/workspace/my_github_repository/fade/src/fade/features/base.py#L12)
- [canonical_feature_registry()](/home/dong/workspace/my_github_repository/fade/src/fade/features/registry.py#L9)
- [default_feature_registry()](/home/dong/workspace/my_github_repository/fade/src/fade/features/registry.py#L32)
- [f01.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f01.py#L16)、[f02.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f02.py#L16)、[f03.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f03.py#L16)、[f04.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f04.py#L16)
- [f05.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f05.py#L16)、[f06.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f06.py#L16)、[f07.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f07.py#L16)、[f08.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f08.py#L16)
- [f09.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f09.py#L17)、[f10.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f10.py#L16)、[f11.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f11.py#L16)、[f12.compute()](/home/dong/workspace/my_github_repository/fade/src/fade/features/f12.py#L16)

### 1.3 整体一句话理解

这个 `src` 目录本质上是在做一件事：

- 把输入图片切成很多 `8x8` 小块
- 对每个小块提取 12 个和雾相关的统计特征
- 再和“有雾/无雾”参考分布比较
- 输出一个 FADE 分数，分数越高通常表示雾越重

---

## 2. 调用流程图

下面这张图对应模块化版本的实际调用路径，也就是 `api.py -> pipeline.py -> context/features/ops -> reference_stats` 这条线。

```text
用户代码
  |
  |  调用
  v
fade(image)                       fade_with_map(image)
  |                                      |
  |--------------------------------------|
                  |
                  v
        src/fade/api.py
                  |
                  | 使用默认流水线
                  v
     _default_pipeline.run(image)
                  |
                  v
      src/fade/pipeline.py
        FadePipeline.run()
                  |
                  | 1. 构建上下文
                  v
      FeatureContext(image)
      src/fade/models/context.py
                  |
                  | 提供并缓存各种中间结果
                  | R/G/B, 灰度图, MSCN, CE, patch信息...
                  |
                  v
      compute_feature_maps(context)
                  |
                  | 2. 依次运行 12 个特征模块
                  v
      src/fade/features/registry.py
                  |
                  | 返回 [f01, f02, ..., f12]
                  v
   +--------------+--------------+--------------+
   |              |              |              |
   v              v              v              v
 f01.py         f02.py         ...            f12.py
   |              |                             |
   |              |                             |
   +--------------+--------------+--------------+
                  |
                  | 每个特征输出一张 2D patch map
                  v
      build_feature_matrix(feature_maps)
                  |
                  | 3. 展平并拼成特征矩阵
                  |    shape: (N_patches, 12)
                  | 4. 做 log1p 变换
                  v
                feat
                  |
                  | 5. 计算每个 patch 的方差 patch_var
                  v
      load_reference_stats()
      src/fade/models/reference_stats.py
                  |
                  | 读取两个参考分布
                  | - fogfree
                  | - foggy
                  v
      mu_free, cov_free, mu_foggy, cov_foggy
                  |
                  | 6. 分别计算到两类参考分布的距离
                  v
      batch_mahalanobis(...)
      src/fade/ops/distance.py
           |                     |
           |                     |
           v                     v
       dist_free             dist_foggy
           |                     |
           v                     v
          Df                   Dff
           |                     |
           +----------+----------+
                      |
                      | 7. 计算最终分数
                      v
         score = Df / (Dff + 1.0)
         D_map = Df_map / (Dff_map + 1.0)
                      |
                      v
         fade() -> 返回 score
         fade_with_map() -> 返回 (score, D_map)
```

压缩成一句话就是：

```text
输入图像
-> 建立上下文并预处理
-> 提取 12 个雾相关特征
-> 拼成每个 patch 的 12 维特征向量
-> 与“无雾/有雾”参考统计分布比较
-> 得到最终 FADE 分数和局部雾图
```

---

## 3. 数据依赖图

下面这张图是 `FeatureContext` 里的“数据依赖图”。可以把它理解成：输入图片进来后，中间量是怎么一步一步被算出来，并最终被 12 个特征使用的。

```text
原始输入图像 image
(shape: H, W, 3)
        |
        v
image_rgb
- 裁剪到 patch_size=8 的整数倍
- 只保留前 3 个通道
        |
        +-----------------------------+
        |                             |
        v                             v
        R                             G
        |                             |
        +-------------+---------------+
                      |
                      v
                      B

R, G, B
  |
  +---------------------> Ig_int
  |                       灰度图
  |                       Ig = 0.2989R + 0.5870G + 0.1140B
  |
  +---------------------> Id
  |                       暗通道
  |                       min(R, G, B) / 255
  |
  +---------------------> rg
  |                       红绿对手通道
  |                       R - G
  |
  +---------------------> by
  |                       蓝黄对手通道
  |                       0.5(R + G) - B
  |
  +---------------------> Is
                          饱和度
                          由 RGB -> HSV 后取 S 通道


Ig_int
  |
  v
Ig_int.astype(float)
  |
  v
compute_mscn_components(...)
(src/fade/ops/mscn.py)
  |
  +---------------------> mscn
  |
  +---------------------> sigma_map
  |
  +---------------------> cv = sigma_map / mu


mscn
  |
  v
mscn_v = mscn * roll(mscn, 1, axis=0)
  |
  v
mscn_v_patches


image_rgb
  |
  v
compute_ce(image_rgb)
(src/fade/ops/ce.py -> src/fade/ce.py)
  |
  +---------------------> CE_gray
  |
  +---------------------> CE_by
  |
  +---------------------> CE_rg
```

下面是这些中间数据分别被哪些特征使用：

```text
mscn ------------------------> f01
mscn_v_patches -------------> f02, f03
sigma_map ------------------> f04
cv -------------------------> f05
CE_gray --------------------> f06
CE_by ----------------------> f07
CE_rg ----------------------> f08
Ig_int ---------------------> f09
Id -------------------------> f10
Is -------------------------> f11
rg + by --------------------> f12
```

再把它和 `to_patches(...)` 连起来看，会更完整：

```text
某个中间图
(mscn / sigma_map / CE_gray / Id ...)
        |
        v
to_patches(...)
把整张图切成很多 8x8 小块
        |
        v
每个 patch 变成长度 64 的一行
        |
        v
在每个 patch 上做统计
mean / var / std / entropy
        |
        v
得到一个 2D 特征图
(shape: patch_row_num, patch_col_num)
```

最关键的一点是，`FeatureContext` 使用缓存 `_cache`：

- 第一次访问某个属性时才计算
- 后面再访问时直接复用
- 避免 12 个特征重复算同样的数据

---

## 4. 12 个特征的详细说明

先给一个总体认识：

这 12 个特征不是直接“测雾浓度”，而是在测图像里一些会被雾影响的统计性质，比如：

- 局部对比度会下降
- 边缘会变弱
- 颜色会变灰、饱和度变低
- 暗区域会被提亮
- 图像细节分布会改变

FADE 的做法就是把这些现象量化成 12 个数字。

### 4.1 共同背景：patch 和特征图

整张图会先被切成很多个 `8x8` 的小块，也就是 patch。

对每个 patch，程序都会算出 12 个特征值之一。所以每个特征最后都不是一个单独数字，而是一张二维特征图：

```text
(patch_row_num, patch_col_num)
```

例如：

- `f01[i, j]` 表示第 `i, j` 个 patch 的第 1 个特征值
- `f09[i, j]` 表示第 `i, j` 个 patch 的第 9 个特征值

后面再把 12 张特征图拼起来，形成每个 patch 的 12 维向量。

### 4.2 MSCN 相关特征：`f01`, `f02`, `f03`

这三个特征建立在 `MSCN` 上。

#### 什么是 MSCN？

MSCN 可以粗略理解为“局部均值去除 + 局部对比归一化”。

代码里在 [src/fade/models/context.py](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py) 和 [src/fade/ops/mscn.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/mscn.py) 中是这样算的：

```python
mu = ndimage.convolve(Ig_f, win, mode="nearest")
sigma_map = sqrt(abs(convolve(Ig_f * Ig_f, win) - mu * mu))
mscn = (Ig_f - mu) / (sigma_map + 1.0)
```

其中：

- `Ig_f`：灰度图
- `mu`：每个像素附近的局部平均亮度
- `sigma_map`：每个像素附近的局部标准差
- `mscn`：像素值减去局部均值，再除以局部波动

这样做后，图像中结构、纹理、边缘会更突出，而绝对亮度影响被削弱。

#### `f01`: MSCN patch variance

- 含义：每个 patch 内，MSCN 值的方差
- 计算方法：
  1. 先得到整张图的 `mscn`
  2. 切成 patch
  3. 对每个 patch 内的 64 个 MSCN 值求方差

代码本质：

```python
np.nanvar(context.to_patches(context.mscn), axis=2, ddof=1)
```

直观理解：

- 方差大：局部变化明显，纹理/边缘更丰富
- 方差小：局部比较平滑

和雾的关系：

- 雾通常会让局部对比变弱、细节模糊，所以很多区域的结构波动会减弱，MSCN 方差可能变小

#### `f02`: variance of non-negative vertical MSCN products

- 含义：垂直相邻像素的 MSCN 乘积中，非负部分的方差
- 计算方法：

先算：

```python
mscn_v = mscn * roll(mscn, 1, axis=0)
```

表示每个像素的 MSCN 值，乘以上一行对应位置像素的 MSCN 值。

然后切 patch，只保留 `>= 0` 的值，其他设成 `NaN`，最后算方差。

代码思想：

```python
tmp = context.mscn_v_patches.copy()
tmp[tmp < 0] = np.nan
np.nanvar(tmp, axis=2, ddof=1)
```

直观理解：

- 如果两个垂直相邻像素的 MSCN 同号，乘积为正
- 正乘积通常表示相邻像素变化趋势一致

所以 `f02` 衡量的是这种“同向局部相关性”的波动程度。

和雾的关系：

- 雾会改变相邻像素之间的局部统计关系，使纹理和边缘变得更弱、更均匀，因此这种相关性分布会变化

#### `f03`: variance of non-positive vertical MSCN products

- 含义：垂直相邻像素的 MSCN 乘积中，非正部分的方差
- 计算方法：与 `f02` 类似，但保留的是 `<= 0` 的值

```python
tmp = context.mscn_v_patches.copy()
tmp[tmp > 0] = np.nan
np.nanvar(tmp, axis=2, ddof=1)
```

直观理解：

- 如果乘积为负，说明相邻两个像素的 MSCN 一正一负，也就是局部有反向变化
- 这通常与边缘、纹理过渡有关

和雾的关系：

- 雾会削弱边缘，使这种正负切换的统计特性发生变化

所以 `f02` 和 `f03` 是一对互补特征：

- `f02`：关注同向关系
- `f03`：关注反向关系

### 4.3 局部波动和对比度：`f04`, `f05`

#### `f04`: mean local standard deviation

- 含义：每个 patch 内，局部标准差图 `sigma_map` 的平均值
- 计算方法：

在 MSCN 预处理中已经算出：

```python
sigma_map = sqrt(abs(E[x^2] - E[x]^2))
```

然后对每个 patch 求平均：

```python
np.mean(context.to_patches(context.sigma_map), axis=2)
```

直观理解：

- `sigma_map` 描述每个像素周围区域亮度波动有多大
- 值大：周围对比强、细节多
- 值小：周围变化弱、比较平

和雾的关系：

- 雾通常会降低局部对比度，让图像变灰蒙蒙，所以局部标准差常常下降

#### `f05`: mean coefficient of variation

- 含义：每个 patch 内，变异系数 `cv` 的平均值
- 计算方法：

先算：

```python
cv = sigma_map / mu
```

再对 patch 求平均：

```python
np.mean(context.to_patches(context.cv), axis=2)
```

直观理解：

- `cv` 是相对波动程度
- 它不是只看变化大不大，而是看“相对于亮度平均值，变化有多明显”

和雾的关系：

- 雾改变的不只是绝对对比，还会改变不同亮度区域里的相对变化结构，因此 `cv` 也是有用的统计量

### 4.4 Contrast Energy 特征：`f06`, `f07`, `f08`

这三个特征都来自 `compute_ce()`。

它的基本思路是：

1. 对图像某个通道做 LoG 风格滤波
2. 分别得到水平和垂直响应
3. 合成梯度强度
4. 做非线性压缩和阈值处理
5. 得到 CE 图

也就是它在测局部对比和边缘能量。

#### `f06`: mean contrast energy on grayscale channel

- 含义：灰度通道 CE 图在每个 patch 上的平均值
- 计算方法：

```python
np.mean(context.to_patches(context.CE_gray), axis=2)
```

直观理解：

- 反映这个区域在亮度上的边缘/对比强度

和雾的关系：

- 雾会削弱边缘清晰度，使对比能量降低，所以这是非常直接的雾相关特征

#### `f07`: mean contrast energy on blue-yellow channel

- 含义：蓝黄对手颜色通道 `by` 的 CE 平均值
- 计算方法：

`by` 定义为：

```python
0.5 * (R + G) - B
```

先对这个通道算 CE，再对 patch 求均值。

直观理解：

- 它测的不是亮度边缘，而是蓝黄颜色对比的局部能量

和雾的关系：

- 雾不仅降低亮度对比，也会削弱色彩对比，尤其让远处颜色趋于灰白，因此颜色对手通道的能量也会受到影响

#### `f08`: mean contrast energy on red-green channel

- 含义：红绿对手颜色通道 `rg` 的 CE 平均值
- 计算方法：

`rg = R - G`，先算 CE，再求 patch 均值。

直观理解：

- 测量红绿差异形成的颜色边缘和局部对比

和雾的关系：

- 和 `f07` 类似，雾会抹平颜色差异，所以这也是有判别力的特征

### 4.5 信息复杂度：`f09`

#### `f09`: patch-wise grayscale entropy

- 含义：每个灰度 patch 的香农熵
- 计算方法：
  1. 统计像素值直方图
  2. 转成概率分布 `p`
  3. 计算 `entropy = -sum(p * log2(p))`

代码在 [src/fade/ops/entropy.py](/home/dong/workspace/my_github_repository/fade/src/fade/ops/entropy.py)。

直观理解：

- 如果一个 patch 里像素都差不多，熵低
- 如果像素分布很丰富，熵高

和雾的关系：

- 雾经常会让细节被淹没、层次变少，导致局部灰度分布变得更单一，熵可能下降

### 4.6 暗通道和饱和度：`f10`, `f11`

#### `f10`: mean dark channel

- 含义：每个 patch 的暗通道均值
- 计算方法：

先对每个像素算：

```python
Id = min(R, G, B) / 255.0
```

再在 patch 上求平均。

直观理解：

- 暗通道表示一个像素在三个颜色通道里最暗的那个值

和雾的关系：

- 在清晰自然图像里，很多区域通常会存在比较暗的颜色分量
- 而有雾时，由于空气光叠加，暗区域会被整体抬亮

所以 `f10` 对识别雾非常重要。

#### `f11`: mean saturation

- 含义：每个 patch 的颜色饱和度平均值
- 计算方法：

先把 RGB 转成 HSV，再取 S 通道：

```python
Is = rgb_to_hsv(image_rgb / 255.0)[:, :, 1]
```

然后对 patch 求均值。

直观理解：

- 饱和度越高，颜色越鲜艳
- 饱和度越低，颜色越灰

和雾的关系：

- 雾会让颜色发白、发灰、失去鲜艳度，所以饱和度通常下降

### 4.7 综合色彩丰富度：`f12`

#### `f12`: colorfulness

- 含义：每个 patch 的综合色彩丰富度
- 计算方法：

先构造两个颜色对手通道：

- `rg = R - G`
- `by = 0.5 * (R + G) - B`

然后在每个 patch 上分别计算：

- `rg_std`, `by_std`
- `rg_mean`, `by_mean`

最后组合成：

```python
sqrt(rg_std^2 + by_std^2) + 0.3 * sqrt(rg_mean^2 + by_mean^2)
```

直观理解：

- 综合考虑了颜色变化是否丰富，以及颜色偏离灰色中性点是否明显

和雾的关系：

- 雾会削弱色彩层次，让画面偏灰、偏白，因此 colorfulness 往往会降低

### 4.8 按类别整理 12 个特征

#### 1. 结构/纹理统计

- `f01`: MSCN 方差
- `f02`: 垂直 MSCN 正乘积方差
- `f03`: 垂直 MSCN 负乘积方差

这组在看局部结构和相邻像素关系。

#### 2. 局部对比波动

- `f04`: 局部标准差均值
- `f05`: 局部变异系数均值

这组在看局部亮度变化强度。

#### 3. 边缘与对比能量

- `f06`: 灰度 CE
- `f07`: 蓝黄 CE
- `f08`: 红绿 CE

这组在看亮度和颜色上的边缘/对比。

#### 4. 信息复杂度

- `f09`: 熵

这组在看 patch 内灰度分布复杂度。

#### 5. 雾对颜色和暗区域的影响

- `f10`: 暗通道
- `f11`: 饱和度
- `f12`: 色彩丰富度

这组在看雾对亮度、颜色、空气光的典型影响。

### 4.9 这些特征如何进入最终分数

这 12 个特征会被拼成一个矩阵：

```python
feat = np.log1p(np.column_stack([f.ravel() for f in feature_maps]))
```

意思是：

- 每个 patch 一行
- 每个特征一列
- 一共 12 列

然后和两组参考统计量比较：

- 一组是自然无雾图像的特征分布
- 一组是自然有雾图像的特征分布

算出两个距离：

- `Df`: 离无雾分布有多远
- `Dff`: 离有雾分布有多远

最后：

```python
score = Df / (Dff + 1.0)
```

可以粗略理解成：

- 如果更像有雾图，分数会偏大
- 如果更像无雾图，分数会偏小

---

## 5. 12 个特征学习表格

下面是一张适合复习和速查的表格。

| 编号 | 文件                                                                              | 名称                          | 输入数据         | 计算方法                                          | 主要反映什么               | 和雾的关系                           |
| ---- | --------------------------------------------------------------------------------- | ----------------------------- | ---------------- | ------------------------------------------------- | -------------------------- | ------------------------------------ |
| f01  | [f01.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f01.py) | MSCN patch variance           | `mscn`           | 对每个 `8x8` patch 的 MSCN 值求方差               | 局部结构、纹理波动强度     | 雾会削弱细节和局部对比，方差常变小   |
| f02  | [f02.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f02.py) | 非负垂直 MSCN 乘积方差        | `mscn_v_patches` | 垂直相邻像素 MSCN 相乘，只保留 `>=0` 的值后求方差 | 相邻像素同向变化的统计特征 | 雾会改变局部相关性分布               |
| f03  | [f03.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f03.py) | 非正垂直 MSCN 乘积方差        | `mscn_v_patches` | 垂直相邻像素 MSCN 相乘，只保留 `<=0` 的值后求方差 | 相邻像素反向变化的统计特征 | 雾会削弱边缘和过渡结构               |
| f04  | [f04.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f04.py) | mean local standard deviation | `sigma_map`      | 对每个 patch 内的局部标准差取平均                 | 局部对比度、亮度波动强度   | 雾会让画面更平、更灰，局部波动常下降 |
| f05  | [f05.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f05.py) | mean coefficient of variation | `cv`             | 对每个 patch 内的 `cv = sigma / mu` 求平均        | 相对波动程度               | 雾会改变亮度与对比的相对关系         |
| f06  | [f06.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f06.py) | grayscale contrast energy     | `CE_gray`        | 对灰度 CE 图在 patch 上求平均                     | 灰度边缘和对比能量         | 雾会削弱亮度边缘和清晰度             |
| f07  | [f07.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f07.py) | blue-yellow contrast energy   | `CE_by`          | 对蓝黄通道 CE 图在 patch 上求平均                 | 蓝黄颜色对比能量           | 雾会减弱颜色差异                     |
| f08  | [f08.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f08.py) | red-green contrast energy     | `CE_rg`          | 对红绿通道 CE 图在 patch 上求平均                 | 红绿颜色对比能量           | 雾会减弱颜色边缘                     |
| f09  | [f09.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f09.py) | patch entropy                 | `Ig_int`         | 统计 patch 灰度直方图并计算香农熵                 | 局部信息复杂度             | 雾会让细节减少，熵常下降             |
| f10  | [f10.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f10.py) | mean dark channel             | `Id`             | 对 `min(R, G, B) / 255` 在 patch 上求平均         | 暗区域特征                 | 雾会把暗区域抬亮，暗通道统计会变化   |
| f11  | [f11.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f11.py) | mean saturation               | `Is`             | RGB 转 HSV 后，取 S 通道并在 patch 上求平均       | 颜色鲜艳程度               | 雾会让颜色发灰，饱和度下降           |
| f12  | [f12.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f12.py) | colorfulness                  | `rg`, `by`       | 综合 `rg/by` 的均值和标准差                       | 色彩丰富度                 | 雾会降低整体色彩感和颜色层次         |

再给一版按类别记忆的压缩表：

| 类别                 | 特征          | 记忆关键词                 |
| -------------------- | ------------- | -------------------------- |
| 局部结构             | `f01 f02 f03` | MSCN、相邻像素关系、纹理   |
| 局部对比             | `f04 f05`     | 标准差、变异系数           |
| 边缘/颜色对比        | `f06 f07 f08` | Contrast Energy            |
| 信息量               | `f09`         | 熵                         |
| 雾对颜色和亮度的影响 | `f10 f11 f12` | 暗通道、饱和度、色彩丰富度 |

最适合初学者记忆的一句总结：

```text
f01-f05 看结构和对比
f06-f08 看边缘和颜色对比
f09 看信息复杂度
f10-f12 看雾对暗通道、饱和度、色彩的影响
```

---

## 6. 建议阅读顺序

如果你是初学者，建议按这个顺序阅读代码：

1. [src/fade/api.py](/home/dong/workspace/my_github_repository/fade/src/fade/api.py)
2. [src/fade/pipeline.py](/home/dong/workspace/my_github_repository/fade/src/fade/pipeline.py)
3. [src/fade/models/context.py](/home/dong/workspace/my_github_repository/fade/src/fade/models/context.py)
4. [src/fade/features/registry.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/registry.py)
5. 挑 2 到 3 个特征文件先看，比如 [f01.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f01.py)、[f06.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f06.py)、[f09.py](/home/dong/workspace/my_github_repository/fade/src/fade/features/f09.py)
6. 再看 [src/fade/ops/](/home/dong/workspace/my_github_repository/fade/src/fade/ops) 里的底层函数
7. 最后回头看 [src/fade/fade.py](/home/dong/workspace/my_github_repository/fade/src/fade/fade.py)

这样你会比较容易把“项目结构”和“算法细节”同时串起来。
