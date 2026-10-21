# 虚拟展厅 · Virtual Gallery

纯前端虚拟展厅：把**大维德花瓶**（腾讯混元生成、带青花贴图的 GLB）放进玻璃展柜，
配暖色射灯、木底座和中文解说面板。可环视、可自动旋转，录屏即为第 4 步成品。

技术：`three.js`（CDN 加载，无需安装）。**完全免费、无账号。**

## 文件与位置

- `index.html` —— 展厅本体（房间 + 展柜 + 灯光 + 解说面板）。
- `serve.cmd` —— 启动本地服务器（**从项目根目录**启动，以便读取 `artifacts/`）。
- 模型：`/artifacts/hunyuan_lite.glb`（腾讯混元导出，已减面/压贴图：约 6 MB，15 万面，含 PBR 贴图）。
  - 原始高模 `artifacts/hunyuan.glb`（82 MB，150 万面）保留作存档。
  - 白模 `code/virtual_gallery/vase.glb`（Blender 程序化生成，308 KB）作备用。

## 怎么用

1. 双击 **`serve.cmd`** → 自动打开 `http://localhost:8000/code/virtual_gallery/`。
2. 首次加载模型较大（约 10–30 秒），稍等。
   - 鼠标左键拖动：环视；滚轮：缩放；右键拖动：平移。
   - **空格**：开/关自动旋转（录屏用）。
   - **L**：开/关解说面板。
3. 录屏：Win + **Alt + R**（Xbox Game Bar），或 **Clipchamp / 剪映**。
4. 成品存 `../../artifacts/`，另截 2–3 张图到 `../../research/outputs/`。

## 备注

- 模型 150 万面偏重；若卡顿，可在 Blender 里 Decimate 到 ~10–20 万面再导出。
- 换模型：改 `index.html` 里 `const MODEL_URL = ...`（相对本页路径）。
- 比例会自动按包围盒缩放到约 2 单位高并居中；`TARGET_HEIGHT` 可调。
