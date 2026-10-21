# Research Journal

- [Design Document](../design/design_doc.md)

## 2026-10-19

- 确定 Week 7 选题：**圆明园大水法（西洋楼）**，取 **1860 前**的状态（非废墟）。
- 复制模板建立项目目录 `projects/yuanmingyuan_dashuifa/`。
- 起草设计文档与来源清单（`sources/processed/source-manifest.md`）。
- 已找到并在网络核实资料来源，下载 4 份公有领域原件到 `sources/raw/`：
  - 伊兰泰《西洋楼铜版画》第 14 幅（远瀛观正面）、第 15 幅（大水法正面/南面）、
    第 16 幅（观水法正面），1786，铜版，故宫博物院等藏；数字版取自 Wikimedia Commons。
  - Ernst Ohlmer（奥尔末）约 1873 年摄"远瀛观南面"老照片；数字版取自 Wikimedia Commons。
  - 有意思的巧合：奥**尔末本人就是中国海关官员**，与 week-3 的海关项目呼应。
- 登记到 `sources/processed/source-manifest.md`，并区分了"毁前证据（铜版画）"与
  "废墟证据（老照片）"。
- 难点已记录：铜版画是线描、无真实色彩；网络下载时被 Wikimedia 限流（429），
  改用 `curl -L` + 规范的 User-Agent 才成功。
- 待办：用铜版画第 14/15/16 幅写 A 图提示词，并做 B 图（仅凭描述）对照。
