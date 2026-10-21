# Project Design Document

## Project Title

大维德花瓶（元至正十一年青花云龙纹象耳瓶）：复原 1351 年状态，有据图 vs 凭空图，并转 3D

## Project Files

- [Research Journal](../journal/research_journal.md)
- [Source Manifest](../../sources/processed/source-manifest.md)

## Background and Context

大维德花瓶是一对元代景德镇青花庙供大瓶，瓶颈写有至正十一年（1351）铭文，是**已知最早带
纪年款的青花瓷**，据此把青花瓷的成熟年代从明代上推到元代。张进文（张文进）向婺源星源
道观进奉一对花瓶与一件香炉（香炉已佚）。原器象首耳内曾挂瓷环，今仅存磨痕。现藏大英博物馆
95 号展厅（Sir Percival David 收藏，编号 PDF B.613 / B.614）。

## Research Questions

1. 1351 年这对瓶的**形制**（盘口、束颈、象首耳+瓷环、器身九条装饰带）是什么样？
2. 哪些资料能把**器形、九条纹样带、铭文、比例**做对？资料不足处有哪些？
3. 有据图（A）与"仅凭文字描述"的图（B）差异具体在哪几处？
4. 生成器在两种做法里分别**编造**了什么？

## Scope

- **In scope:** 单支花瓶的 1351 状态（选 PDF B.614：高 63.8cm、最大径 19.6cm、重 7.7kg），
  含象首耳与"原挂瓷环"的复原；需要时并排一对。
- **Out of scope:** 那件已佚的香炉；铭文逐字书法复原（太细）。

## Methodology

1. **依据权威来源**：大英博物馆藏品著录（器形描述 + 九条带 + 八种纹样 + 尺寸）、
   高清正视图、铭文特写照、纹样细部照。
2. **做对照图**：
   - A 图：结构化提示词，逐项写入——铜器造型、盘口、束颈、象首双耳（原挂瓷环）、
     颈部分层（缠枝扁菊 / 蕉叶 / 飞凤灵芝 / 缠枝莲）、腹部四爪云龙、下部海涛×2 /
     缠枝牡丹 / 覆莲杂宝；釉下青花。
   - B 图：只写"一只中国青花瓷瓶"，模拟无资料者。
   - 并排，逐项回答研究问题 1–3。
3. **转 3D**：image-to-3D（如 Tripo）用正视图生成主体；象耳/瓷环若不足，单独做再拼装。
   路线待定，用前查价留收据。
4. **第 4 步用途**：待定（短片/陈列场景/动画）。

## Sources

见 [source-manifest.md](../../sources/processed/source-manifest.md)。核心：大英博物馆
PDF B.613 / B.614 藏品著录（含铭文原录与英译）+ Commons 高清照片（公有领域 / CC BY）。

## Expected Outputs

- `research/outputs/`：A/B 两张对照图 + 说明文字。
- `artifacts/`：3D 模型文件、渲染截图/录屏（git 忽略）。
- 工具日志（prompt、输入、输出、花费）。

## Working Hypotheses

- A 图能在**九条装饰带的顺序与题材、四爪云龙、象首耳**上明显更准。
- B 图会给出泛化的"青花大瓶"，缺象耳、缺分层纹样、龙形随意。
- 两张都会在**釉色浓淡、胎体火石红、比例**上编造。

## Risks and Open Questions

- 釉下青花的**发色深浅**受窑温影响，文字资料无法还原准确色阶——须标注为推断。
- 象耳内**瓷环**已失，只有磨痕证据；复原属合理推测，须说明。
- 单张正视图做 image-to-3D，**背面纹样会被镜像/编造**（龙朝向左右两瓶相反）——需核对。
- 若无法运行 Blender：只用 image-to-3D 服务即可。
- 工具与花费已定（见 `research/notes/tools-and-cost.md`）：图像用 Gemini 应用（香港可用，
  免费用 Nano Banana 2）；3D 用 **Meshy 免费**（腾讯混元因需实名/领额度、港区不可用已弃用）。
  **全程 HK$0**。

## Action Items

- [x] 找到权威来源（大英博物馆 PDF B.613/B.614）并核实关键事实。
- [x] 下载公有领域/开放许可高清照片到 `sources/raw/`。
- [x] 写 source-manifest。
- [x] 用著录写 A 图结构化提示词，并写 B 图（仅凭描述）提示词（见 `research/notes/image-prompts.md`）。
- [ ] 生成 A 图与 B 图，并排导出到 `research/outputs/`。
- [ ] 回答三个对照问题。
- [ ] 选 image-to-3D 路线，产出 3D 模型。
- [x] 第 4 步用途定为**虚拟展厅**：`code/virtual_gallery/`（three.js，玻璃展柜 + 解说面板 + 自动旋转）。
- [ ] 工具日志 + 至少一个真实困难。
