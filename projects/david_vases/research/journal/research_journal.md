# Research Journal

- [Design Document](../design/design_doc.md)

## 2026-10-19

- 原选题"圆明园大水法"偏难（整片建筑群 + 线描图版），改选**单件器物**：
  **元至正十一年青花云龙纹象耳瓶（大维德花瓶）**。理由：单件、对称，image-to-3D 稳；
  权威资料极全（大英博物馆编号 PDF B.613/B.614）。
- 复制模板建立项目目录 `projects/david_vases/`。
- 网络核实关键事实：1351、景德镇、张进文供奉、最早纪年青花、九条纹样带、象首耳原挂瓷环。
- 下载 3 张公有领域 / 开放许可照片到 `sources/raw/`（Szilas；Marie-Lan Nguyen）。
- 写 `sources/processed/source-manifest.md`；完成设计文档。
- 选题"历史点"定为 **1351 年状态**——尤其象首耳内**原挂瓷环**（今仅存磨痕），
  这是有据图能还原、凭空图做不到的差异点。
- 起草图像提示词，存 `research/notes/image-prompts.md`：
  - A 图（有据）：结构化英文/中文提示词，逐条写入九条装饰带、象首耳+原挂瓷环、四爪云龙。
  - B 图（凭空）：仅 `a Chinese blue-and-white porcelain vase` 一句。
  - 附负面提示、A 图检查点、并排三问模板、花费记录表。
- 已知预期缺陷：生成器写不出正确汉字，A 图铭文会是伪字——如实记录。
- 定工具（香港 + 仅银联 + 免费），记入 `research/notes/tools-and-cost.md`：
  图像用 **Gemini 应用**（Nano Banana 2，免费≤20张/天）；3D 用 **腾讯混元 3D**（免费20次/天，
  微信登录）。**全程 HK$0，无需付款**。注意：香港用不了 Google AI Studio/API，须用 Gemini 应用。
- 第 4 步用途定为**虚拟展厅**；已搭好 `code/virtual_gallery/`（`index.html` + `serve.cmd`，three.js）。
  本地启动测试通过（HTTP 200）。把导出模型命名为 `vase.glb` 放进该文件夹即可看到展柜效果。
- 实测：**腾讯混元3D 用不了**（积分 0，报"次数已达上限"）——免费额度需腾讯云开通+实名+手动领取，
  国际站新用户活动 2026-06-30 已截止，港区账号不符合。改用它站免费服务，记入 `tools-and-cost.md`：
  **Meshy 免费**（首选）/ **Hugging Face Spaces**（不用注册）/ **Tripo 免费**，均导出 GLB。
- 3D 模型：改由 **Blender 程序化建模**（`code/blender_build_vase.py`），已生成并导出
  `code/virtual_gallery/vase.glb`（0.205×0.195×0.638 m，308 KB，glTF 有效）。
  组成：瓶身旋成（盘口/束颈/鼓腹/圈足）+ 两侧象首耳 + 悬环 + 白瓷材质。
  免费服务的导出限制（Tripo 付费墙、Meshy 贴图付费、HF ZeroGPU 额度）由此绕过。
- 改用**腾讯混元最终模型** `hunyuan.glb`（82 MB，150 万面，含 PBR 贴图：底图/法线/金属粗糙），
  已移入 `artifacts/`（git 忽略）。节点自带 +90°X 旋转，three.js 中自动立起；
  尺寸约 0.40×0.40×1.16（模型单位），展厅里会按包围盒缩放到 2 单位高。
- 展厅改为**从项目根目录**启动服务器（`serve.cmd`），`MODEL_URL` 指向 `../../artifacts/hunyuan.glb`；
  本地测试通过：页面 200、GLB 200（Content-Length 82.7MB）。
- 修展厅两个问题：
  1) **闪烁（z-fighting）**：房间原来是实心 Box，底面与地板同在 y=0 相互抢面 → 改为四壁+天花板，
     玻璃改为稳定透明材质（去 transmission）。
  2) **模型过重**：用 Blender 后台模式（`D:\blender.exe -b`）Decimate 150 万面→15 万面、
     贴图 4K→1K、JPEG 压缩，导出 `artifacts/hunyuan_lite.glb`（82MB→5.7MB）。
  `MODEL_URL` 改为 `/artifacts/hunyuan_lite.glb`。本地验证：页面 200、模型 200。
- 待办：按此生成 A/B 两图并排导出到 `research/outputs/`。
- 未决：瓷环复原属推测，如何在答案里标注？——记入根目录 `questions.md`。
